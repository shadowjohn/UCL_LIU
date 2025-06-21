#-----------------------------------------------------------------------------
# Copyright (c) 2013-2018, PyInstaller Development Team.
#
# Distributed under the terms of the GNU General Public License with exception
# for distributing bootloader.
#
# The full license is in the file COPYING.txt, distributed with this software.
#-----------------------------------------------------------------------------


"""
This CArchiveReader is used only by the archieve_viewer utility.
"""

# TODO clean up this module

import struct


from PyInstaller.loader.pyimod02_archive import ArchiveReader


class NotAnArchiveError(Exception):
    pass


class CTOCReader(object):
    """
    A class encapsulating the table of contents of a CArchive.

    When written to disk, it is easily read from C.
    """
    ENTRYSTRUCT = '!iiiiBB'  # (structlen, dpos, dlen, ulen, flag, typcd) followed by name
    ENTRYLEN = struct.calcsize(ENTRYSTRUCT)

    def __init__(self):
        self.data = []

    def frombinary(self, s):
        """
        Decode the binary string into an in memory list.

        S is a binary string.
        """
        p = 0

        while p < len(s):
            (slen, dpos, dlen, ulen, flag, typcd) = struct.unpack(self.ENTRYSTRUCT,
                                                        s[p:p + self.ENTRYLEN])
            nmlen = slen - self.ENTRYLEN
            p = p + self.ENTRYLEN
            (nm,) = struct.unpack('%is' % nmlen, s[p:p + nmlen])
            p = p + nmlen
            # nm may have up to 15 bytes of padding
            nm = nm.rstrip(b'\0')
            nm = nm.decode('utf-8')
            typcd = chr(typcd)
            self.data.append((dpos, dlen, ulen, flag, typcd, nm))


    def get(self, ndx):
        """
        Return the table of contents entry (tuple) at index NDX.
        """
        return self.data[ndx]

    def __getitem__(self, ndx):
        return self.data[ndx]

    def find(self, name):
        """
        Return the index of the toc entry with name NAME.

        Return -1 for failure.
        """
        for i, nm in enumerate(self.data):
            if nm[-1] == name:
                return i
        return -1


class CArchiveReader(ArchiveReader):
    """
    An Archive subclass that can hold arbitrary data.

    This class encapsulates all files that are bundled within an executable.
    It can contain ZlibArchive (Python .pyc files), dlls, Python C extensions
    and all other data files that are bundled in --onefile mode.

    Easily handled from C or from Python.
    """
    # MAGIC is usefull to verify that conversion of Python data types
    # to C structure and back works properly.
    MAGIC = b'MEI\014\013\012\013\016'
    HDRLEN = 0
    LEVEL = 9

    # Cookie - holds some information for the bootloader. C struct format
    # definition. '!' at the beginning means network byte order.
    # C struct looks like:
    #
    #   typedef struct _cookie {
    #       char magic[8]; /* 'MEI\014\013\012\013\016' */
    #       int  len;      /* len of entire package */
    #       int  TOC;      /* pos (rel to start) of TableOfContents */
    #       int  TOClen;   /* length of TableOfContents */
    #       int  pyvers;   /* new in v4 */
    #       char pylibname[64];    /* Filename of Python dynamic library. */
    #   } COOKIE;
    #
    _cookie_format = '!8siiii64s'
    _cookie_size = struct.calcsize(_cookie_format)

    def __init__(self, archive_path=None, start=0, length=0, pylib_name=''):
        """
        Constructor.

        archive_path path name of file (create empty CArchive if path is None).
        start        is the seekposition within PATH.
        len          is the length of the CArchive (if 0, then read till EOF).
        pylib_name   name of Python DLL which bootloader will use.
        """
        self.length = length
        self._pylib_name = pylib_name


        # A CArchive created from scratch starts at 0, no leading bootloader.
        self.pkg_start = 0
        super(CArchiveReader, self).__init__(archive_path, start)

    def checkmagic(self):
        """
        Verify that self is a valid CArchive.

        Magic signature is at end of the archive.

        This fuction is used by ArchiveViewer.py utility.
        """
        # Magic is at EOF; if we're embedded, we need to figure where that is.
        if self.length:
            self.lib.seek(self.start + self.length, 0)
        else:
            self.lib.seek(0, 2)
        filelen = self.lib.tell()

        self.lib.seek(max(0, filelen-4096))
        searchpos = self.lib.tell()
        buf = self.lib.read(min(filelen, 4096))
        pos = buf.rfind(self.MAGIC)
        if pos == -1:
            raise RuntimeError("%s is not a valid %s archive file" %
                               (self.path, self.__class__.__name__))
        filelen = searchpos + pos + self._cookie_size
        (magic, totallen, tocpos, toclen, pyvers, pylib_name) = struct.unpack(
            self._cookie_format, buf[pos:pos+self._cookie_size])
        if magic != self.MAGIC:
            raise RuntimeError("%s is not a valid %s archive file" %
                               (self.path, self.__class__.__name__))

        self.pkg_start = filelen - totallen
        if self.length:
            if totallen != self.length or self.pkg_start != self.start:
                raise RuntimeError('Problem with embedded archive in %s' %
                        self.path)
        # Verify presence of Python library name.
        if not pylib_name:
            raise RuntimeError('Python library filename not defined in archive.')
        self.tocpos, self.toclen = tocpos, toclen

    def loadtoc(self):
        """
        Load the table of contents into memory.
        """
        self.toc = CTOCReader()
        self.lib.seek(self.pkg_start + self.tocpos)
        tocstr = self.lib.read(self.toclen)
        self.toc.frombinary(tocstr)

    def extract(self, name):
        """
        Get the contents of an entry.

        NAME is an entry name OR the index to the TOC.

        Return the tuple (ispkg, contents).
        For non-Python resoures, ispkg is meaningless (and 0).
        Used by the import mechanism.
        """
        if type(name) == type(''):
            ndx = self.toc.find(name)
            if ndx == -1:
                return None
        else:
            ndx = name
        (dpos, dlen, ulen, flag, typcd, nm) = self.toc.get(ndx)

        with self.lib:
            self.lib.seek(self.pkg_start + dpos)
            rslt = self.lib.read(dlen)

        if flag == 1:
            import zlib
            rslt = zlib.decompress(rslt)
        if typcd == 'M':
            return (1, rslt)

        return (typcd == 'M', rslt)

    def contents(self):
        """
        Return the names of the entries.
        """
        rslt = []
        for (dpos, dlen, ulen, flag, typcd, nm) in self.toc:
            rslt.append(nm)
        return rslt

    def openEmbedded(self, name):
        """
        Open a CArchive of name NAME embedded within this CArchive.

        This fuction is used by ArchiveViewer.py utility.
        """
        ndx = self.toc.find(name)

        if ndx == -1:
            raise KeyError("Member '%s' not found in %s" % (name, self.path))
        (dpos, dlen, ulen, flag, typcd, nm) = self.toc.get(ndx)

        if typcd not in "zZ":
            raise NotAnArchiveError('%s is not an archive' % name)

        if flag:
            raise ValueError('Cannot open compressed archive %s in place' %
                    name)
        return CArchiveReader(self.path, self.pkg_start + dpos, dlen)

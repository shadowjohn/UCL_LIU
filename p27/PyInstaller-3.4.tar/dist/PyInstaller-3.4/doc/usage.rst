.. _using pyinstaller:

====================
Using PyInstaller
====================


The syntax of the ``pyinstaller`` command is:

    ``pyinstaller`` [*options*] *script* [*script* ...] | *specfile*

In the most simple case,
set the current directory to the location of your program ``myscript.py``
and execute::

    pyinstaller myscript.py

|PyInstaller| analyzes :file:`myscript.py` and:

* Writes :file:`myscript.spec` in the same folder as the script.
* Creates a folder :file:`build` in the same folder as the script if it does not exist.
* Writes some log files and working files in the ``build`` folder.
* Creates a folder :file:`dist` in the same folder as the script if it does not exist.
* Writes the :file:`myscript` executable folder in the :file:`dist` folder.

In the :file:`dist` folder you find the bundled app you distribute to your users.

Normally you name one script on the command line.
If you name more, all are analyzed and included in the output.
However, the first script named supplies the name for the
spec file and for the executable folder or file.
Its code is the first to execute at run-time.

For certain uses you may edit the contents of ``myscript.spec``
(described under :ref:`Using Spec Files`).
After you do this, you name the spec file to |PyInstaller| instead of the script:

    ``pyinstaller myscript.spec``

The :file:`myscript.spec` file contains most of the information
provided by the options that were specified when
:command:`pyinstaller` (or :command:`pyi-makespec`)
was run with the script file as the argument.
You typically do not need to specify any options when running
:command:`pyinstaller` with the spec file.
Only :ref:`a few command-line options <Using Spec Files>`
have an effect when building from a spec file.

You may give a path to the script or spec file, for example

    ``pyinstaller`` `options...` ``~/myproject/source/myscript.py``

or, on Windows,

    ``pyinstaller "C:\Documents and Settings\project\myscript.spec"``


Options
~~~~~~~~~~~~~~~

General Options
------------------

.. include:: _pyinstaller-options.tmp



Shortening the Command
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Because of its numerous options, a full ``pyinstaller`` command
can become very long.
You will run the same command again and again as you develop
your script.
You can put the command in a shell script or batch file,
using line continuations to make it readable.
For example, in Linux::

    pyinstaller --noconfirm --log-level=WARN \
        --onefile --nowindow \
        --add-data="README:." \
        --add-data="image1.png:img" \
        --add-binary="libfoo.so:lib" \
        --hidden-import=secret1 \
        --hidden-import=secret2 \
        --upx-dir=/usr/local/share/ \
        myscript.spec

Or in Windows, use the little-known BAT file line continuation::

    pyinstaller --noconfirm --log-level=WARN ^
        --onefile --nowindow ^
        --add-data="README;." ^
        --add-data="image1.png;img" ^
        --add-binary="libfoo.so;lib" ^
        --hidden-import=secret1 ^
        --hidden-import=secret2 ^
        --icon=..\MLNMFLCN.ICO ^
        myscript.spec


Running |PyInstaller| with Python optimizations
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. Note::

    When using this feature, you should be aware of how the Python bytecode
    optimization mechanism works. When using ``-O``, ``__debug__`` is set
    to ``False`` and ``assert`` statements are removed from the bytecode.
    The ``-OO`` flag additionally removes docstrings.

    Using this feature affects not only your main script, but *all* modules
    included by |PyInstaller|. If your code (or any module imported by your
    script) relies on these features, your program may break or have
    unexpected behavior.

|PyInstaller| can be run with Python optimization flags (``-O`` or ``-OO``)
by executing it as a Python module, rather than using the ``pyinstaller``
command::

    # run with basic optimizations
    python -O -m PyInstaller myscript.py

    # also discard docstrings
    python -OO -m PyInstaller myscript.py

Or, by explicitly setting the ``PYTHONOPTIMIZE`` environment variable
to a non-zero value::

    # Unix
    PYTHONOPTIMIZE=1 pyinstaller myscript.py

    # Windows
    set PYTHONOPTIMIZE=1 && pyinstaller myscript.py

You can use any |PyInstaller| options that are otherwise available with
the ``pyinstaller`` command. For example::

    python -O -m PyInstaller --onefile myscript.py

Alternatively, you can also use the path to pyinstaller::

    python -O /path/to/pyinstaller myscript.py

Using UPX
~~~~~~~~~~~~~~~~~~~

UPX_ is a free utility available for most operating systems.
UPX compresses executable files and libraries, making them smaller,
sometimes much smaller.
UPX is available for most operating systems and can compress
a large number of executable file formats.
See the UPX_ home page for downloads, and for the list of
supported executable formats.

A compressed executable program is wrapped in UPX
startup code that dynamically decompresses the program
when the program is launched.
After it has been decompressed, the program runs normally.
In the case of a |PyInstaller| one-file executable that has
been UPX-compressed, the full execution sequence is:

* The compressed program start up in the UPX decompressor code.
* After decompression, the program executes the |PyInstaller| |bootloader|,
  which creates a temporary environment for Python.
* The Python interpreter executes your script.

|PyInstaller| looks for UPX on the execution path
or the path specified with the ``--upx-dir`` option.
If UPX exists, |PyInstaller| applies it to the final executable,
unless the ``--noupx`` option was given.
UPX has been used with |PyInstaller| output often, usually with no problems.


.. _encrypting python bytecode:

Encrypting Python Bytecode
~~~~~~~~~~~~~~~~~~~~~~~~~~

To encrypt the Python bytecode modules stored in the bundle,
pass the ``--key=``\ *key-string*  argument on
the command line.

For this to work, you must have the PyCrypto_
module installed.
The *key-string* is a string of 16 characters which is used to
encrypt each file of Python byte-code before it is stored in
the archive inside the executable file.


.. _defining the extraction location:

Defining the Extraction Location
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In rare cases, when you bundle to a single executable
(see :ref:`Bundling to One File` and :ref:`how the one-file program works`),
you may want to control the location of the temporary directory at compile
time. This can be done using the ``--runtime-tmpdir`` option. If this option is
given, the bootloader will ignore any temp-folder location defined by the
run-time OS. Please use this option only if you know what you are doing.


.. _supporting multiple platforms:

Supporting Multiple Platforms
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you distribute your application for only one combination of OS and Python,
just install |PyInstaller| like any other package and use it in your
normal development setup.


Supporting Multiple Python Environments
-----------------------------------------

When you need to bundle your application within one OS
but for different versions of Python and support libraries -- for example,
a Python 3 version and a Python 2.7 version;
or a supported version that uses Qt4 and a development version that uses Qt5 --
we recommend you use virtualenv_.
With virtualenv you can maintain different combinations of Python
and installed packages, and switch from one combination to another easily.
(If you work only with Python 3.4 and later, ``python3 -m venv``
does the same job, see module venv_.)

* Use virtualenv to create as many different development environments as you need,
  each with its unique combination of Python and installed packages.
* Install |PyInstaller| in each environment.
* Use |PyInstaller| to build your application in each environment.

Note that when using virtualenv, the path to the |PyInstaller| commands is:

* Windows: ENV_ROOT\\Scripts
* Others:  ENV_ROOT/bin

Under Windows, the pip-Win_ package installs virtualenv and makes it
especially easy to set up different environments and switch between them.
Under Linux and Mac OS, you switch environments at the command line.

See :pep:`405` for more information about Python virtual environments.


Supporting Multiple Operating Systems
---------------------------------------

If you need to distribute your application for more than one OS,
for example both Windows and Mac OS X, you must install |PyInstaller|
on each platform and bundle your app separately on each.

You can do this from a single machine using virtualization.
The free virtualBox_ or the paid VMWare_ and Parallels_
allow you to run another complete operating system as a "guest".
You set up a virtual machine for each "guest" OS.
In it you install
Python, the support packages your application needs, and PyInstaller.

The Dropbox_ system is useful with virtual machines.
Install a Dropbox client in each virtual machine, all linked to your Dropbox account.
Keep a single copy of your script(s) in a Dropbox folder.
Then on any virtual machine you can run |PyInstaller| thus::

    cd ~/Dropbox/project_folder/src # Linux, Mac -- Windows similar
    rm *.pyc # get rid of modules compiled by another Python
    pyinstaller --workpath=path-to-local-temp-folder  \
                --distpath=path-to-local-dist-folder  \
                ...other options as required...       \
                ./myscript.py

|PyInstaller| reads scripts from the common Dropbox folder,
but writes its work files and the bundled app in folders that
are local to the virtual machine.

If you share the same home directory on multiple platforms, for
example Linux and OS X, you will need to set the PYINSTALLER_CONFIG_DIR
environment variable to different values on each platform otherwise
PyInstaller may cache files for one platform and use them on the other
platform, as by default it uses a subdirectory of your home directory
as its cache location.

It is said to be possible to cross-develop for Windows under Linux
using the free Wine_ environment.
Further details are needed, see `How to Contribute`_.


.. _capturing windows version data:

Capturing Windows Version Data
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A Windows app may require a Version resource file.
A Version resource contains a group of data structures,
some containing binary integers and some containing strings,
that describe the properties of the executable.
For details see the Microsoft `Version Information Structures`_ page.

Version resources are complex and
some elements are optional, others required.
When you view the version tab of a Properties dialog,
there's no simple relationship between
the data displayed and the structure of the resource.
For this reason |PyInstaller| includes the ``pyi-grab_version`` command.
It is invoked with the full path name of any Windows executable
that has a Version resource:

      ``pyi-grab_version`` *executable_with_version_resource*

The command writes text that represents
a Version resource in readable form to standard output.
You can copy it from the console window or redirect it to a file.
Then you can edit the version information to adapt it to your program.
Using ``pyi-grab_version`` you can find an executable that displays the kind of
information you want, copy its resource data, and modify it to suit your package.

The version text file is encoded UTF-8 and may contain non-ASCII characters.
(Unicode characters are allowed in Version resource string fields.)
Be sure to edit and save the text file in UTF-8 unless you are
certain it contains only ASCII string values.

Your edited version text file can be given with the ``--version-file=``
option to ``pyinstaller`` or ``pyi-makespec``.
The text data is converted to a Version resource and
installed in the bundled app.

In a Version resource there are two 64-bit binary values,
``FileVersion`` and ``ProductVersion``.
In the version text file these are given as four-element tuples,
for example::

    filevers=(2, 0, 4, 0),
    prodvers=(2, 0, 4, 0),

The elements of each tuple represent 16-bit values
from most-significant to least-significant.
For example the value ``(2, 0, 4, 0)`` resolves to
``0002000000040000`` in hex.

You can also install a Version resource from a text file after
the bundled app has been created, using the ``pyi-set_version`` command:

    ``pyi-set_version`` *version_text_file* *executable_file*

The ``pyi-set_version`` utility reads a version text file as written
by ``pyi-grab_version``, converts it to a Version resource,
and installs that resource in the *executable_file* specified.

For advanced uses, examine a version text file as written by  ``pyi-grab_version``.
You find it is Python code that creates a ``VSVersionInfo`` object.
The class definition for ``VSVersionInfo`` is found in
``utils/win32/versioninfo.py`` in the |PyInstaller| distribution folder.
You can write a program that imports ``versioninfo``.
In that program you can ``eval``
the contents of a version info text file to produce a
``VSVersionInfo`` object.
You can use the ``.toRaw()`` method of that object to
produce a Version resource in binary form.
Or you can apply the ``unicode()`` function to the object
to reproduce the version text file.


Building Mac OS X App Bundles
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Under Mac OS X, |PyInstaller| always builds a UNIX executable in
:file:`dist`.
If you specify ``--onedir``, the output is a folder named :file:`myscript`
containing supporting files and an executable named :file:`myscript`.
If you specify ``--onefile``, the output is a single UNIX executable
named :file:`myscript`.
Either executable can be started from a Terminal command line.
Standard input and output work as normal through that Terminal window.

If you specify ``--windowed`` with either option, the ``dist`` folder
also contains an OS X application named :file:`myscript.app`.

As you probably know, an application is a special type of folder.
The one built by |PyInstaller| contains a folder always named
:file:`Contents` which contains:

  + A folder :file:`Frameworks` which is empty.
  + A folder :file:`Resources` that contains an icon file.
  + A file :file:`Info.plist` that describes the app.
  + A folder :file:`MacOS` that contains the the executable and 
    supporting files, just as in the ``--onedir`` folder.

Use the ``icon=`` argument to specify a custom icon for the application.
It will be copied into the :file:`Resources` folder.
(If you do not specify an icon file, |PyInstaller| supplies a
file :file:`icon-windowed.icns` with the |PyInstaller| logo.)

Use the ``osx-bundle-identifier=`` argument to add a bundle identifier.
This becomes the ``CFBundleIdentifier`` used in code-signing
(see the `PyInstaller code signing recipe`_
and for more detail, the `Apple code signing overview`_ technical note).

You can add other items to the :file:`Info.plist` by editing the spec file;
see :ref:`Spec File Options for a Mac OS X Bundle` below.


Platform-specific Notes
~~~~~~~~~~~~~~~~~~~~~~~~~~

GNU/Linux
-------------------

Making Linux Apps Forward-Compatible
=====================================

Under Linux, |PyInstaller| does not bundle ``libc``
(the C standard library, usually ``glibc``, the Gnu version) with the app.
Instead, the app expects to link dynamically to the ``libc`` from the
local OS where it runs.
The interface between any app and ``libc`` is forward compatible to
newer releases, but it is not backward compatible to older releases.

For this reason, if you bundle your app on the current version of Linux,
it may fail to execute (typically with a runtime dynamic link error) if
it is executed on an older version of Linux.

The solution is to always build your app on the *oldest* version of
Linux you mean to support.
It should continue to work with the ``libc`` found on newer versions.

The Linux standard libraries such as ``glibc`` are distributed in 64-bit
and 32-bit versions, and these are not compatible.
As a result you cannot bundle your app on a 32-bit system and run it
on a 64-bit installation, nor vice-versa.
You must make a unique version of the app for each word-length supported.

.. _Platform-specific Notes - Windows:

Windows
---------------

For **Python >= 3.5** targeting *Windows < 10*, the developer needs to take
special care to include the Visual C++ run-time .dlls:
Python 3.5 uses Visual Studio 2015 run-time, which has been renamed into
`“Universal CRT“
<https://blogs.msdn.microsoft.com/vcblog/2015/03/03/introducing-the-universal-crt/>`_
and has become part of Windows 10.
For Windows Vista through Windows 8.1 there are Windows Update packages,
which may or may not be installed in the target-system.
So you have the following options:

1. Build on *Windows 7* which has been reported to work.

2. Include one of the VCRedist packages (the redistributable package files)
   into your application's installer. This is Microsoft's recommended way, see
   “Distributing Software that uses the Universal CRT“ in the above-mentioned
   link, numbers 2 and 3.

3. Install the `Windows Software Development Kit (SDK) for Windows 10
   <https://dev.windows.com/en-us/downloads/windows-10-sdk>`_ and expand the
   `.spec`-file to include the required DLLs, see “Distributing Software that
   uses the Universal CRT“ in the above-mentioned link, number 6.

   If you think, |PyInstaller| should do this by itself, please :ref:`help
   improving <how-to-contribute>` |PyInstaller|.



Mac OS X
-------------------

Making Mac OS X apps Forward-Compatible
========================================

In Mac OS X, components from one version of the OS are usually compatible
with later versions, but they may not work with earlier versions.

The only way to be certain your app supports an older version of Mac OS X
is to run PyInstaller in the oldest version of the OS you need to support.

For example, to be sure of compatibility with "Snow Leopard" (10.6)
and later versions, you should execute PyInstaller in that environment.
You would create a copy of Mac OS X 10.6, typically in a virtual machine.
In it, install the desired level of Python
(the default Python in Snow Leopard was 2.6, which PyInstaller no longer supports),
and install |PyInstaller|, your source, and all its dependencies.
Then build your app in that environment.
It should be compatible with later versions of Mac OS X.


Building 32-bit Apps in Mac OS X
====================================

Older versions of Mac OS X supported both 32-bit and 64-bit executables.
PyInstaller builds an app using the the word-length of the Python used to execute it.
That will typically be a 64-bit version of Python,
resulting in a 64-bit executable.
To create a 32-bit executable, run PyInstaller under a 32-bit Python.

Python as installed in OS X will usually be executable in either 64- or 32-bit mode.
To verify this, apply the ``file`` command to the Python executable::

    $ file /usr/local/bin/python3
    /usr/local/bin/python3: Mach-O universal binary with 2 architectures
    /usr/local/bin/python3 (for architecture i386):     Mach-O executable i386
    /usr/local/bin/python3 (for architecture x86_64):   Mach-O 64-bit executable x86_64

The OS chooses which architecture to run, and typically defaults to 64-bit.
You can force the use of either architecture by name using the ``arch`` command::

    $ /usr/local/bin/python3
    Python 3.4.2 (v3.4.2:ab2c023a9432, Oct  5 2014, 20:42:22)
    [GCC 4.2.1 (Apple Inc. build 5666) (dot 3)] on darwin
    Type "help", "copyright", "credits" or "license" for more information.
    >>> import sys; sys.maxsize
    9223372036854775807

    $ arch -i386 /usr/local/bin/python3
    Python 3.4.2 (v3.4.2:ab2c023a9432, Oct  5 2014, 20:42:22)
    [GCC 4.2.1 (Apple Inc. build 5666) (dot 3)] on darwin
    Type "help", "copyright", "credits" or "license" for more information.
    >>> import sys; sys.maxsize
    2147483647

Apple's default ``/usr/bin/python`` may circumvent the ``arch``
specification and run 64-bit regardless.
(That is not the case if you apply ``arch`` to a specific version
such as ``/usr/bin/python2.7``.)
To make sure of running 32-bit in all cases, set the following environment variable::

    VERSIONER_PYTHON_PREFER_32_BIT=yes
    arch -i386 /usr/bin/python pyinstaller --clean -F -w myscript.py


Getting the Opened Document Names
====================================

.. Note::

	Support for OpenDocument events is broken in |PyInstaller| 3.0
	owing to code changes needed in the bootloader to support current
	versions of Mac OS X.
	Do not attempt to use this feature until it has been fixed.
	If this feature is important to you, follow and comment on
	the status of `PyInstaller Issue #1309`_.

When a user double-clicks a document of a type your application
supports, or when a user drags a document icon and drops it
on your application's icon, Mac OS X launches your application
and provides the name(s) of the opened document(s) in the
form of an OpenDocument AppleEvent.
This AppleEvent is received by the |bootloader|
before your code has started executing.

The |bootloader| gets the names of opened documents from
the OpenDocument event and encodes them into the ``argv``
string before starting your code.
Thus your code can query ``sys.argv`` to get the names
of documents that should be opened at startup.

OpenDocument is the only AppleEvent the |bootloader| handles.
If you want to handle other events, or events that
are delivered after the program has launched, you must
set up the appropriate handlers.



.. include:: _common_definitions.txt

.. Emacs config:
 Local Variables:
 mode: rst
 ispell-local-dictionary: "american"
 End:

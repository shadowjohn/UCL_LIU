#-----------------------------------------------------------------------------
# Copyright (c) 2005-2018, PyInstaller Development Team.
#
# Distributed under the terms of the GNU General Public License with exception
# for distributing bootloader.
#
# The full license is in the file COPYING.txt, distributed with this software.
#-----------------------------------------------------------------------------

# Imports
# =======
# Futures
# -------
from __future__ import print_function

# Library imports
# ---------------
import copy
import glob
import os
import pytest
import re
import subprocess
import sys
import inspect
import textwrap
import io
import shutil

# Third-party imports
# -------------------
import py
import psutil # Manages subprocess timeout.


# Set a handler for the root-logger to inhibit 'basicConfig()' (called in
# PyInstaller.log) is setting up a stream handler writing to stderr. This
# avoids log messages to be written (and captured) twice: once on stderr and
# once by pytests's caplog.
import logging
logging.getLogger().addHandler(logging.NullHandler())


# Local imports
# -------------
# Expand sys.path with PyInstaller source.
_ROOT_DIR = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
sys.path.append(_ROOT_DIR)

from PyInstaller import configure, config
from PyInstaller import __main__ as pyi_main
from PyInstaller.utils.cliutils import archive_viewer
from PyInstaller.compat import is_darwin, is_win, is_py2, safe_repr, \
    architecture, is_linux, suppress, text_read_mode
from PyInstaller.depend.analysis import initialize_modgraph
from PyInstaller.utils.win32 import winutils
from PyInstaller.utils.hooks.qt import pyqt5_library_info

# Monkeypatch the psutil subprocess on Python 2
if is_py2:
    import subprocess32
    psutil.subprocess = subprocess32
    subprocess.TimeoutExpired = psutil.TimeoutExpired

# Globals
# =======
# Directory with Python scripts for functional tests. E.g. main scripts, etc.
_SCRIPT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'scripts')
# Directory with testing modules used in some tests.
_MODULES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'modules')
# Directory with .toc log files.
_LOGS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs')
# Directory storing test-specific data.
_DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
# Directory with .spec files used in some tests.
_SPEC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'specs')
# Timeout for running the executable. If executable does not exit in this time
# then it is interpreted as test failure.
_EXE_TIMEOUT = 30  # In sec.
# Number of retries we should attempt if the executable times out.
_MAX_RETRIES = 2

# Code
# ====
# Fixtures
# --------


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # execute all other hooks to obtain the report object
    outcome = yield
    rep = outcome.get_result()

    # set an report attribute for each phase of a call, which can
    # be "setup", "call", "teardown"

    setattr(item, "rep_" + rep.when, rep)


@pytest.fixture
def script_dir():
    return py.path.local(_SCRIPT_DIR)

# A helper function to copy from data/dir to tmpdir/data.
def _data_dir_copy(
  # The name of the subdirectory located in data/name to copy.
  subdir_name,
  # The tmpdir object for this test. See
  # https://pytest.org/latest/tmpdir.html.
  tmpdir):

    # Form the source and tmp paths.
    source_data_dir = py.path.local(_DATA_DIR).join(subdir_name)
    tmp_data_dir = tmpdir.join('data', subdir_name)
    # Copy the data.
    shutil.copytree(source_data_dir.strpath, tmp_data_dir.strpath)
    # Return the temporary data directory, so that the copied data can now be
    # used.
    return tmp_data_dir

# Define a fixure for the DataDir object.
@pytest.fixture
def data_dir(
  # The request object for this test. See
  # https://pytest.org/latest/builtin.html#_pytest.python.FixtureRequest
  # and
  # https://pytest.org/latest/fixture.html#fixtures-can-introspect-the-requesting-test-context.
  request,
  # The tmpdir object for this test. See
  # https://pytest.org/latest/tmpdir.html.
  tmpdir):

    # Strip the leading 'test_' from the test's name.
    name = request.function.__name__[5:]
    # Copy to tmpdir and return the path.
    return _data_dir_copy(name, tmpdir)

class AppBuilder(object):

    def __init__(self, tmpdir, bundle_mode, module_graph):
        self._tmpdir = tmpdir
        self._mode = bundle_mode
        self._specdir = self._tmpdir
        self._distdir = os.path.join(self._tmpdir, 'dist')
        self._builddir = os.path.join(self._tmpdir, 'build')
        self._modgraph = module_graph


    def test_spec(self, specfile, *args, **kwargs):
        """
        Test a Python script that is referenced in the supplied .spec file.
        """
        __tracebackhide__ = True
        specfile = os.path.join(_SPEC_DIR, specfile)
        # 'test_script' should handle .spec properly as script.
        return self.test_script(specfile, *args, **kwargs)


    def test_source(self, source, *args, **kwargs):
        """
        Test a Python script given as source code.

        The source will be written into a file named like the
        test-function. This file will then be passed to `test_script`.
        If you need other related file, e.g. as `.toc`-file for
        testing the content, put it at at the normal place. Just mind
        to take the basnename from the test-function's name.

        :param script: Source code to create executable from. This
                       will be saved into a temporary file which is
                       then passed on to `test_script`.

        :param test_id: Test-id for parametrized tests. If given, it
                        will be appended to the script filename,
                        separated by two underscores.

        All other arguments are passed streigth on to `test_script`.

        Ensure that the caller of `test_source` is in a UTF-8
        encoded file with the correct '# -*- coding: utf-8 -*-' marker.

        """
        __tracebackhide__ = True
        if is_py2:
            if isinstance(source, str):
                source = source.decode('UTF-8')
        testname = inspect.stack()[1][3]
        if 'test_id' in kwargs:
            # For parametrized test append the test-id.
            testname = testname + '__' + kwargs['test_id']
            del kwargs['test_id']

        # Periods are not allowed in Python module names.
        testname = testname.replace('.', '_')

        scriptfile = os.path.join(os.path.abspath(self._tmpdir),
                                  testname + '.py')
        source = textwrap.dedent(source)
        with io.open(scriptfile, 'w', encoding='utf-8') as ofh:
            print(u'# -*- coding: utf-8 -*-', file=ofh)
            print(source, file=ofh)
        return self.test_script(scriptfile, *args, **kwargs)


    def test_script(self, script, pyi_args=None, app_name=None,
                    app_args=None, runtime=None, run_from_path=False):
        """
        Main method to wrap all phases of testing a Python script.

        :param script: Name of script to create executable from.
        :param pyi_args: Additional arguments to pass to PyInstaller when creating executable.
        :param app_name: Name of the executable. This is equivalent to argument --name=APPNAME.
        :param app_args: Additional arguments to pass to
        :param runtime: Time in seconds how long to keep executable running.
        :param toc_log: List of modules that are expected to be bundled with the executable.
        """
        __tracebackhide__ = True

        def marker(line):
            # Print some marker to stdout and stderr to make it easier
            # to distinguish the phases in the CI test output.
            print('-------', line, '-------')
            print('-------', line, '-------', file=sys.stderr)

        if pyi_args is None:
            pyi_args = []
        if app_args is None:
            app_args = []

        if app_name:
            pyi_args.extend(['--name', app_name])
        else:
            # Derive name from script name.
            app_name = os.path.splitext(os.path.basename(script))[0]

        # Relative path means that a script from _script_dir is referenced.
        if not os.path.isabs(script):
            script = os.path.join(_SCRIPT_DIR, script)
        self.script = script
        assert os.path.exists(self.script), 'Script %s not found.' % script

        marker('Starting build.')
        if not self._test_building(args=pyi_args):
            pytest.fail('Building of %s failed.' % script)

        marker('Build finshed, now running executable.')
        self._test_executables(app_name, args=app_args,
                               runtime=runtime, run_from_path=run_from_path)
        marker('Running executable finished.')

    def _test_executables(self, name, args, runtime, run_from_path):
        """
        Run created executable to make sure it works.

        Multipackage-tests generate more than one exe-file and all of
        them have to be run.

        :param args: CLI options to pass to the created executable.
        :param runtime: Time in seconds how long to keep the executable running.

        :return: Exit code of the executable.
        """
        __tracebackhide__ = True
        exes = self._find_executables(name)
        # Empty list means that PyInstaller probably failed to create any executable.
        assert exes != [], 'No executable file was found.'
        for exe in exes:
            # Try to find .toc log file. .toc log file has the same basename as exe file.
            toc_log = os.path.join(_LOGS_DIR, os.path.basename(exe) + '.toc')
            if os.path.exists(toc_log):
                if not self._examine_executable(exe, toc_log):
                    pytest.fail('Matching .toc of %s failed.' % exe)
            retcode = self._run_executable(exe, args, run_from_path, runtime)
            if retcode != 0:
                pytest.fail('Running exe %s failed with return-code %s.' %
                            (exe, retcode))

    def _find_executables(self, name):
        """
        Search for all executables generated by the testcase.

        If the test-case is called e.g. 'test_multipackage1', this is
        searching for each of 'test_multipackage1.exe' and
        'multipackage1_?.exe' in both one-file- and one-dir-mode.

        :param name: Name of the executable to look for.

        :return: List of executables
        """
        exes = []
        onedir_pt = os.path.join(self._distdir, name, name)
        onefile_pt = os.path.join(self._distdir, name)
        patterns = [onedir_pt, onefile_pt,
                    # Multipackage one-dir
                    onedir_pt + '_?',
                    # Multipackage one-file
                    onefile_pt + '_?']
        # For Windows append .exe extension to patterns.
        if is_win:
            patterns = [pt + '.exe' for pt in patterns]
        # For Mac OS X append pattern for .app bundles.
        if is_darwin:
            # e.g:  ./dist/name.app/Contents/MacOS/name
            pt = os.path.join(self._distdir, name + '.app', 'Contents', 'MacOS', name)
            patterns.append(pt)
        # Apply file patterns.
        for pattern in patterns:
            for prog in glob.glob(pattern):
                if os.path.isfile(prog):
                    exes.append(prog)
        return exes

    def _run_executable(self, prog, args, run_from_path, runtime):
        """
        Run executable created by PyInstaller.

        :param args: CLI options to pass to the created executable.
        """
        # Run the test in a clean environment to make sure they're really self-contained.
        prog_env = copy.deepcopy(os.environ)
        prog_env['PATH'] = ''
        del prog_env['PATH']
        # For Windows we need to keep minimal PATH for successful running of some tests.
        if is_win:
            # Minimum Windows PATH is in most cases:   C:\Windows\system32;C:\Windows
            prog_env['PATH'] = os.pathsep.join(winutils.get_system_path())

        exe_path = prog
        if(run_from_path):
            # Run executable in the temp directory
            # Add the directory containing the executable to $PATH
            # Basically, pretend we are a shell executing the program from $PATH.
            prog_cwd = self._tmpdir
            prog_name = os.path.basename(prog)
            prog_env['PATH'] = os.pathsep.join([prog_env.get('PATH', ''), os.path.dirname(prog)])

        else:
            # Run executable in the directory where it is.
            prog_cwd = os.path.dirname(prog)
            # The executable will be called with argv[0] as relative not absolute path.
            prog_name = os.path.join(os.curdir, os.path.basename(prog))

        # Workaround to enable win_codepage_test
        # If _distdir is 'bytes', PyI build fails with ASCII decode error
        # when it joins the 'bytes' _distdir with the 'unicode' filenames from bindep and
        # winmanifest.
        #
        # PyI succeeds with _distdir as 'unicode', but subprocess
        # fails with ASCII encode error. subprocess succeeds if progname is
        # mbcs-encoded 'bytes'
        if is_win and is_py2:
            if isinstance(exe_path, unicode):
                exe_path = exe_path.encode('mbcs')
            if isinstance(prog_name, unicode):
                prog_name = prog_name.encode('mbcs')
            if isinstance(prog_cwd, unicode):
                prog_cwd = prog_cwd.encode('mbcs')

        args = [prog_name] + args
        # Using sys.stdout/sys.stderr for subprocess fixes printing messages in
        # Windows command prompt. Py.test is then able to collect stdout/sterr
        # messages and display them if a test fails.
        for _ in range(_MAX_RETRIES):
            retcode = self.__run_executable(args, exe_path, prog_env,
                                            prog_cwd, runtime)
            if retcode != 1:  # retcode == 1 means a timeout
                break
        return retcode


    def __run_executable(self, args, exe_path, prog_env, prog_cwd, runtime):
        process = psutil.Popen(args, executable=exe_path,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE,
                               env=prog_env, cwd=prog_cwd)

        def _msg(*text):
            print('[' + str(process.pid) + '] ', *text)

        # Run executable. stderr is redirected to stdout.
        _msg('RUNNING: ', safe_repr(exe_path), ', args: ', safe_repr(args))
        # 'psutil' allows to use timeout in waiting for a subprocess.
        # If not timeout was specified then it is 'None' - no timeout, just waiting.
        # Runtime is useful mostly for interactive tests.
        try:
            timeout = runtime if runtime else _EXE_TIMEOUT
            stdout, stderr = process.communicate(timeout=timeout)
            retcode = process.returncode
        except (psutil.TimeoutExpired, subprocess.TimeoutExpired):
            if runtime:
                # When 'runtime' is set then expired timeout is a good sing
                # that the executable was running successfully for a specified time.
                # TODO Is there a better way return success than 'retcode = 0'?
                retcode = 0
            else:
                # Exe is running and it is not interactive. Fail the test.
                retcode = 1
                _msg('TIMED OUT!')
            # Kill the subprocess and its child processes.
            for p in list(process.children(recursive=True)) + [process]:
                with suppress(psutil.NoSuchProcess):
                    p.kill()
            stdout, stderr = process.communicate()

        if is_py2:
            sys.stdout.write(stdout)
            sys.stderr.write(stderr)
        else:
            sys.stdout.buffer.write(stdout)
            sys.stderr.buffer.write(stderr)

        return retcode

    def _test_building(self, args):
        """
        Run building of test script.

        :param args: additional CLI options for PyInstaller.

        Return True if build succeded False otherwise.
        """
        default_args = ['--debug=bootloader', '--noupx',
                '--specpath', self._specdir,
                '--distpath', self._distdir,
                '--workpath', self._builddir,
                '--path', _MODULES_DIR,
                '--log-level=DEBUG'
                ]

        # Choose bundle mode.
        if self._mode == 'onedir':
            default_args.append('--onedir')
        elif self._mode == 'onefile':
            default_args.append('--onefile')
        # if self._mode is None then just the spec file was supplied.

        pyi_args = [self.script] + default_args + args
        # TODO fix return code in running PyInstaller programatically
        PYI_CONFIG = configure.get_config(upx_dir=None)
        # Override CACHEDIR for PyInstaller and put it into self.tmpdir
        PYI_CONFIG['cachedir'] = self._tmpdir
        # Speed up tests by reusing copy of basic module graph object.
        PYI_CONFIG['tests_modgraph'] = copy.deepcopy(self._modgraph)

        pyi_main.run(pyi_args, PYI_CONFIG)
        retcode = 0

        return retcode == 0

    def _examine_executable(self, exe, toc_log):
        """
        Compare log files (now used mostly by multipackage test_name).

        :return: True if .toc files match
        """
        print('EXECUTING MATCHING:', toc_log)
        fname_list = archive_viewer.get_archive_content(exe)
        fname_list = [fn for fn in fname_list]
        with open(toc_log, text_read_mode) as f:
            pattern_list = eval(f.read())
        # Alphabetical order of patterns.
        pattern_list.sort()
        missing = []
        for pattern in pattern_list:
            for fname in fname_list:
                if re.match(pattern, fname):
                    print('MATCH:', pattern, '-->', fname)
                    break
            else:
                # No matching entry found
                missing.append(pattern)
                print('MISSING:', pattern)

        # Not all modules matched.
        # Stop comparing other .toc files and fail the test.
        if missing:
            for m in missing:
                print('Missing', m, 'in', exe)
            return False
        # All patterns matched.
        return True


# Scope 'session' should keep the object unchanged for whole tests.
# This fixture caches basic module graph dependencies that are same
# for every executable.
@pytest.fixture(scope='session')
def pyi_modgraph():
    # Explicitly set the log level since the plugin `pytest-catchlog` (un-)
    # sets the root logger's level to NOTSET for the setup phase, which will
    # lead to TRACE messages been written out.
    import PyInstaller.log as logging
    logging.logger.setLevel(logging.DEBUG)
    return initialize_modgraph()


# Run by default test as onedir and onefile.
@pytest.fixture(params=['onedir', 'onefile'])
def pyi_builder(tmpdir, monkeypatch, request, pyi_modgraph):
    tmp = tmpdir.strpath
    # Save/restore environment variable PATH.
    monkeypatch.setenv('PATH', os.environ['PATH'], )
    # PyInstaller or a test case might manipulate 'sys.path'.
    # Reset it for every test.
    monkeypatch.syspath_prepend(None)
    # Set current working directory to
    monkeypatch.chdir(tmp)
    # Clean up configuration and force PyInstaller to do a clean configuration
    # for another app/test.
    # The value is same as the original value.
    monkeypatch.setattr('PyInstaller.config.CONF', {'pathex': []})

    yield AppBuilder(tmp, request.param, pyi_modgraph)

    if is_darwin or is_linux:
        if request.node.rep_setup.passed:
            if request.node.rep_call.passed:
                if os.path.exists(tmp):
                    shutil.rmtree(tmp)
    # Clear any PyQt5 state.
    try:
        del pyqt5_library_info.version
    except AttributeError:
        pass


# Fixture for .spec based tests.
# With .spec it does not make sense to differentiate onefile/onedir mode.
@pytest.fixture
def pyi_builder_spec(tmpdir, monkeypatch, pyi_modgraph):
    tmp = tmpdir.strpath
    # Save/restore environment variable PATH.
    monkeypatch.setenv('PATH', os.environ['PATH'], )
    # Set current working directory to
    monkeypatch.chdir(tmp)
    # PyInstaller or a test case might manipulate 'sys.path'.
    # Reset it for every test.
    monkeypatch.syspath_prepend(None)
    # Clean up configuration and force PyInstaller to do a clean configuration
    # for another app/test.
    # The value is same as the original value.
    monkeypatch.setattr('PyInstaller.config.CONF', {'pathex': []})

    return AppBuilder(tmp, None, pyi_modgraph)

# Define a fixture which compiles the data/load_dll_using_ctypes/ctypes_dylib.c
# program in the tmpdir, returning the tmpdir object.
@pytest.fixture()
def compiled_dylib(tmpdir):
    tmp_data_dir = _data_dir_copy('ctypes_dylib', tmpdir)

    # Compile the ctypes_dylib in the tmpdir: Make tmpdir/data the CWD. Don't
    # use monkeypatch.chdir to change, then monkeypatch.undo() to restore the
    # CWD, since this will undo ALL monkeypatches (such as the pyi_builder's
    # additions to sys.path), breaking the test.
    old_wd = tmp_data_dir.chdir()
    try:
        if is_win:
            tmp_data_dir = tmp_data_dir.join('ctypes_dylib.dll')
            # For Mingw-x64 we must pass '-m32' to build 32-bit binaries
            march = '-m32' if architecture() == '32bit' else '-m64'
            ret = subprocess.call('gcc -shared ' + march + ' ctypes_dylib.c -o ctypes_dylib.dll', shell=True)
            if ret != 0:
                # Find path to cl.exe file.
                from distutils.msvccompiler import MSVCCompiler
                comp = MSVCCompiler()
                comp.initialize()
                cl_path = comp.cc
                # Fallback to msvc.
                ret = subprocess.call([cl_path, '/LD', 'ctypes_dylib.c'], shell=False)
        elif is_darwin:
            tmp_data_dir = tmp_data_dir.join('ctypes_dylib.dylib')
            # On Mac OS X we need to detect architecture - 32 bit or 64 bit.
            arch = 'i386' if architecture() == '32bit' else 'x86_64'
            cmd = ('gcc -arch ' + arch + ' -Wall -dynamiclib '
                'ctypes_dylib.c -o ctypes_dylib.dylib -headerpad_max_install_names')
            ret = subprocess.call(cmd, shell=True)
            id_dylib = os.path.abspath('ctypes_dylib.dylib')
            ret = subprocess.call('install_name_tool -id %s ctypes_dylib.dylib' % (id_dylib,), shell=True)
        else:
            tmp_data_dir = tmp_data_dir.join('ctypes_dylib.so')
            ret = subprocess.call('gcc -fPIC -shared ctypes_dylib.c -o ctypes_dylib.so', shell=True)
        assert ret == 0, 'Compile ctypes_dylib failed.'
    finally:
        # Reset the CWD directory.
        old_wd.chdir()

    return tmp_data_dir

#!/usr/local/bin/python3
__author__ = 'apaeffgen'
# -*- coding: utf-8 -*-

    # This file is part of Panconvert.
    #
    # Panconvert is free software: you can redistribute it and/or modify
    # it under the terms of the GNU General Public License as published by
    # the Free Software Foundation, either version 3 of the License, or
    # (at your option) any later version.
    #
    # Panconvert is distributed in the hope that it will be useful,
    # but WITHOUT ANY WARRANTY; without even the implied warranty of
    # MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    # GNU General Public License for more details.
    #
    # You should have received a copy of the GNU General Public License
    # along with Panconvert.  If not, see <http://www.gnu.org/licenses/>.

import os, shutil, io, sys
import platform
import subprocess
from PyQt6.QtCore import QSettings
from source.language.messages import *


global fromFormat, path_pandoc

# Module-level path_pandoc - lazily initialized via get_path_pandoc()
path_pandoc = ''


def _get_settings():
    """Lazy QSettings getter - avoids module-level instantiation."""
    return QSettings('Pandoc', 'PanConvert')

def get_path_pandoc():

    settings = _get_settings()
    path_pandoc_tmp = settings.value('path_pandoc','')
    path_pandoc = str(path_pandoc_tmp)

    if not os.path.isfile(path_pandoc):

        try:
            if getattr(sys, 'frozen', False):
                # In a bundled app, shutil.which may not see the full system PATH
                # because PyInstaller modifies the environment. Use multiple strategies:

                # Strategy 1: Check common macOS/Unix locations where pandoc is installed
                common_paths = [
                    '/usr/local/bin/pandoc',   # macOS .pkg installer, Homebrew on Intel
                    '/opt/homebrew/bin/pandoc', # Homebrew on Apple Silicon
                    '/opt/local/bin/pandoc',    # MacPorts
                    '/usr/bin/pandoc',          # System default (rare)
                ]
                for p in common_paths:
                    if os.path.isfile(p):
                        path_pandoc = p
                        break

                # Strategy 2: If not found in common paths, try 'which' with explicit PATH
                if not os.path.isfile(path_pandoc):
                    if platform.system() == 'Darwin' or os.name == 'posix':
                        # Build a comprehensive PATH that includes common locations
                        user_path = os.environ.get('PATH', '')
                        # Add common paths that might be missing from subprocess env
                        extra_paths = ['/usr/local/bin', '/opt/homebrew/bin', '/opt/local/bin',
                                       '/usr/bin', '/bin', '/usr/sbin', '/sbin']
                        # Merge: user PATH + extra paths not already in user PATH
                        existing = set(user_path.split(':')) if user_path else set()
                        for ep in extra_paths:
                            if ep not in existing:
                                user_path = user_path + ':' + ep if user_path else ep
                        env = os.environ.copy()
                        env['PATH'] = user_path
                        p_proc = subprocess.Popen(
                            ['which', 'pandoc'],
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            env=env)
                        stdout, _ = p_proc.communicate()
                        found = stdout.decode('utf-8').strip()
                        if found and os.path.isfile(found):
                            path_pandoc = found
                    else:
                        # Windows: use 'where' command
                        p_proc = subprocess.Popen(
                            ['where', 'pandoc'],
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
                        stdout, _ = p_proc.communicate()
                        found = stdout.decode('utf-8').strip().split('\n')[-1].strip()
                        if found and os.path.isfile(found):
                            path_pandoc = found

                if path_pandoc and os.path.isfile(path_pandoc):
                    settings.setValue('path_pandoc', path_pandoc)
                    settings.sync()
                else:
                    raise FileNotFoundError("pandoc not found")
            else:
                # Normal (non-bundled) mode: use shutil.which
                if platform.system() == 'Darwin' or os.name == 'posix':
                    path_pandoc = which("pandoc")
                else:
                    path_pandoc = where("pandoc.exe")
                settings.setValue('path_pandoc', path_pandoc)
                settings.sync()
        except FileNotFoundError:
            path_pandoc = ''
            settings.setValue('path_pandoc', path_pandoc)
            settings.sync()

    return path_pandoc


def get_path_multimarkdown():
    settings = _get_settings()
    path_multimarkdown = settings.value('path_multimarkdown','')

    if getattr( sys, 'frozen', False ):
            if platform.system() == 'Darwin' or os.name == 'posix':
                path_multimarkdown = which("multimarkdown")
                settings.setValue('path_multimarkdown', path_multimarkdown)
                settings.sync()
            else:
                args = ['where', 'multimarkdown']
                p = subprocess.Popen(
                    args,
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE)

                path_multimarkdown = p.communicate(path_multimarkdown.encode('utf-8'))[0].decode('utf-8').rstrip()
                settings.setValue('path_multimarkdown', path_multimarkdown)
                settings.sync()
                return path_multimarkdown
    else:

        if platform.system() == 'Darwin' or os.name == 'posix':
            args = ['which', 'multimarkdown']
            p = subprocess.Popen(
                args,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE)

            path_multimarkdown = p.communicate(path_multimarkdown.encode('utf-8'))[0].decode('utf-8').rstrip()
            settings.setValue('path_multimarkdown', path_multimarkdown)
            settings.sync()
            return path_multimarkdown

        elif platform.system() == 'Windows':
            args = ['where', 'multimarkdown']
            p = subprocess.Popen(
                args,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE)

            path_multimarkdown = p.communicate(path_multimarkdown.encode('utf-8'))[0].decode('utf-8').rstrip()
            settings.setValue('path_multimarkdown', path_multimarkdown)
            settings.sync()
            return path_multimarkdown


def get_pandoc_version():

    settings = _get_settings()
    path_pandoc = settings.value('path_pandoc','')

    if os.path.isfile(path_pandoc):

        p = subprocess.Popen(
            [path_pandoc, '-v'],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE)
        output = p.communicate()[0].decode().splitlines(False)
        versionstr = output[0]

        # Extract major version number (handles pandoc 2.x and 3.x)
        # Examples: "pandoc 2.11.4", "pandoc 3.10.1"
        import re
        match = re.search(r'pandoc\s+(\d+)', versionstr)
        if match:
            version = int(match.group(1))
        else:
            version = 0

    return version



def get_pandoc_formats():
    """
    Dynamic preprocessor for Pandoc formats.
    Return 2 lists. "from_formats" and "to_formats".
    """
    settings = _get_settings()
    path_pandoc = settings.value('path_pandoc','')

    if not os.path.isfile(path_pandoc):
        path_pandoc = get_path_pandoc()
        path_pandoc = settings.value('path_pandoc','')
        if not os.path.isfile(path_pandoc):
            message = error_converter_path()
            print(message)
            return None, None

    if os.path.isfile(path_pandoc):

        version = get_pandoc_version()

        # Pandoc >= 2.18 supports --list-input-formats / --list-output-formats
        # version is now the MAJOR version number (2, 3, etc.)
        if version < 2:

                p = subprocess.Popen(
                    [path_pandoc, '-h'],
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE)
                help_text = p.communicate()[0].decode().splitlines(False)
                txt = ' '.join(help_text[1:help_text.index('Options:')])


                aux = txt.split('Output formats: ')
                in_ = aux[0].split('Input formats: ')[1].split(',')
                out = aux[1].split(',')

                return [f.strip() for f in in_], [f.strip() for f in out]


        else:

            p = subprocess.Popen(
                [path_pandoc, '--list-input-formats'],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE)
            inputformats = p.communicate()[0].decode().splitlines(False)


            p = subprocess.Popen(
                [path_pandoc, '--list-output-formats'],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE)
            outputformats = p.communicate()[0].decode().splitlines(False)

            in_ = inputformats
            out = outputformats

            return [f.strip() for f in in_], [f.strip() for f in out]


def get_pandoc_options():
    """
    Get the Options of the Pandoc help section
    """
    settings = _get_settings()
    path_pandoc = settings.value('path_pandoc','')

    if not os.path.isfile(path_pandoc):
        path_pandoc = get_path_pandoc()
        path_pandoc = settings.value('path_pandoc','')
        if not os.path.isfile(path_pandoc):
            message = error_converter_path()
            print(message)
            return None

    if os.path.isfile(path_pandoc):

        version = get_pandoc_version()

        if version < 1.18:

            p = subprocess.Popen(
                    [path_pandoc, '-h'],
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE)
            help_text = p.communicate()[0].decode().splitlines(True)


            aux = help_text[15:89]

            return aux


        else:

            p = subprocess.Popen(
                    [path_pandoc, '-h'],
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE)
            help_text = p.communicate()[0].decode().splitlines(True)
            aux = help_text

            return aux

def which(target):
    """Search for an executable in the system PATH.

    Raises:
        FileNotFoundError: If the executable is not found in PATH.
    """
    result = shutil.which(target)
    if result is None:
        raise FileNotFoundError(f"Executable '{target}' not found in system PATH")
    return result


def where(target):
    """Search for an executable in the system PATH (Windows alias).

    Raises:
        FileNotFoundError: If the executable is not found in PATH.
    """
    result = shutil.which(target)
    if result is None:
        raise FileNotFoundError(f"Executable '{target}' not found in system PATH")
    return result




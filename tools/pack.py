# -*- coding: utf-8 -*-
#
# Copyright (C) 2019-2023 Xpp521
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
"""
Packing tool.

Require packages: pip、twine、wheel.
"""
from shutil import rmtree
from subprocess import Popen, PIPE
from os import chdir, getcwd, listdir
from os.path import exists, join, pardir
from sys import argv, executable, exec_prefix, platform

# Main package name
PACKAGE_NAME = 'PyHotKey'


def load_info(path):
    """Load module info."""
    info = {}
    with open(path) as f:
        for line in f:
            if line.startswith('#'):
                continue
            data = line.strip().replace(' ', '').replace("'", '').split('=')
            if 2 == len(data):
                info[data[0]] = data[1]
    return info


def exec_cmd(*args):
    """
    Executes a command.
    :param args: the command.
    :return: stdout of the command.
    :raises: RuntimeError.
    """
    res = Popen(args, stdout=PIPE, stderr=PIPE)
    stdout, stderr = res.communicate()
    if 0 != res.returncode:
        raise RuntimeError('Failed to execute <{}> ({}): {}'.format(args, res.returncode, stderr.decode('gbk')))
    else:
        return stdout.decode('gbk')


# Load "pip" and "twine"
if 'win32' == platform:         # Windows
    PIP = join(exec_prefix, 'Scripts', 'pip.exe')
    TWINE = join(exec_prefix, 'Scripts', 'twine.exe')
elif 'darwin' == platform:      # Mac OS
    PIP = join(exec_prefix, 'bin', 'pip')
    TWINE = join(exec_prefix, 'bin', 'twine')
    # TWINE = r'/Users/xpp/.local/bin/twine'
else:                           # Linux
    PIP = join(exec_prefix, 'bin', 'pip')
    TWINE = join(exec_prefix, 'bin', 'twine')
if not exists(PIP):
    raise ModuleNotFoundError("No module named 'pip'")
if not exists(TWINE):
    raise ModuleNotFoundError("No module named 'twine'")
chdir(pardir)
ROOT = getcwd()
INFO = load_info(join(ROOT, PACKAGE_NAME, '_info.py'))


def clean():
    """Clean up old versions."""
    paths = [join(ROOT, 'build'), join(ROOT, 'dist'),
             join(ROOT, '{}.egg-info'.format(INFO.get('NAME')))]
    for path in paths:
        print('Cleaning directory: {}'.format(path))
        try:
            rmtree(path)
        except FileNotFoundError:
            continue
    print()


def pack():
    """Pack a new release."""
    print(exec_cmd(executable, join(ROOT, 'setup.py'), 'sdist', 'bdist_wheel'))


def check():
    """Check the new release."""
    print(exec_cmd(TWINE, 'check', join(ROOT, 'dist', '*')))


def upload():
    """Upload the new release to PYPI."""
    # Encoding error ↓↓↓, consider using os.popen...
    print(exec_cmd(TWINE, 'upload', join(ROOT, 'dist', '*')))


def install():
    """Install the current version."""
    wheel = ''
    for p in listdir(join(ROOT, 'dist')):
        if p.startswith('{}-{}'.format(INFO.get('NAME'), INFO.get('VERSION'))) and p.endswith('.whl'):
            wheel = join(ROOT, 'dist', p)
            break
    if wheel:
        print(exec_cmd(PIP, 'uninstall', '-y', INFO.get('NAME')))
        print(exec_cmd(PIP, 'install', wheel))
    else:
        print('No wheel file found...')


def main():
    note = '''\n\t\tPacking tool
————————————————————————————>
Command:
    \tc:\t\tClean up old version.

    \tp:\t\tPackage new version.

    \ti:\t\tInstall current version.
    '''
    if 2 != len(argv):
        print(note)
        return
    ch = argv[1]
    if 'c' == ch:
        clean()
    elif 'p' == ch:
        clean()
        pack()
        check()
    elif 'i' == ch:
        install()
    # elif 'u' == ch:
    #     if 'y' == input('Upload to PYPI (y/n)? '):
    #         upload()
    else:
        print(note)


if __name__ == '__main__':
    main()

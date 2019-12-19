# -*- coding: utf-8 -*-
# PyHotKey
# Copyright (C) 2019 Xpp521
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
You need to move the script to the root directory before using it.
"""
from os import listdir
from shutil import rmtree, move
from subprocess import Popen, PIPE
from sys import executable, exec_prefix
from os.path import join, isdir, exists, dirname


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


# The current directory
CUR_DIR = dirname(__file__)

# The root directory
ROOT = CUR_DIR

# The path of twine.exe.
# If it does not exist, try installing it with pip or easy_install.
TWINE = join(exec_prefix, 'Scripts', 'twine.exe')
if not exists(TWINE):
    pip = join(exec_prefix, 'Scripts', 'pip.exe')
    easy_install = join(exec_prefix, 'Scripts', 'easy_install.exe')
    if exists(pip):
        exec_cmd(pip, 'install', 'twine')
    elif exists(easy_install):
        exec_cmd(easy_install, 'twine')
    else:
        raise ModuleNotFoundError('Please install "twine".')

# Load the main package name
with open(join(ROOT, 'setup.py')) as f:
    for line in f.readlines():
        if line.startswith('MAIN_PACKAGE_NAME'):
            line = line.strip().replace(' ', '').replace('"', '').replace("'", '')
            MAIN_PACKAGE_NAME = line.split('=')[-1]
            break


def clean():
    """
    Clean up old versions.
    """
    paths = [join(ROOT, 'build'), join(ROOT, 'dist'),
             join(ROOT, '{}.egg-info'.format(MAIN_PACKAGE_NAME))]
    for path in paths:
        print('Cleaning directory: {}'.format(path))
        try:
            rmtree(path)
        except FileNotFoundError:
            continue


def pack():
    """
    Pack a new release.
    """
    print(exec_cmd(executable, join(ROOT, 'setup.py'), 'sdist', 'bdist_wheel'))
    for p in listdir(CUR_DIR):
        if isdir(p):
            move(join(CUR_DIR, p), join(ROOT, p))


def check():
    """
    Check the new release.
    """
    print(exec_cmd(TWINE, 'check', join(ROOT, 'dist', '*')))


def upload():
    """
    Upload the new release to PYPI.
    """
    print(exec_cmd(TWINE, 'upload', join(ROOT, 'dist', '*')))


def main():
    clean()
    pack()
    check()
    if 'y' == input('Upload to PYPI (y/n)? ').strip():
        upload()
    input('Script end...')


if __name__ == '__main__':
    main()

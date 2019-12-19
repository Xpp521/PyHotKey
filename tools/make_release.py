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
from os import listdir
from shutil import rmtree, move
from subprocess import Popen, PIPE
from sys import executable, exec_prefix
from os.path import join, dirname, isdir, pardir


# The current directory
CUR_DIR = dirname(__file__)

# The root directory
ROOT = join(CUR_DIR, pardir)

# The path of twine.exe
TWINE = join(exec_prefix, 'Scripts', 'twine.exe')

# Load main package name
with open(join(ROOT, 'setup.py')) as f:
    for line in f.readlines():
        if line.startswith('MAIN_PACKAGE_NAME'):
            line = line.strip().replace(' ', '').replace('"', '').replace("'", '')
            MAIN_PACKAGE_NAME = line.split('=')[-1]
            break


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
        raise RuntimeError('Failed to execute <{}> ({}): {}'.format(args, res.returncode, stderr))
    else:
        return stdout.decode('utf8')


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


if __name__ == '__main__':
    clean()
    pack()
    check()
    c = input('Upload to PYPI (y/n)? ').strip()
    if 'y' == c:
        upload()
    input('Script end...')

# -*- coding: utf-8 -*-
# @Time    : 2019/11/15 17:24
# @Author  : Xpp
# @Email   : Xpp233@foxmail.com
from os import listdir
from shutil import rmtree, move
from subprocess import Popen, PIPE
from sys import executable, exec_prefix
from os.path import join, dirname, isdir


# The current directory
CUR_DIR = dirname(__file__)

# The root directory
ROOT = dirname(CUR_DIR)

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
    print(exec_cmd(executable, join(ROOT, 'setup.py'), 'sdist', 'bdist_wheel', '--universal'))
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

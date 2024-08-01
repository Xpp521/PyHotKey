# -*- coding: utf-8 -*-
# @Time    : 2024/08/01 13:00
# @Author  : Xpp
# @GitHub  : github.com/Xpp521
# @Email   : Xpp233@foxmail.com
from sys import path
from time import sleep
from os.path import pardir
path.append(pardir)
from typing import Union, Callable
from PyHotKey import Key, keyboard


def change_function(key: Union[Key, str], on_press: Union[bool, int],
                    func: Callable, *args, **kwargs):
    """Change the function of a certain key."""
    if on_press:
        keyboard.set_magickey_on_press(key, func, *args, **kwargs)
    else:
        keyboard.set_magickey_on_release(key, func, *args, **kwargs)


def block_key(key: Union[Key, str]):
    """Block a certain key."""
    keyboard.set_magickey_on_press(key, lambda: print('【Press blocked】{}'.format(key)))
    keyboard.set_magickey_on_release(key, lambda: print('【Release blocked】{}'.format(key)))


def main():
    keyboard.suppress_magickey = 1
    block_key(Key.cmd_l)
    change_function('a', 1, lambda: print('my function'))
    print('Start————————————————————————————>')
    sleep(233)


if __name__ == '__main__':
    main()
    # input()

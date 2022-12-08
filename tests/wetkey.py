# -*- coding: utf-8 -*-
# @Time    : 2022/12/8 0:53
# @Author  : Xpp
# @GitHub  : github.com/Xpp521
# @Email   : Xpp233@foxmail.com
from sys import path
from time import sleep
from os.path import pardir
path.append(pardir)
from PyHotKey import Key, keyboard_manager


def print_info(key, pressed):
    print('{} is {}.'.format(key, 'pressed' if pressed else 'released'))


def main():
    keyboard_manager.logger = True
    # keyboard_manager.set_log_file('Test_Wetkey.log')
    keyboard_manager.set_wetkey_on_press(Key.ctrl_l, print_info, Key.ctrl_l, 1)
    keyboard_manager.set_wetkey_on_release(Key.ctrl_l, print_info, Key.ctrl_l, 0)
    keyboard_manager.register_hotkey([Key.ctrl_l, Key.alt_l, 'z'], None, lambda: print(2333333))
    keyboard_manager.register_hotkey([Key.ctrl_l], 2, lambda: print('Double tap————————————>>'))
    n = 0
    while True:
        sleep(3)
        n += 1
        # print(n)


if __name__ == '__main__':
    main()
    # input()

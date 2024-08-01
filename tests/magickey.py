# -*- coding: utf-8 -*-
# @Time    : 2022/12/8 0:53
# @Author  : Xpp
# @GitHub  : github.com/Xpp521
# @Email   : Xpp233@foxmail.com
from sys import path
from time import sleep
from os.path import pardir

path.append(pardir)
from PyHotKey import Key, keyboard


def print_info(key, pressed):
    print('{} is {}.'.format(key, 'pressed' if pressed else 'released'))


def main():
    keyboard.toggle_logger(1)
    # keyboard_manager.set_log_file('Test_magickey.log')
    keyboard.suppress_magickey = 1
    keyboard.set_magickey_on_press(Key.ctrl_l, print_info, Key.ctrl_l, 1)
    # keyboard.set_magickey_on_release(Key.ctrl_l, print_info, Key.ctrl_l, 0)
    # keyboard.set_magickey_on_press(Key.caps_lock, print_info, 'caps_lock', 1)
    keyboard.set_magickey_on_release(Key.cmd_l,lambda: print('【Win】Blocked~!'))
    # keyboard.set_magickey_on_press(Key.num_lock,lambda: print('【Num_Lock】Blocked~!'))
    # keyboard.set_magickey_on_press(Key.media_play_pause,lambda: print('【Num_Lock】Blocked~!'))
    # keyboard.register_hotkey([Key.alt_l, Key.tab], None, lambda: print('Alt + Tab'))
    # keyboard.register_hotkey([Key.ctrl_l, 'z'], None, lambda: print('Ctrl + Z'))
    # keyboard.register_hotkey([Key.ctrl_l], 2, lambda: print('Double tap————————————>>'))
    # keyboard.register_hotkey([Key.ctrl_l, Key.alt_l], None, lambda: print('ctrl - alt'))
    print(keyboard.magickeys)
    n = 0
    while True:
        sleep(3)
        n += 1
        # print(n)


if __name__ == '__main__':
    main()
    # input()

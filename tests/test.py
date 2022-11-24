from time import sleep
from os.path import join
from PyHotKey import Key, keyboard_manager as manager
# from pynput.keyboard import Key, Controller


def func(li):
    print(23333333333333333333333)
    li.append(233)
    print(li)


def hotkey():
    l = []
    x, y = 4, 3
    manager.logger = True
    manager.ttl = 2
    key_id1 = manager.register_hotkey(lambda: print(233), ['Z', Key.shift_l])
    key_id2 = manager.register_hotkey(lambda x: print('【X】{}'.format(x)), [Key.ctrl_l], 3, 777)
    print(manager.hotkeys)
    # manager.start_recording_hotkey_single(lambda k: print(k))
    n = 0
    while True:
        if 1 == n:
            x = 230
            with manager.pressed(Key.shift) as r:
                print(r)
                manager.press('Z')
            print('————————————————————————End——————————————————————')
            # break
            # manager.press('z')
            # manager.press(Key.ctrl_l)
            # manager.press(Key.alt_l)
            # manager.RegisterHotKey(func, [Key.caps_lock])
            # manager.setLogPath(join('log', 'log.txt'))
            # manager.logger = False
            # manager.UnregisterHotKey(key_id)
        # print('loop: {}, running: {}'.format(n, manager.running))
        n += 1
        sleep(3)


if __name__ == '__main__':
    hotkey()
    # input()

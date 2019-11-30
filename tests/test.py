from time import sleep
from os.path import join
from PyHotKey import manager, Key


def func(li):
    # print(23333333333333333333333)
    li.append(233)
    print(li)


if __name__ == '__main__':
    l = []
    x, y = 4, 3
    manager.logger = True
    key_id1 = manager.RegisterHotKey(func, [1, Key.ctrl_l, Key.alt_l], 2, 0.5)
    key_id2 = manager.RegisterHotKey(func, ['z', Key.ctrl_l, Key.alt_l], 2, 0.5)
    print(manager.hot_keys)
    print(key_id2)
    n = 0
    while True:
        if 3 == n:
            x = 230
            manager.RegisterHotKey(func, [Key.caps_lock])
            manager.setLogPath(join('log', 'log.txt'))
            # manager.logger = False
            # manager.UnregisterHotKey(key_id)
        print('loop: {}'.format(n))
        n += 1
        sleep(3)

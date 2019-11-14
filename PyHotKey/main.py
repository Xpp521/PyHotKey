# -*- coding: utf-8 -*-
# @Time    : 2019/11/14 15:16
# @Author  : Xpp
# @Email   : Xpp233@foxmail.com
from time import time
from enum import IntEnum
from pynput.keyboard import Listener, Key, KeyCode


class HotKeyType(IntEnum):
    # single key
    SINGLE = 1
    # multiple keys
    MULTIPLE = 2


class HotKey:
    def __init__(self, _id, trigger, keys, count=2, interval=0.5, *args, **kwargs):
        if callable(trigger):
            self.__trigger = trigger
        else:
            raise TypeError('Wrong type, "trigger" must be a function.')
        if not isinstance(keys, (list, set)):
            raise TypeError('Wrong type, "keys" must be a list, '
                            'and the type of its element must be "PyHotKey.Key", int or char.')
        if isinstance(keys, list):
            keys = set(keys)
        try:
            self.__keys = [key if isinstance(key, Key) else KeyCode(char=key[0]) for key in keys]
        except Exception:
            raise TypeError('Wrong type, "keys" must be a list, '
                            'and the type of its element must be "pynput.keyboard.Key", int or char.')
        if not self.__keys:
            raise ValueError('Wrong value, "keys" must be a Non empty list.')
        self.__type = HotKeyType.SINGLE if 1 == len(self.__keys) else HotKeyType.MULTIPLE
        if HotKeyType.SINGLE == self.__type:
            if isinstance(count, int) and 0 < count:
                self.__count = count
            else:
                raise ValueError('Invalid value, "count" must be a positive integer.')
            if isinstance(interval, float) and 0 < interval < 1:
                self.__interval = interval
            else:
                raise ValueError('Invalid value, "interval" must be between 0 and 1.')
        else:
            self.__count = 2
            self.__interval = 0.5
        self.__id = _id
        self.__args = args
        self.__kwargs = kwargs

    def __eq__(self, o):
        if isinstance(o, self.__class__):
            return self.__id == o.id
        return False

    def __repr__(self):
        return '<HotKey id: {} keys: ({})>'.format(self.__id, ','.join([repr(key) for key in self.__keys]))

    def trigger(self):
        return self.__trigger(*self.__args, **self.__kwargs)

    @property
    def id(self):
        return self.__id

    @property
    def type(self):
        return self.__type

    @property
    def keys(self):
        return self.__keys

    @property
    def count(self):
        return self.__count

    @property
    def interval(self):
        return self.__interval


class HotKeyManager:
    def __init__(self):
        self.__id = 1
        self.__hot_keys = []
        self.__pressed_keys = []
        self.__released_keys = []
        self.__listener = Listener(on_press=self.__on_press, on_release=self.__on_release)

    def RegisterHotKey(self, trigger, keys, count=2, interval=0.5, *args, **kwargs):
        """
        :param trigger: the function called when hot key is triggered.
        :param list keys: key list.
        :param int count: the press times of hot key. Only for single type hot key.
        :param float interval: the interval time between presses, unit: second. Only for single type hot key.
        :param args: the arguments of trigger.
        :param kwargs: the keyword arguments of trigger.
        :return: if successful, return id, else return -1. You can use this id to unregister hot key.
        :rtype: int.
        """
        keys = set(keys)
        if any([key.keys == keys for key in self.__hot_keys]):
            return -1
        try:
            hot_key = HotKey(self.__id, trigger, keys, count, interval, *args, **kwargs)
        except (TypeError, ValueError):
            return -1
        self.__hot_keys.append(hot_key)
        self.__id += 1
        return self.__id - 1

    def UnregisterHotKey(self, key_id):
        """
        :param key_id: the id of the hot key you want to unregister.
        :rtype: bool.
        """
        for key in self.__hot_keys:
            if key_id == key.id:
                self.__hot_keys.remove(key)
                return True
        return False

    @staticmethod
    def __exec_trigger(hot_key):
        try:
            return hot_key.trigger()
        except Exception as e:
            print('Exception in {}:\n{}: {}\n'.format(hot_key, type(e), e))

    def __on_press(self, key):
        if key in self.__pressed_keys:
            return
        self.__pressed_keys.append(key)
        print('【pressed】{}'.format(key))
        for hot_key in self.__hot_keys:
            if HotKeyType.MULTIPLE == hot_key.type and all([key in self.__pressed_keys for key in hot_key.keys]):
                self.__exec_trigger(hot_key)

    def __on_release(self, key):
        self.__pressed_keys.remove(key)
        print('【released】{}'.format(key))
        for k in self.__hot_keys:
            if HotKeyType.SINGLE == k.type and key in k.keys:
                hot_key = k
                break
        else:
            return
        cur_time = time()
        if self.__released_keys:
            for rk in reversed(self.__released_keys):
                if key == rk.get('key') and hot_key.interval < cur_time - rk.get('time'):
                    self.__released_keys = [rk for rk in self.__released_keys if key != rk.get('key')]
                    break
        self.__released_keys.append({'key': key, 'time': cur_time})
        n = 0
        for rk in self.__released_keys:
            if key == rk.get('key'):
                n += 1
        if hot_key.count == n:
            self.__released_keys = [rk for rk in self.__released_keys if key != rk.get('key')]
            self.__exec_trigger(hot_key)

    @property
    def suppress(self):
        return self.__listener.suppress

    @property
    def running(self):
        return self.__listener.running

    def wait(self):
        self.__listener.wait()

    def start(self):
        self.__listener.start()

    def stop(self):
        self.__listener.stop()

    def join(self):
        self.__listener.join()

    @property
    def hot_keys(self):
        return self.__hot_keys

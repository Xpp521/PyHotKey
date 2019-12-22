# -*- coding: utf-8 -*-
#
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
from time import time
from .hot_key import HotKey
from pynput.keyboard import Listener
from logging import getLogger, DEBUG, WARNING, StreamHandler, FileHandler, Formatter


class HotKeyManager:
    def __init__(self):
        self.__id = 1
        self.__hot_keys = []
        self.__pressed_keys = []
        self.__released_keys = []
        self.__logger = getLogger('{}.{}'.format(self.__class__.__module__, self.__class__.__name__))
        self.__cur_file_handler = ''
        self.__formatter = Formatter('[%(asctime)s]%(message)s')
        stream_handler = StreamHandler()
        stream_handler.setFormatter(self.__formatter)
        self.__logger.addHandler(stream_handler)
        self.logger = False
        self.__listener = Listener(on_press=self.__on_press, on_release=self.__on_release)

    @property
    def logger(self):
        return False if DEBUG > self.__logger.level else True

    @logger.setter
    def logger(self, value):
        if value:
            self.__logger.setLevel(DEBUG)
            if 1 == len(self.__logger.handlers):
                self.setLogPath('{}.log'.format(self.__class__.__module__.split('.')[0]))
        else:
            self.__logger.setLevel(WARNING)

    def setLogPath(self, path):
        """
        Set the log path.
        :rtype: bool.
        """
        try:
            file_handler = FileHandler(path, encoding='utf8')
        except FileNotFoundError:
            return False
        file_handler.setFormatter(self.__formatter)
        if 1 < len(self.__logger.handlers):
            self.__logger.removeHandler(self.__cur_file_handler)
        self.__logger.addHandler(file_handler)
        self.__cur_file_handler = file_handler
        return True

    def RegisterHotKey(self, trigger, keys, count=2, interval=0.5, *args, **kwargs):
        """
        :param trigger: the function invoked when the hot key is triggered.
        :param list keys: the key list.
        :param int count: the number of repeated keystrokes.
        :param float interval: the interval time between each keystroke, unit: second.
        :param args: the arguments of trigger.
        :param kwargs: the keyword arguments of trigger.
        :return: returns a key id if successful; otherwise returns -1.
        """
        keys = set(keys)
        if any([key.keys == keys for key in self.__hot_keys]):
            self.__logger.info('【Register failed】{}: This hot key has been registered'.format(keys))
            return -1
        try:
            hot_key = HotKey(self.__id, trigger, keys, count, interval, *args, **kwargs)
        except Exception as e:
            e_type = str(type(e))
            self.__logger.info('''【Register failed】{}:
{}: {}'''.format(keys, e_type[e_type.find("'") + 1: e_type.rfind("'")], e))
            return -1
        self.__hot_keys.append(hot_key)
        self.__id += 1
        self.__logger.info('【Register succeed】{}'.format(hot_key))
        return self.__id - 1

    def UnregisterHotKey(self, key_id):
        """
        :param key_id: the id of the hot key to be unregistered.
        :rtype: bool.
        """
        if isinstance(key_id, int) and 0 < key_id < self.__id:
            for key in self.__hot_keys:
                if key_id == key.id:
                    self.__hot_keys.remove(key)
                    self.__logger.info('【Unregister succeed】{}'.format(key))
                    return True
        self.__logger.info("【Unregister failed】the hot key id: {} doesn't exist".format(key_id))
        return False

    def __exec_trigger(self, hot_key):
        try:
            return hot_key.trigger()
        except Exception as e:
            e_type = str(type(e))
            self.__logger.error('''【Exception】in {}'s trigger function:
{}: {}'''.format(hot_key, e_type[e_type.find("'") + 1: e_type.rfind("'")], e))

    def __on_press(self, key):
        if key in self.__pressed_keys:
            return
        self.__pressed_keys.append(key)
        self.__logger.debug('【key pressed】{}'.format(key))
        for hot_key in self.__hot_keys:
            if 1 < len(hot_key.keys) and all([key in self.__pressed_keys for key in hot_key.keys]):
                self.__exec_trigger(hot_key)

    def __on_release(self, key):
        if key in self.__pressed_keys:
            self.__pressed_keys.remove(key)
        self.__logger.debug('【key released】{}'.format(key))
        for k in self.__hot_keys:
            if 1 == len(k.keys) and key in k.keys:
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
    def hotKeyList(self):
        return self.__hot_keys

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

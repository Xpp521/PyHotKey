# -*- coding: utf-8 -*-
#
# Copyright (C) 2019-2023 Xpp521
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
from contextlib import contextmanager
from ._key import Controller, Listener, WarmKey, HotKey, cold_keys
from logging import getLogger, DEBUG, WARNING, StreamHandler, FileHandler, Formatter


class KeyboardManager:
    def __init__(self):
        self.__id = 1
        self.__hotkeys = []
        self.__pressed_keys = []
        self.__released_keys = []
        self.__ttl = 5
        self.__interval = 0.5
        self.__block = True
        self.__recording_state = 0
        self.__recording_callback = None
        self.__strict_mode = True
        self.__logger = getLogger('{}.{}'.format(self.__class__.__module__, self.__class__.__name__))
        self.__cur_file_handler = ''
        self.__formatter = Formatter('[%(asctime)s]%(message)s')
        stream_handler = StreamHandler()
        stream_handler.setFormatter(self.__formatter)
        self.__logger.addHandler(stream_handler)
        self.logger = False
        self.__controller = Controller()
        self.__listener = None
        self.start()

    @property
    def logger(self):
        return DEBUG > self.__logger.level

    @logger.setter
    def logger(self, v):
        self.__logger.setLevel(DEBUG if v else WARNING)

    def set_log_file(self, path, mode='w'):
        """
        Set a file for logging.
        :param path: filepath.
        :param mode: 'w' = overwrite; 'a' = append.
        :rtype: bool.
        """
        try:
            file_handler = FileHandler(path, 'w' if 'w' != mode and 'a' != mode else mode, 'utf8')
        except FileNotFoundError:
            return False
        file_handler.setFormatter(self.__formatter)
        if 1 < len(self.__logger.handlers):
            self.__logger.removeHandler(self.__cur_file_handler)
        self.__logger.addHandler(file_handler)
        self.__cur_file_handler = file_handler
        return True

    def press(self, key):
        """Press a key"""
        if self.__recording_state:
            return
        self.__controller.press(key)

    def release(self, key):
        """Release a key"""
        if self.__recording_state:
            return
        self.__controller.release(key)

    def tap(self, key):
        """Press and release a key"""
        if self.__recording_state:
            return
        self.__controller.press(key)
        self.__controller.release(key)

    @contextmanager
    def pressed(self, *keys):
        """
        Do something while holding down some keys.
        example:

        with manager.pressed(Key.ctrl, Key.shift) as r:
            if r:
                do_something()

        :param keys: keys that need to be kept pressed.
        """
        if self.__recording_state:
            yield False
        else:
            for key in keys:
                self.__controller.press(key)
            try:
                yield True
            finally:
                for key in reversed(keys):
                    self.__controller.release(key)

    def type(self, string):
        """Type a string"""
        if self.__recording_state:
            return
        self.__controller.type(string)

    def register_hotkey(self, trigger, keys, count=2, *args, **kwargs):
        """
        :param trigger: the function invoked when the hotkey is triggered.
        :param keys: the key list or tuple.
        :param count: number of pressed times for hotkey with single key.
        :param args: the arguments of trigger function.
        :param kwargs: the keyword arguments of trigger function.
        :return: positive integer = hotkey id; 0 = Invalid parameters; -1 = the hotkey has been registered.
        """
        if not callable(trigger):
            self.__logger.info('【Register 0】"trigger" function is not callable')
            return 0
        if 1 == len(keys) and (not isinstance(count, int) or 0 >= count):
            self.__logger.info('【Register 0】"count" is not a positive integer')
            return 0
        keys = cold_keys(keys)
        length = len(keys)
        if 0 == length:
            self.__logger.info('【Register 0】Invalid key list: {}'.format(keys))
            return 0
        if any([length == len(hotkey.keys) and all([k in hotkey.keys for k in keys]) for hotkey in self.__hotkeys]):
            self.__logger.info('【Register -1】The hotkey: {} has been registered.'.format(keys))
            return -1
        hot_key = HotKey(self.__id, trigger, keys, count, *args, **kwargs)
        self.__hotkeys.append(hot_key)
        self.__id += 1
        self.__logger.info('【Register 1】{}'.format(hot_key))
        return self.__id - 1

    def unregister_hotkey_by_id(self, id_):
        """
        :param id_: the id of the hotkey to be unregistered.
        :rtype: bool.
        """
        if isinstance(id_, int) and 0 < id_ < self.__id:
            for hotkey in self.__hotkeys:
                if id_ == hotkey.id:
                    self.__hotkeys.remove(hotkey)
                    self.__logger.info('【Unregister 1】{}'.format(hotkey))
                    return True
        self.__logger.info("【Unregister 0】the hotkey id: {} doesn't exist".format(id_))
        return False

    def unregister_hotkey_by_keys(self, keys):
        """
        :param keys: the key list or tuple to be unregistered.
        :rtype: bool.
        """
        keys = cold_keys(keys)
        length = len(keys)
        if 0 == length:
            self.__logger.info('【Unregister 0】Invalid key list: {}'.format(keys))
            return False
        for hotkey in self.__hotkeys:
            if length == len(hotkey.keys) and all([k in hotkey.keys for k in keys]):
                self.__hotkeys.remove(hotkey)
                self.__logger.info('【Unregister 1】{}'.format(hotkey))
                return True
        self.__logger.info("【Unregister 0】the hotkey: {} doesn't exists".format(keys))
        return False

    def __exec_trigger(self, hot_key):
        try:
            hot_key.trigger()
        except Exception as e:
            e_type = str(type(e))
            self.__logger.error('''【Exception】in {}'s trigger function:
{}: {}'''.format(hot_key, e_type[e_type.find("'") + 1: e_type.rfind("'")], e))
        # self.__pressed_keys.clear()
        # self.__released_keys.clear()

    def __filter_darwin(self, event_type, event):
        return event

    def __filter_win32(self, msg, data):
        pass
        # if self.__block:
        #     self.__listener.suppress_event()
        # return True

    def __start_recording_hotkey(self, callback, type_):
        if self.__recording_state:
            return False
        if callable(callback):
            self.__recording_callback = callback
            self.__recording_state = type_
            self.__pressed_keys.clear()
            self.__released_keys.clear()
            return True
        return False

    def start_recording_hotkey_single(self, callback):
        """Record a single keystroke hotkey. The result will be send to the "callback" function."""
        if self.__start_recording_hotkey(callback, 1):
            self.__logger.info('【Recording started】(Single key)...')
            return True
        return False

    def start_recording_hotkey_multiple(self, callback):
        """Record a multiple keystroke hotkey. The result will be send to the "callback" function."""
        if self.__start_recording_hotkey(callback, 2):
            self.__logger.info('【Recording started】(Multiple key)...')
            return True
        return False

    def stop_recording(self):
        """Stop recording hotkey."""
        self.__recording_state = 0
        self.__pressed_keys.clear()
        self.__released_keys.clear()
        self.__logger.info('【Recording ended】')

    def __update_pressed_keys(self, key, pressed):
        t = []
        flag = False
        ts = key.timestamp
        if pressed:
            for k in self.__pressed_keys:
                if ts - k.timestamp > self.__ttl:
                    continue
                if key == k:
                    flag = True
                    continue
                t.append(k)
            t.append(key)
            self.__pressed_keys = t
        else:
            for i, k in enumerate(self.__pressed_keys):
                if key == k:
                    self.__pressed_keys.pop(i)
                    break
        return flag

    def __update_released_keys(self, key):
        t = []
        ts = key.timestamp
        for k in self.__released_keys:
            if ts - k.timestamp > self.__interval:
                continue
            elif key == k:
                key.n = k.n + 1
                continue
            t.append(k)
        t.append(key)
        self.__released_keys = t

    def __on_press(self, key):
        key = WarmKey(key)
        if 2 == self.__recording_state:
            if key in self.__pressed_keys:
                return
            self.__pressed_keys.append(key)
            # t = []
            # ts = time()
            # for k in self.__pressed_keys:
            #     if ts - k.timestamp > self.__ttl:
            #         continue
            #     t.append(k)
            # t.append(key)
            # self.__pressed_keys = t
            if 1 < len(self.__pressed_keys):
                self.__recording_callback(self.__pressed_keys)
                return
        if self.__update_pressed_keys(key, True):
            return
        if not self.__recording_state:
            self.__logger.debug('【Key down】{}'.format(key))
        length = len(self.__pressed_keys)
        for hotkey in self.__hotkeys:
            length_hotkey = len(hotkey.keys)
            if 1 == length_hotkey:
                continue
            if self.__strict_mode:
                if length_hotkey == length and all([k in self.__pressed_keys for k in hotkey.keys]):
                    self.__exec_trigger(hotkey)
                    return
            elif all([k in self.__pressed_keys for k in hotkey.keys]):
                self.__exec_trigger(hotkey)
                return

    def __on_release(self, key):
        key = WarmKey(key)
        if 1 == self.__recording_state:
            self.__recording_callback([key])
            return
        if 2 == self.__recording_state:
            self.__pressed_keys = [k for k in self.__pressed_keys if k != key]
            return
        self.__update_pressed_keys(key, False)
        self.__update_released_keys(key)
        if not self.__recording_state:
            self.__logger.debug('【Key up】{}'.format(key))
        for hotkey in self.__hotkeys:
            if 1 == len(hotkey.keys):
                for k in self.__released_keys:
                    if hotkey.keys[0] == k and hotkey.count == k.n:
                        self.__exec_trigger(hotkey)
                        return

    @property
    def pressed_keys(self):
        return self.__pressed_keys.copy()

    @property
    def hotkeys(self):
        return self.__hotkeys.copy()

    @property
    def recording(self):
        return self.__recording_state

    @property
    def strict_mode(self):
        return self.__strict_mode

    @strict_mode.setter
    def strict_mode(self, v):
        self.__strict_mode = bool(v)

    @property
    def ttl(self):
        return self.__ttl

    @ttl.setter
    def ttl(self, t):
        if isinstance(t, int) and 3 < t:
            self.__ttl = t
        else:
            self.__ttl = 5

    @property
    def interval(self):
        return self.__interval

    @interval.setter
    def interval(self, i):
        if isinstance(i, float) and 0.0 < i <= 1.0:
            self.__interval = i
        else:
            self.__interval = 0.3

    # @property
    # def suppress(self):
    #     return self.__listener.suppress

    @property
    def running(self):
        return self.__listener.running if self.__listener else False

    def start(self):
        if self.running:
            return
        self.__listener = Listener(on_press=self.__on_press, on_release=self.__on_release,
                                   win32_event_filter=self.__filter_win32,
                                   darwin_intercept=self.__filter_darwin)
        self.__listener.start()
        self.__logger.info('【Keyboard listener started】——————————————————>')

    # def wait(self):
    #     self.__listener.wait()

    def stop(self):
        self.__recording_state = 0
        self.__pressed_keys.clear()
        self.__released_keys.clear()
        self.__listener.stop()
        self.__logger.info('【Keyboard listener ended】——————————————————>')


keyboard_manager = KeyboardManager()

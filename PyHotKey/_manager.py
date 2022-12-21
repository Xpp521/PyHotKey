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
from logging import getLogger, CRITICAL, DEBUG, StreamHandler, FileHandler, Formatter
from ._key import Key, ColdKey, WarmKey, HotKey, WetKey, cold_keys, Controller, Listener, filter_name, event_filter


class KeyboardManager:
    def __init__(self):
        self.__id = 1
        self.__hotkeys = []
        self.__pressed_keys = []
        self.__released_keys = []
        self.__wetkeys = {}
        self.__ttl = 5
        self.__interval = 0.5
        self.__suppress = False
        self.__triggered = False
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
        self._listener = None
        self.start()

    # def set_log_level(self, level):
    #     self.__logger.setLevel(level)

    @property
    def logger(self):
        return DEBUG >= self.__logger.level

    @logger.setter
    def logger(self, v):
        self.__logger.setLevel(DEBUG if v else CRITICAL)

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

    def register_hotkey(self, keys, count, func, *args, **kwargs):
        """
        :param keys: the key list or tuple.
        :param count: number of pressed times for hotkey with single key.
        :param func: the function invoked when the hotkey is triggered.
        :param args: the arguments of "func".
        :param kwargs: the keyword arguments of "func".
        :return:
                positive integer = hotkey id;
                0 = invalid parameters;
                -1 = the hotkey has been registered;
                -2 = conflict with system hotkey.
        """
        if not callable(func):
            self.__logger.info('【Register hotkey 0】"func" is not callable')
            return 0
        if 1 == len(keys) and (not isinstance(count, int) or 1 >= count):
            self.__logger.info('【Register hotkey 0】"count" >= 2')
            return 0
        keys = cold_keys(keys)
        length = len(keys)
        if 0 == length:
            self.__logger.info('【Register hotkey 0】Invalid key list')
            return 0
        if any([length == len(hotkey.keys) and all([k in hotkey.keys for k in keys]) for hotkey in self.__hotkeys]):
            self.__logger.info('【Register hotkey -1】Hotkey: {} has been registered.'.format(keys))
            return -1
        hotkey = HotKey(self.__id, keys, count, func, *args, **kwargs)
        self.__hotkeys.append(hotkey)
        self.__id += 1
        self.__logger.info('【Register hotkey 1】{}'.format(hotkey))
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
                    self.__logger.info('【Unregister hotkey 1】{}'.format(hotkey))
                    return True
        self.__logger.info("【Unregister hotkey 0】the hotkey id: {} doesn't exist".format(id_))
        return False

    def unregister_hotkey_by_keys(self, keys):
        """
        :param keys: the key list or tuple to be unregistered.
        :rtype: bool.
        """
        keys = cold_keys(keys)
        length = len(keys)
        if 0 == length:
            self.__logger.info('【Unregister hotkey 0】Invalid key list: {}'.format(keys))
            return False
        for hotkey in self.__hotkeys:
            if length == len(hotkey.keys) and all([k in hotkey.keys for k in keys]):
                self.__hotkeys.remove(hotkey)
                self.__logger.info('【Unregister hotkey 1】{}'.format(hotkey))
                return True
        self.__logger.info("【Unregister hotkey 0】the hotkey: {} doesn't exists".format(keys))
        return False

    def unregister_all_hotkeys(self):
        self.__hotkeys.clear()
        self.__logger.info("【Unregister hotkey 1】all hotkeys")
        return True

    def __set_wetkey(self, key, on_press, func, *args, **kwargs):
        if not callable(func):
            self.__logger.info('【Set wetkey 0】"func" is not callable')
            return False
        key = ColdKey.from_object(key)
        if key is None:
            self.__logger.info('【Set wetkey 0】Invalid key')
            return False
        wetkey = self.__wetkeys.get(repr(key)) or WetKey(key)
        if on_press:
            wetkey.set_func_on_press(func, *args, **kwargs)
        else:
            wetkey.set_func_on_release(func, *args, **kwargs)
        self.__wetkeys[repr(key)] = wetkey
        self.__logger.info('【Set wetkey 1】{}'.format(wetkey))
        return True

    def set_wetkey_on_press(self, key, func, *args, **kwargs):
        """
        Set a wetkey for key press event.
        :param key: target key.
        :param func: the function invoked when "key" is pressed.
        :param args: the arguments of "func".
        :param kwargs: the keyword arguments of "func".
        :rtype: bool.
        """
        return self.__set_wetkey(key, 1, func, *args, **kwargs)

    def set_wetkey_on_release(self, key, func, *args, **kwargs):
        """
        Set a wetkey for key release event.
        :param key: target key.
        :param func: the function invoked when "key" is released.
        :param args: the arguments of "func".
        :param kwargs: the keyword arguments of "func".
        :rtype: bool.
        """
        return self.__set_wetkey(key, 0, func, *args, **kwargs)

    def __remove_wetkey(self, key, on_press=None):
        key = ColdKey.from_object(key)
        if key is None:
            self.__logger.info('【Remove wetkey 0】Invalid key')
            return False
        wet_key = self.__wetkeys.get(repr(key))
        if wet_key:
            if None is on_press:
                self.__wetkeys.pop(repr(key))
                self.__logger.info('【Remove wetkey 1】{}'.format(key))
            elif on_press:
                wet_key.clear_on_press()
                self.__logger.info('【Remove wetkey on press】{}'.format(key))
            else:
                wet_key.clear_on_release()
                self.__logger.info('【Remove wetkey on release】{}'.format(key))
            return True
        else:
            self.__logger.info('【Remove wetkey -1】The key: {} is not monitored'.format(key))
            return False

    def remove_wetkey(self, key):
        """
        Remove a wetkey for key press and release event.
        :param key: target key.
        :rtype: bool.
        """
        return self.__remove_wetkey(key)

    def remove_wetkey_on_press(self, key):
        """
        Remove a wetkey for key press event.
        :param key: target key.
        :rtype: bool.
        """
        return self.__remove_wetkey(key, 1)

    def remove_wetkey_on_release(self, key):
        """
        Remove a wetkey for key release event.
        :param key: target key.
        :rtype: bool.
        """
        return self.__remove_wetkey(key, 0)

    def remove_all_wetkeys(self):
        self.__wetkeys.clear()
        self.__logger.info('【Remove all wetkeys】')
        return True

    def __trigger_hotkey(self, hotkey):
        try:
            self.__logger.info('【HotKey triggered】{}'.format(hotkey))
            hotkey()
        except Exception as e:
            e_type = str(type(e))
            self.__logger.error('''【HotKey exception】 {}:
{}: {}'''.format(hotkey, e_type[e_type.find("'") + 1: e_type.rfind("'")], e))
        finally:
            self.__triggered = True
            return self.__suppress

    def __trigger_wetkey(self, wetkey, on_press):
        try:
            self.__logger.info('【WetKey triggered on {}】{}'.format('press' if on_press else 'release', wetkey.key))
            wetkey(on_press)
        except Exception as e:
            e_type = str(type(e))
            self.__logger.error('''【WetKey exception on {}】 {}:
{}: {}'''.format('press' if on_press else 'release', wetkey.key,
                 e_type[e_type.find("'") + 1: e_type.rfind("'")], e))

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

    def _on_press(self, key):
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
        if not self.__pressed_keys:
            wetkey = self.__wetkeys.get(repr(key))
            if wetkey and wetkey.on_press:
                self.__trigger_wetkey(wetkey, 1)
        if self.__update_pressed_keys(key, True):
            return self.__triggered
        self.__triggered = False
        if not self.__recording_state:
            self.__logger.debug('【Key down】{}'.format(key))
        length = len(self.__pressed_keys)
        for hotkey in self.__hotkeys:
            length_hotkey = len(hotkey.keys)
            if 1 == length_hotkey:
                continue
            if self.__strict_mode:
                if length_hotkey == length and all([k in self.__pressed_keys for k in hotkey.keys]):
                    return self.__trigger_hotkey(hotkey)
            elif all([k in self.__pressed_keys for k in hotkey.keys]):
                return self.__trigger_hotkey(hotkey)

    def _on_release(self, key):
        key = WarmKey(key)
        if 1 == self.__recording_state:
            self.__recording_callback([key])
            return
        if 2 == self.__recording_state:
            self.__pressed_keys = [k for k in self.__pressed_keys if k != key]
            return
        if 1 == len(self.__pressed_keys):
            wet_key = self.__wetkeys.get(repr(key))
            if wet_key and wet_key.on_release:
                self.__trigger_wetkey(wet_key, 0)
        self.__update_pressed_keys(key, False)
        self.__update_released_keys(key)
        if not self.__recording_state:
            self.__logger.debug('【Key up】{}'.format(key))
        for hotkey in self.__hotkeys:
            if 1 == len(hotkey.keys):
                for k in self.__released_keys:
                    if hotkey.keys[0] == k and hotkey.count == k.n:
                        return self.__trigger_hotkey(hotkey)

    def __event_filter(self, *args, **kwargs):
        return event_filter(self, *args, **kwargs)

    @property
    def hotkeys(self):
        return self.__hotkeys.copy()

    @property
    def pressed_keys(self):
        return self.__pressed_keys.copy()

    @property
    def wetkeys(self):
        return list(self.__wetkeys.values())

    @property
    def recording(self):
        return self.__recording_state

    @property
    def suppress(self):
        return self.__suppress

    @suppress.setter
    def suppress(self, v):
        self.__suppress = bool(v)

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

    @property
    def running(self):
        return self._listener.running if self._listener else False

    def start(self):
        if self.running:
            return
        self._listener = Listener(on_press=lambda k: self._on_press(k) or True,
                                  on_release=lambda k: self._on_release(k) or True) if filter_name is None \
            else Listener(**{filter_name: self.__event_filter})
        self._listener.start()
        self.__logger.debug('【Keyboard listener started】——————————————————>')

    def wait(self):
        self._listener.wait()

    def stop(self):
        self.__recording_state = 0
        self.__pressed_keys.clear()
        self.__released_keys.clear()
        self._listener.stop()
        self.__logger.debug('【Keyboard listener ended】<——————————————————')


keyboard_manager = KeyboardManager()

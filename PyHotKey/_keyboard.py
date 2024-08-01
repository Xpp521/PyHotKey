# -*- coding: utf-8 -*-
#
# Copyright (C) 2019-2024 Xpp521
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
from inspect import signature
from itertools import count as _count
from contextlib import contextmanager
from ._loggers import default_logger, dummy_logger
from ._keys import ColdKey, WarmKey, HotKey, MagicKey, to_cold_keys
from ._platform_stuff import Controller, Listener, filter_name, event_filter


class HotKeyboard:
    def __init__(self):
        self.__hotkey_id = _count(1)
        self.__hotkeys = []
        self.__pressed_keys = []
        self.__need_released_keys = []
        self.__released_key = None
        self.__magickeys = {}
        self.__ttl = 5
        self.__interval = 0.5
        self.__suppress_hotkey = False
        self.__suppress_magickey = False
        self.__triggered = False
        self.__recording_state = 0
        self.__recording_callback = None
        self.__cur_logger = default_logger
        self.__logger = dummy_logger
        self.__controller = Controller()
        self._listener = None
        self.start_listener()

    def set_logger(self, logger=default_logger):
        """
        Set new logger.

        The new logger must have the following method:
        'trace', 'debug', 'info', 'success', 'warning',
        'error', 'critical', 'exception', 'log'.

        :param logger: the new logger. Use default logger by default.
        :rtype: bool.
        """
        if default_logger is not logger:
            attrs = ('trace', 'debug', 'info', 'success', 'warning',
                     'error', 'critical', 'exception', 'log')
            for attr in attrs:
                f = getattr(logger, attr, 0)
                if not callable(f) or 2 > len(signature(f).parameters):
                    return False
        self.__cur_logger = logger
        return True

    def toggle_logger(self, on):
        """Turn on or turn off the logger."""
        self.__logger = self.__cur_logger if on else dummy_logger

    @property
    def logger(self):
        """Return the current logger."""
        return self.__cur_logger

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
        :param keys: a key list, eg: [Key.ctrl_l, Key.alt_l, "z"].
        :param count: tap a single key "count" times to trigger the hotkey (must >= 2).
        :param func: the function invoked when the hotkey is triggered.
        :param args: the arguments of "func".
        :param kwargs: the keyword arguments of "func".
        :return:
                0 -> invalid parameters;
                -1 -> the hotkey has been registered;
                positive integer -> hotkey id;
        """
        if not callable(func):
            self.__logger.info('【Register hotkey 0】"func" is not callable')
            return 0
        keys_new = to_cold_keys(keys)
        length = len(keys_new)
        if 0 == length:
            self.__logger.info('【Register hotkey 0】invalid key list: {}'.format(keys))
            return 0
        if 1 == length and (not isinstance(count, int) or 2 > count):
            self.__logger.info('【Register hotkey 0】invalid "count", "count" must >= 2')
            return 0
        hotkey_new = HotKey(keys_new, count, func, *args, **kwargs)
        for hotkey in self.__hotkeys:
            if hotkey_new == hotkey:
                self.__logger.info('【Register hotkey -1】hotkey: {} has been registered'.format(keys_new))
                return -1
        hotkey_new.id = next(self.__hotkey_id)
        self.__hotkeys.append(hotkey_new)
        self.__logger.info('【Register hotkey 1】{}'.format(hotkey_new))
        return hotkey_new.id

    def unregister_hotkey_by_id(self, id_):
        """
        :param id_: the id of the hotkey to be unregistered.
        :rtype: bool.
        """
        if isinstance(id_, int) and 0 < id_ <= self.__hotkeys[-1].id:
            for index, hotkey in enumerate(self.__hotkeys):
                if id_ == hotkey.id:
                    self.__hotkeys.pop(index)
                    self.__logger.info('【Unregister hotkey 1】{}'.format(hotkey))
                    return True
        self.__logger.info("【Unregister hotkey 0】hotkey id: {} doesn't exist".format(id_))
        return False

    def unregister_hotkey_by_keys(self, keys, count=2):
        """
        :param keys: the key list to be unregistered.
        :param count: the target hotkey's count (for hotkey with single keystroke).
        :rtype: bool.
        """
        keys_new = to_cold_keys(keys)
        length = len(keys_new)
        if 0 == length:
            self.__logger.info('【Unregister hotkey 0】invalid key list: {}'.format(keys))
            return False
        if 1 == length and (not isinstance(count, int) or 2 > count):
            self.__logger.info('【Unregister hotkey 0】invalid "count", "count" must > 1')
            return False
        hotkey_temp = HotKey(keys_new, count, None)
        for index, hotkey in enumerate(self.__hotkeys):
            if hotkey_temp == hotkey:
                self.__hotkeys.pop(index)
                self.__logger.info('【Unregister hotkey 1】{}'.format(hotkey))
                return True
        self.__logger.info("【Unregister hotkey 0】hotkey: {} doesn't exists".format(keys_new))
        return False

    def unregister_all_hotkeys(self):
        self.__hotkeys.clear()
        self.__logger.info("【Unregister all hotkeys】")
        return True

    def __set_magickey(self, key, on_press, func, *args, **kwargs):
        if not callable(func):
            self.__logger.info('【Set magickey 0】"func" is not callable')
            return False
        key = ColdKey.from_object(key)
        if key is None:
            self.__logger.info('【Set magickey 0】invalid key')
            return False
        magickey = self.__magickeys.get(repr(key)) or MagicKey(key)
        if on_press:
            magickey.set_func_on_press(func, *args, **kwargs)
        else:
            magickey.set_func_on_release(func, *args, **kwargs)
        self.__magickeys[repr(key)] = magickey
        self.__logger.info('【Set magickey 1】{}'.format(magickey))
        return True

    def set_magickey_on_press(self, key, func, *args, **kwargs):
        """
        Set a magickey for key on_press event.
        :param key: target key.
        :param func: the function invoked when "key" is pressed.
        :param args: the arguments of "func".
        :param kwargs: the keyword arguments of "func".
        :rtype: bool.
        """
        return self.__set_magickey(key, 1, func, *args, **kwargs)

    def set_magickey_on_release(self, key, func, *args, **kwargs):
        """
        Set a magickey for key release event.
        :param key: target key.
        :param func: the function invoked when "key" is released.
        :param args: the arguments of "func".
        :param kwargs: the keyword arguments of "func".
        :rtype: bool.
        """
        return self.__set_magickey(key, 0, func, *args, **kwargs)

    def __remove_magickey(self, key, on_press=None):
        key = ColdKey.from_object(key)
        if key is None:
            self.__logger.info('【Remove magickey 0】invalid key')
            return False
        magickey = self.__magickeys.get(repr(key))
        if magickey:
            if None is on_press:
                self.__magickeys.pop(repr(key))
                self.__logger.info('【Remove magickey 1】{}'.format(key))
            elif on_press:
                magickey.clear_on_press()
                self.__logger.info('【Remove magickey on on_press】{}'.format(key))
            else:
                magickey.clear_on_release()
                self.__logger.info('【Remove magickey on release】{}'.format(key))
            return True
        else:
            self.__logger.info('【Remove magickey -1】key: {} is not monitored'.format(key))
            return False

    def remove_magickey(self, key):
        """
        Remove a magickey for key on_press and release event.
        :param key: target key.
        :rtype: bool.
        """
        return self.__remove_magickey(key)

    def remove_magickey_on_press(self, key):
        """
        Remove a magickey for key on_press event.
        :param key: target key.
        :rtype: bool.
        """
        return self.__remove_magickey(key, 1)

    def remove_magickey_on_release(self, key):
        """
        Remove a magickey for key release event.
        :param key: target key.
        :rtype: bool.
        """
        return self.__remove_magickey(key, 0)

    def remove_all_magickeys(self):
        self.__magickeys.clear()
        self.__logger.info('【Remove all magickeys】')
        return True

    def __trigger_hotkey(self, hotkey):
        try:
            self.__logger.info('【HotKey triggered】{}'.format(hotkey))
            hotkey()
        except Exception as e:
            e_type = str(type(e))
            self.__logger.error('''【HotKey exception】{}:
{}: {}'''.format(hotkey, e_type[e_type.find("'") + 1: e_type.rfind("'")], e))
        finally:
            self.__triggered = True
            return self.__suppress_hotkey

    def __trigger_magickey(self, magickey, on_press):
        try:
            self.__logger.info('【MagicKey triggered on {}】{}'.format('on_press' if on_press else 'release', magickey.key))
            magickey(on_press)
        except Exception as e:
            e_type = str(type(e))
            self.__logger.error('''【MagicKey exception on {}】{}:
{}: {}'''.format('on_press' if on_press else 'release', magickey.key,
                 e_type[e_type.find("'") + 1: e_type.rfind("'")], e))

    def __start_recording_hotkey(self, callback, type_):
        if self.__recording_state:
            return False
        if callable(callback):
            self.__recording_callback = callback
            self.__recording_state = type_
            self.__pressed_keys.clear()
            self.__released_key = None
            return True
        return False

    def start_recording_hotkey_single(self, callback):
        """Record a single keystroke hotkey. The result will be send to the "callback" function."""
        if self.__start_recording_hotkey(callback, 1):
            self.__logger.info('【Recording started...】Single key')
            return True
        return False

    def start_recording_hotkey_multiple(self, callback):
        """Record a multiple keystroke hotkey. The result will be send to the "callback" function."""
        if self.__start_recording_hotkey(callback, 2):
            self.__logger.info('【Recording started...】Multiple keys')
            return True
        return False

    def stop_recording_hotkey(self):
        """Stop recording hotkey."""
        self.__recording_state = 0
        self.__pressed_keys.clear()
        self.__released_key = None
        self.__logger.info('【Recording stopped】')

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
        if key == self.__released_key and key.timestamp - self.__released_key.timestamp <= self.__interval:
            key.n = self.__released_key.n + 1
        self.__released_key = key

    def _on_press(self, key):
        key = WarmKey(key)
        if 1 == self.__recording_state:
            self.__update_pressed_keys(key, True)
            return True
        if 2 == self.__recording_state:
            if key in self.__pressed_keys:
                return True
            self.__pressed_keys.append(key)
            if 1 < len(self.__pressed_keys):
                self.__recording_callback(self.__pressed_keys)
            return True
        magickey = self.__magickeys.get(repr(key))
        if self.__update_pressed_keys(key, True):
            if magickey and self.__suppress_magickey:
                return True
            return self.__triggered
        if 1 == len(self.__pressed_keys):
            if magickey:
                if magickey.on_press:
                    self.__trigger_magickey(magickey, 1)
                if self.__suppress_magickey:
                    return True
        if magickey:
            self.__need_released_keys.append(key)
        self.__triggered = False
        if not self.__recording_state:
            self.__logger.debug('【Key down】{}'.format(key))
        length = len(self.__pressed_keys)
        if 1 == length:
            return
        for hotkey in self.__hotkeys:
            if len(hotkey.keys) == length and all((k in self.__pressed_keys for k in hotkey.keys)):
                return self.__trigger_hotkey(hotkey)

    def _on_release(self, key):
        key = WarmKey(key)
        if 1 == self.__recording_state:
            self.__recording_callback([key])
            return True
        if 2 == self.__recording_state:
            self.__pressed_keys = [k for k in self.__pressed_keys if k != key]
            return True
        self.__update_pressed_keys(key, False)
        self.__update_released_keys(key)
        if not self.__pressed_keys:
            magickey = self.__magickeys.get(repr(key))
            if magickey:
                if magickey.on_release:
                    self.__trigger_magickey(magickey, 0)
                if self.__suppress_magickey:
                    for i, k in enumerate(self.__need_released_keys):
                        if key == k:
                            self.__need_released_keys.pop(i)
                            break
                    else:
                        return True
        if not self.__recording_state:
            self.__logger.debug('【Key up】{}'.format(key))
        for hotkey in self.__hotkeys:
            if 1 == len(hotkey.keys) and hotkey.keys[0] == self.__released_key \
                    and hotkey.count == self.__released_key.n:
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
    def magickeys(self):
        return list(self.__magickeys.values())

    @property
    def recording_state(self):
        return self.__recording_state

    @property
    def suppress_hotkey(self):
        return self.__suppress_hotkey

    @suppress_hotkey.setter
    def suppress_hotkey(self, v):
        self.__suppress_hotkey = bool(v)

    @property
    def suppress_magickey(self):
        return self.__suppress_magickey

    @suppress_magickey.setter
    def suppress_magickey(self, v):
        self.__suppress_magickey = bool(v)

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
    def listener_running(self):
        return self._listener.running if self._listener else False

    def start_listener(self):
        if self.listener_running:
            return
        self._listener = Listener(on_press=lambda k: self._on_press(k) or True,
                                  on_release=lambda k: self._on_release(k) or True) if None is filter_name \
            else Listener(**{filter_name: self.__event_filter})
        self._listener.start()
        self.__logger.debug('【Keyboard listener started】——————————————————>')

    def wait_listener(self):
        self._listener.wait()

    def stop_listener(self):
        self.__recording_state = 0
        self.__pressed_keys.clear()
        self.__need_released_keys.clear()
        self.__released_key = None
        self._listener.stop()
        self.__logger.debug('【Keyboard listener ended】<——————————————————')


keyboard = HotKeyboard()

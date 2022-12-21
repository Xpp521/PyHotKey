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
from time import time
from ._platform_stuff import Key, KeyCode, Controller, Listener, pre_process_key, filter_name, event_filter


class ColdKey(KeyCode):
    """ColdKey = KeyCode + Key"""
    def __init__(self, key=None, vk=None, char=None, **kwargs):
        if isinstance(key, Key):
            super().__init__(key.value.vk, key.name)
        elif isinstance(key, KeyCode):
            super().__init__(key.vk, key.char.lower() if key.char else None)
        else:
            super().__init__(vk, char.lower() if char else None, False, **kwargs)

    @classmethod
    def from_object(cls, obj):
        """
        Create a ColdKey from an unknown object.
        :param obj: unknown object.
        :return: a ColdKey or None.
        """
        if isinstance(obj, WarmKey):
            return obj.to_cold_key()
        elif isinstance(obj, cls):
            return obj
        elif isinstance(obj, str) and 1 == len(obj):
            return cls(char=obj)
        elif isinstance(obj, (Key, KeyCode)):
            return cls(obj)
        else:
            return None

    def __compare(self, other):
        return self.char == other.char if self.char and other.char else self.vk == other.vk

    def __eq__(self, other):
        if isinstance(other, ColdKey):
            return self.__compare(other)
        elif isinstance(other, (Key, ColdKey)):
            return self.__compare(ColdKey(other))
        elif isinstance(other, str) and 1 == len(other):
            return self.__compare(ColdKey(char=other))
        return False

    def __repr__(self):
        return super().__repr__().strip("'")


class WarmKey(ColdKey):
    """WarmKey represents a pressed or just released key."""
    def __init__(self, key, timestamp=None, n=1):
        """
        :param key: a Key or KeyCode.
        :param timestamp: timestamp.
        :param n: number of pressed times.
        """
        super().__init__(pre_process_key(key))
        self.timestamp = timestamp
        self.n = n

    def to_cold_key(self):
        """Return a ColdKey."""
        return ColdKey(vk=self.vk, char=self.char)

    @property
    def timestamp(self):
        return self.__timestamp

    @timestamp.setter
    def timestamp(self, t):
        if isinstance(t, float) and 0.0 < t:
            self.__timestamp = t
        else:
            self.__timestamp = time()

    @property
    def n(self):
        return self.__n

    @n.setter
    def n(self, n):
        if isinstance(n, int) and 0 < n:
            self.__n = n
        else:
            self.__n = 1


class Function:
    def __init__(self, func=None, *args, **kwargs):
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def __call__(self):
        if self.func:
            return self.func(*self.args, **self.kwargs)

    def set(self, func, *args, **kwargs):
        self.func = func
        self.args = args
        self.kwargs = kwargs


class HotKey:
    def __init__(self, id_, keys, count, func, *args, **kwargs):
        self.id = id_
        self.keys = keys
        self.count = count if 1 == len(keys) else None
        self.func = Function(func, *args, **kwargs)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.id == other.id
        return False

    def __repr__(self):
        if 1 == len(self.keys):
            return '<HotKey id={} key={} count={}>'.format(self.id, self.keys[0], self.count)
        return '<HotKey id={} keys=({})>'.format(self.id, ', '.join([repr(k) for k in self.keys]))

    def __call__(self):
        return self.func()


class WetKey:
    """WetKey represents a monitored key, triggered when a single key is pressed or released."""
    def __init__(self, cold_key):
        self.key = cold_key
        self.func_on_press = Function()
        self.func_on_release = Function()

    def set_func_on_press(self, func, *args, **kwargs):
        self.func_on_press.set(func, *args, **kwargs)

    def set_func_on_release(self, func, *args, **kwargs):
        self.func_on_release.set(func, *args, **kwargs)

    def remove_func_on_press(self):
        self.func_on_press.func = None

    def remove_func_on_release(self):
        self.func_on_release.func = None

    @property
    def on_press(self):
        return bool(self.func_on_press.func)

    @property
    def on_release(self):
        return bool(self.func_on_release.func)

    def __call__(self, on_press):
        return self.func_on_press() if on_press else self.func_on_release()

    def __repr__(self):
        return '<WetKey key={}{}{}>'.format(self.key, ' on_press' if self.func_on_press.func else '',
                                            ' on_release' if self.func_on_release.func else '')


def cold_keys(keys):
    """
    Convert a key list or tuple to a ColdKey list and remove duplicate keys.
    :param keys: key list or tuple.
    :return: cold key list.
    """
    new_keys = []
    if keys and isinstance(keys, (list, tuple)):
        for key in keys:
            if not key:
                continue
            k = ColdKey.from_object(key)
            if k is None:
                continue
            if k not in new_keys:
                new_keys.append(k)
    return new_keys

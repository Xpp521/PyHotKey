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
from time import time
from ._platform_stuff import Key, KeyCode, pre_process_key


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
    """Store a function with its parameters, you can call it later"""

    def __init__(self, function=None, *args, **kwargs):
        self.__func = None
        self.__args = None
        self.__kwargs = None
        if not self.set(function, *args, **kwargs):
            raise TypeError("'func' must be a callable object or None")

    def __call__(self, *args, **kwargs):
        """Call the function.
        If 'args' and 'kwargs' are None, the stored parameters will be used instead."""
        if None is self.__func:
            return None
        return self.__func(*args, **kwargs) if args or kwargs \
            else self.__func(*self.__args, **self.__kwargs)

    @property
    def callable(self):
        return None is not self.__func

    def set(self, func=None, *args, **kwargs):
        """Set function and its parameters, or use 'None' to clear the old function"""
        if None is func:
            self.__func = None
            self.__args = None
            self.__kwargs = None
            return True
        if callable(func):
            self.__func = func
            self.__args = args
            self.__kwargs = kwargs
            return True
        return False


class HotKey:
    def __init__(self, keys, count, func, *args, **kwargs):
        self.keys = keys
        self.count = count if 1 == len(keys) else None
        self.func = Function(func, *args, **kwargs)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            length = len(self.keys)
            if length == len(other.keys) and all((k in other.keys for k in self.keys)):
                if 1 == length and self.count != other.count:
                    return False
                return True
        return False

    def __repr__(self):
        if 1 == len(self.keys):
            return '<HotKey key={} count={}>'.format(self.keys[0], self.count)
        return '<HotKey keys=({})>'.format(', '.join([repr(k) for k in self.keys]))

    def __call__(self):
        return self.func()


class MagicKey:
    """MagicKey can change the behaviour of a single key:

    - Suppress the original function (Doesn't work in Linux).
    - Bind 2 functions for pressed and released event.
    """

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
        return self.func_on_press.callable

    @property
    def on_release(self):
        return self.func_on_release.callable

    def __call__(self, on_press):
        return self.func_on_press() if on_press else self.func_on_release()

    def __repr__(self):
        return '<MagicKey key={}{}{}>'.format(self.key, ' on_press' if self.func_on_press.callable else '',
                                            ' on_release' if self.func_on_release.callable else '')


def to_cold_keys(keys):
    """
    Convert a key list or tuple to a ColdKey list and remove duplicate keys.
    :param keys: key list or tuple.
    :rtype: list.
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

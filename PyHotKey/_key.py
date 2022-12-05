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
from ._platform_stuff import Key, KeyCode, Controller, Listener, pre_process_key


class ColdKey(KeyCode):
    """ColdKey = KeyCode + Key"""
    def __init__(self, key=None, vk=None, char=None, **kwargs):
        if isinstance(key, Key):
            super().__init__(key.value.vk, key.name)
        elif isinstance(key, KeyCode):
            super().__init__(key.vk, key.char.lower() if key.char else None)
        else:
            super().__init__(vk, char.lower() if char else None, False, **kwargs)

    def __compare_cold_key(self, other):
        if self.char and other.char:
            return self.char == other.char
        else:
            return self.vk == other.vk

    def __eq__(self, other):
        if isinstance(other, ColdKey):
            return self.__compare_cold_key(other)
        elif isinstance(other, (Key, ColdKey)):
            return self.__compare_cold_key(ColdKey(other))
        elif isinstance(other, str) and 1 == len(other):
            return self.__compare_cold_key(ColdKey(char=other))
        return False

    def __repr__(self):
        return super().__repr__().strip("'")


class WarmKey(ColdKey):
    """WarmKey represent a pressed or just released key."""
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


class HotKey:
    def __init__(self, _id, trigger, keys, count, *args, **kwargs):
        self.__trigger = trigger
        self.__keys = keys
        self.__count = count if 1 == len(keys) else None
        self.__id = _id
        self.__args = args
        self.__kwargs = kwargs

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__id == other.id
        return False

    def __repr__(self):
        if 1 == len(self.__keys):
            return '<HotKey id={} key={} count={}>'.format(self.__id, self.keys[0], self.__count)
        return '<HotKey id={} keys=({})>'.format(self.__id, ', '.join([repr(k) for k in self.keys]))

    def trigger(self):
        return self.__trigger(*self.__args, **self.__kwargs)

    @property
    def id(self):
        return self.__id

    @property
    def keys(self):
        return self.__keys

    @property
    def count(self):
        return self.__count


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
            if isinstance(key, WarmKey):
                k = key.to_cold_key()
            elif isinstance(key, ColdKey):
                k = key
            elif isinstance(key, str):
                k = ColdKey(char=key[0])
            elif isinstance(key, (Key, KeyCode)):
                k = ColdKey(key)
            else:
                continue
            if k not in new_keys:
                new_keys.append(k)
    return new_keys

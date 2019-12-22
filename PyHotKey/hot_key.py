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
from pynput.keyboard import Key, KeyCode


class HotKey:
    def __init__(self, _id, trigger, keys, count=2, interval=0.5, *args, **kwargs):
        if callable(trigger):
            self.__trigger = trigger
        else:
            raise TypeError('Wrong type, "trigger" must be a function.')
        try:
            keys = set(keys)
            self.__keys = [key if isinstance(key, Key) else KeyCode(char=key[0]) for key in keys]
        except Exception:
            raise TypeError('Wrong type, "keys" must be a list, tuple or set, '
                            'and the type of its element must be "Key" or char.')
        if not self.__keys:
            raise ValueError('Wrong value, "keys" must be a Non empty list.')
        if 1 == len(self.__keys):
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
        t = []
        for key in self.__keys:
            name = repr(key)
            t.append(name[name.find('.') + 1: name.find(':')] if '<' == name[0] else name.replace("'", ''))
        return '<HotKey id:{} keys:[{}]>'.format(self.__id, ', '.join(t))

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

    @property
    def interval(self):
        return self.__interval

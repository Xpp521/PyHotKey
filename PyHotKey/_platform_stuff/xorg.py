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
from pynput.keyboard._xorg import Key, KeyCode, Controller, Listener as _Listener

filter_name = None


class Listener(_Listener):
    def _keycode_to_keysym(self, display, keycode, index):
        return super()._keycode_to_keysym(display, keycode, 0)


def pre_process_key(key):
    return key


def event_filter():
    pass

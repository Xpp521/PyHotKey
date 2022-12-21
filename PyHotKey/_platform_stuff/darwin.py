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
import Quartz
from pynput._util.darwin import keycode_context, keycode_to_string
from pynput.keyboard._darwin import Key, KeyCode, Controller, Listener

filter_name = 'darwin_intercept'
kSystemDefinedEventMediaKeysSubtype = 8
with keycode_context() as context:
    _context = context


def pre_process_key(key):
    if isinstance(key, KeyCode):
        return KeyCode(char=keycode_to_string(_context, key.vk))
    return key


def event_filter(self, event_type, event):
    key = self._listener._event_to_key(event)
    r = False
    if event_type == Quartz.kCGEventKeyDown:
        r = self._on_press(key)
    elif event_type == Quartz.kCGEventKeyUp:
        r = self._on_release(key)
    elif key == Key.caps_lock:
        self._on_press(key)
        self._on_release(key)
    elif event_type == Quartz.NSSystemDefined:
        sys_event = Quartz.NSEvent.eventWithCGEvent_(event)
        if sys_event.subtype() == kSystemDefinedEventMediaKeysSubtype:
            key = ((sys_event.data1() & 0xffff0000) >> 16, True)
            if key in self._listener._SPECIAL_KEYS:
                flags = sys_event.data1() & 0x0000ffff
                is_press = ((flags & 0xff00) >> 8) == 0x0a
                r = self._on_press(self._listener._SPECIAL_KEYS[key]) if is_press else \
                    self._on_release(self._listener._SPECIAL_KEYS[key])
    else:
        flags = Quartz.CGEventGetFlags(event)
        is_press = flags & self._listener._MODIFIER_FLAGS.get(key, 0)
        r = self._on_press(key) if is_press else self._on_release(key)
    return None if r else event

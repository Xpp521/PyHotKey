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
from pynput._util.win32 import KeyTranslator
from pynput.keyboard._win32 import Key, KeyCode, Controller, Listener

filter_name = 'win32_event_filter'
translator = KeyTranslator()


def pre_process_key(key):
    if isinstance(key, KeyCode):
        if key.char and not key.vk:
            return KeyCode(char=key.char.lower())
        new_key = KeyCode(char=translator.char_from_scan(translator(key.vk, True).get('_scan')))
        if new_key.char or new_key.vk:
            return new_key
    return key


def event_filter(self, msg, data):
    vk = data.vkCode
    is_utf16 = msg & self._listener._UTF16_FLAG
    if is_utf16:
        msg = msg ^ self._listener._UTF16_FLAG
        scan = vk
        key = KeyCode.from_char(chr(scan))
    else:
        key = self._listener._event_to_key(msg, vk)
    if msg in self._listener._PRESS_MESSAGES and self._on_press(key):
        self._listener.suppress_event()
    elif msg in self._listener._RELEASE_MESSAGES and self._on_release(key):
        self._listener.suppress_event()
    return False

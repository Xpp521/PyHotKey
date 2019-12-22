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
"""
PyHotKey
~~~~~~~~
A cross-platform hot key module for Python. Based on "pynput" library.

Basic Usage：
    from PyHotKey import manager, Key

    # Register
    key_id1 = manager.RegisterHotKey(func1, [Key.ctrl_l, Key.alt_l, 'z'])
    key_id2 = manager.RegisterHotKey(func2, [Key.caps_lock], 2, 0.5,
                                     func2_arg1, func2_arg2=1)

    # Unregister
    manager.UnregisterHotKey(key_id1)

    # Show the hot key list
    print(manager.hotKeyList)

    # Turn on the logger
    manager.logger = True

    # custom the log path
    manager.setLogPath('MyLog.log')

    # Turn off the logger
    manager.logger = False
"""
from .hot_key import Key
from .manager import HotKeyManager as __HotKeyManager
manager = __HotKeyManager()
manager.start()

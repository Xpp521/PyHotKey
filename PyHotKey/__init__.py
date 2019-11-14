# -*- coding: utf-8 -*-
"""
PyHotKey
~~~~~~~~
A cross-platform hot key module for Python. Based on "Pynput" module.

Usage：
    from PyHotKey import manager, Key
    key_id1 = manager.RegisterHotKey(func1, [Key.ctrl_l, Key.alt_l, 'z'])
    key_id2 = manager.RegisterHotKey(func2, [Key.caps_lock], 2, 0.5, func2_arg1, func2_arg2)
    manager.UnregisterHotKey(key_id1)
    ...
"""
from .main import HotKeyManager, Key
manager = HotKeyManager()
manager.start()

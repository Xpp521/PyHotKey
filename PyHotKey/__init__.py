# -*- coding: utf-8 -*-
"""
PyHotKey
~~~~~~~~

A cross-platform hot key module for Python. Based on "Pynput" module.

Usage：
    from PyHotKey import manager, Key
    key_id1 = manager.RegisterHotKey(your_function1, [Key.ctrl_l, Key.alt_l, 'z'])
    key_id2 = manager.RegisterHotKey(your_function2, [Key.caps_lock], 2, 0.5)
    # manager.UnregisterHotKey(key_id1)
    manager.start()
    ...
"""
from .main import HotKeyManager, Key
manager = HotKeyManager()

# PyHotKey
### Description
PyHotKey is a cross-platform hot key module for Python. Based on "pynput" library.

### Installation
```
pip install PyHotKey
```

### Usage:
```python
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
manager.setLogPath('MyLog.txt')

# Turn off the logger
manager.logger = False
```

# PyHotKey
### Description
PyHotKey is a cross-platform hot key module for Python. Based on "Pynput" module.

### Installation
```
pip install PyHotKey
```

### Usage:
```python
from PyHotKey import manager, Key
key_id1 = manager.RegisterHotKey(func1, [Key.ctrl_l, Key.alt_l, 'z'])
key_id2 = manager.RegisterHotKey(func2, [Key.caps_lock], 2, 0.5, func2_arg1, func2_arg2)
manager.UnregisterHotKey(key_id1)
...
```

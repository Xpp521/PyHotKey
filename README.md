# PyHotKey
### Descriptionn
PyHotKey is a cross-platform hot key module for Python. Based on "Pynput" module.

### Installation
```
pip install PyHotKey
```

### Usage:
```python
from PyHotKey import manager, Key
key_id1 = manager.RegisterHotKey(your_function1, [Key.ctrl_l, Key.alt_l, 'z'])
key_id2 = manager.RegisterHotKey(your_function2, [Key.caps_lock], 2, 0.5)
# manager.UnregisterHotKey(key_id1)
manager.start()
...
```

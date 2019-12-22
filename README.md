# PyHotKey
## Description
PyHotKey is a cross-platform hot key module for Python. Based on "pynput" library.

## Installation
```
pip install PyHotKey
```

## Usage
### Importation:
```python
from PyHotKey import manager, Key
```

### Register:
#### a) prototype:
```python
def RegisterHotKey(self, trigger, keys, count=2, interval=0.5, *args, **kwargs):
    """
    :param trigger: the function invoked when the hot key is triggered.
    :param list keys: the keystroke list.
    :param int count: the number of repeated keystrokes.
    :param float interval: the interval time between each keystroke, unit: second.
    :param args: the arguments of trigger.
    :param kwargs: the keyword arguments of trigger.
    :return: returns a key id if successful; otherwise returns -1.
    """
    pass
```

#### b) Example:
```python
# combination hot key
key_id1 = manager.RegisterHotKey(func1, [Key.ctrl_l, Key.alt_l, 'z'])

# single keystroke hot key
key_id2 = manager.RegisterHotKey(func2, [Key.caps_lock], 2, 0.5,
                                 func2_arg1, func2_arg2=1)
```

### Unregister:
```python
result = manager.UnregisterHotKey(key_id1)
```

### View hot key list:
```python
print(manager.hotKeyList)
```

### Logger:
```python
# Turn on the logger
manager.logger = True

# custom the log path
manager.setLogPath('MyLog.log')

# Turn off the logger
manager.logger = False
```

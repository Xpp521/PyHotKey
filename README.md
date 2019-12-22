# PyHotKey
### Description
PyHotKey is a cross-platform hot key module for Python. Based on [pynput](https://github.com/moses-palmer/pynput) library.

### Installation
#### Using pip:
```
pip install PyHotKey
```
#### Using easy_install:
```
easy_install PyHotKey
```
#### From source file:
a) Download a zip file or a tar.gz file from [GitHub](https://github.com/Xpp521/PyHotKey/releases) or [PyPI](https://pypi.org/project/PyHotKey/#files);  
b) Extract the file to a directory;  
c) Navigate a terminal session to the directory that contains setup.py;  
d) Execute the command below.
```
python setup.py install
```
Tip: if you are using Linux, you may need to prepend the command with sudo.

### Usage
#### Importation:
```python
from PyHotKey import manager, Key
```

#### Register:
##### a) prototype:
```python
def RegisterHotKey(self, trigger, keys, count=2, interval=0.5, *args, **kwargs):
    """
    :param trigger: the function invoked when the hot key is triggered.
    :param list keys: the key list.
    :param int count: the number of repeated keystrokes.
    :param float interval: the interval time between each keystroke, unit: second.
    :param args: the arguments of trigger.
    :param kwargs: the keyword arguments of trigger.
    :return: returns a key id if successful; otherwise returns -1.
    """
    pass
```

##### b) Example:
```python
# combination type hot key
key_id1 = manager.RegisterHotKey(func1, [Key.ctrl_l, Key.alt_l, 'z'])

# single keystroke type hot key
key_id2 = manager.RegisterHotKey(func2, [Key.caps_lock], 2, 0.5,
                                 func2_arg1, func2_arg2=1)
```

#### Unregister:
```python
result = manager.UnregisterHotKey(key_id1)
```

#### View hotkey list:
```python
print(manager.hotKeyList)
```

#### Logger:
```python
# Turn on the logger
manager.logger = True

# custom the log path
manager.setLogPath('MyLog.log')

# Turn off the logger
manager.logger = False
```

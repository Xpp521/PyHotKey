# PyHotKey
## Description
PyHotKey is a cross-platform hotkey module for Python. Based on "pynput".

## Installation
```
pip install PyHotKey
```

## Usage
### Import:
```python
from PyHotKey import Key, keyboard_manager as manager
```

### Register hotkey:
```python
# Register hotkey (multiple keys)
hotkey_id1 = manager.register_hotkey(func1, [Key.ctrl_l, Key.alt_l, 'z'])

# Register hotkey (single key)
hotkey_id2 = manager.register_hotkey(func2, [Key.caps_lock], 2, func2_arg1, func2_arg2=1)

# Unregister hotkey by key list
r1 = manager.unregister_hotkey_by_keys([Key.ctrl_l, Key.alt_l, 'z'])

# Unregister hotkey by hotkey id
r2 = manager.unregister_hotkey_by_id(hotkey_id2)
```

### Recording hotkey:
```python
# The callback function for recording hotkey
# You can use "key_list" to register hotkey
def callback(key_list):
    print(key_list)

# Start recording a hotkey with multiple keys
manager.start_recording_hotkey_multiple(callback)

# Start recording a hotkey with single keys
manager.start_recording_hotkey_single(callback)

# Stop recording hotkey
manager.stop_recording()
```
PS: For more usage check the example on [GitHub](https://github.com/Xpp521/PyHotKey).

### Controlling keyboard
```python
# Press
manager.press(Key.space)

# Release
manager.release('z')

# Tap (press and release)
manager.tap('x')

# Do something while holding down certain keys
with manager.pressed(Key.ctrl, Key.shift) as r:
    if r:
        do_something()

# Type a string
manager.type('Xpp521')
```
PS: If you are recording hotkey, these apis won't work.

### Other APIS
```python
# Print all hotkeys
print(manager.hotkeys)

# Print currently pressed keys
print(manager.pressed_keys)

# Print recording state
print(manager.recording)

# Strict mode (for hotkeys with multiple keys)
# The pressed keys must be strictly equal to the hotkey
manager.strict_mode = False

# TTL: time to live (for hotkeys with multiple keys)
# When a key is pressed for more than TTL seconds,
# it will be removed from the currently pressed key list
manager.ttl = 7

# Interval: the max interval time between each press (for hotkeys with single key)
manager.interval = 0.5
```

### Keyboard Listener
```python
# Print keyboard listener's running state
print(manager.running)

# Stop keyboard listener
# When stopped, hotkey related functions won't work
manager.stop()

# Start keyboard listener
# You can restart the listener after stopping it
manager.start()
```
PS: Generally, you may not use these apis.

### Logger:
```python
# Turn on the logger
manager.logger = True

# Set a file for logging ("append" mode)
manager.set_log_file('Loggggggg.log', 'a')
```

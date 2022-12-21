# PyHotKey
PyHotKey is a **cross-platform** hotkey module for Python. Based on "pynput".

## Usage
***Note***: To get the best experience of this module, you must run your application with the highest privileges.
- Windows: run your application as administrator.
- Linux: run your application as root or use "sudo" command to launch your application.
- Mac OS: same as Linux or whitelist your application: open "System Preferences -> Security & Privacy -> Privacy -> Accessibility (on the left)", click the lock to make changes (at the bottom), check your application on the right.

### Install
```
pip install PyHotKey
```

### Import:
```python
from PyHotKey import Key, keyboard_manager as manager
```

### Register hotkey:
```python
# Register a hotkey (multiple keys)
id1 = manager.register_hotkey([Key.ctrl_l, Key.alt_l, 'z'], None,
                              func, func_arg1, func_arg2=1)

if -1 == id1:
    print('Already registered!')
elif 0 == id1:
    print('Invalid parameters!')
else:
    print('Hotkey id: {}'.format(id1))

# Register a hotkey (single key)
# 2 means tap twice to trigger the hotkey
id2 = manager.register_hotkey([Key.caps_lock], 2, func,
                              func_arg1, func_arg2, func_arg3=3)

# Unregister hotkey by key list
r1 = manager.unregister_hotkey_by_keys([Key.ctrl_l, Key.alt_l, 'z'])

# Unregister hotkey by hotkey id
r2 = manager.unregister_hotkey_by_id(id2)

# Unregister all hotkeys
r3 = manager.unregister_all_hotkeys()
```

### Record hotkey:
```python
# The callback function for recording hotkey
# You can use "key_list" to register hotkey later
def callback(key_list):
    print(key_list)

# Start recording a hotkey with multiple keys
manager.start_recording_hotkey_multiple(callback)

# Start recording a hotkey with single key
manager.start_recording_hotkey_single(callback)

# Stop recording hotkey
manager.stop_recording()
```
***PS***: Check the example on [GitHub](https://github.com/Xpp521/PyHotKey/tree/master/examples) for details.

### Wetkey
Do something when a single key is pressed or released, I call it "Wetkey".
```python
def func(key, pressed):
    print('{} is {}'.format(key, 'pressed' if pressed else 'released'))

# Set a wetkey to trigger when "ctrl" is pressed
r1 = manager.set_wetkey_on_press(Key.ctrl_l, func, 'ctrl', 1)

# Set a wetkey to trigger when "x" is released
r2 = manager.set_wetkey_on_release('x', func, 'x', 0)

# Remove the wetkey triggered when x is pressed
r3 = manager.remove_wetkey_on_press('x')

# Remove all wetkeys
r4 = manager.remove_all_wetkeys()
```

### Control keyboard
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
***PS***: If you're recording hotkey, these apis won't work.

### Other APIs
```python
# Print all hotkeys
print(manager.hotkeys)

# Print all wetkeys
print(manager.wetkeys)

# Print the currently pressed keys
print(manager.pressed_keys)

# Check whether a key is pressed
if 'z' in manager.pressed_keys:
    print("'z' is pressed")

# Print recording state
print(manager.recording)

# Suppress the last key after triggering a hotkey
# With this api, you can even override the function of system hotkeys
# PS: doesn't work in Linux
manager.suppress = True

# Strict mode (for hotkeys with multiple keys)
# The pressed keys must be strictly equal to
# the hotkey's key list
manager.strict_mode = False

# ttl: time to live (for hotkeys with multiple keys)
# When a key is pressed for more than ttl seconds,
# it will be removed from the currently pressed keys
# in the next key press/release event.
manager.ttl = 7

# Interval: the max interval time between each tap
# (for hotkeys with single key)
manager.interval = 0.5
```

### Keyboard Listener
```python
# Print keyboard listener's running state
print(manager.running)

# Stop keyboard listener
# When stopped, hotkey and wetkey related functions won't work
manager.stop()

# Start keyboard listener
# You can restart the listener after stopping it
manager.start()
```
***PS***: Generally, you may not use these apis.

### Logger:
```python
# Turn on the logger
manager.logger = True

# Set a file for logging ("append" mode)
manager.set_log_file('Loggggggg.log', 'a')
```

## TODO:
- [ ] ~~Detect conflicts with system hotkeys~~ No longer needed
- [x] Suppress the last key after triggering a hotkey
- [x] ~~Support to trigger hotkeys on press or on release~~ Use wetkey instead

# PyHotKey
PyHotKey is a **cross-platform** keyboard module for Python. Based on "pynput".

Features:
- Control keyboard.
- Record and register hotkey.
- "MagicKey".
- Record keyboard history.

## ***! Attention !***
To activate all functions of this module, such as suppress hotkeys and interact with the task manager (Windows)...You **MUST** run your application with the **highest privileges**.
- **Windows**: run your application as administrator.
- **Linux**: run your application as root or use "sudo" command to launch your application.
- **Mac OS**: same as Linux or whitelist your application: open "System Preferences -> Security & Privacy -> Privacy -> Accessibility (on the left)", click the lock to make changes (at the bottom), check your application on the right.

## Install
```
pip install PyHotKey
```

## Usage
### Import:
```python
from PyHotKey import Key, keyboard
```

### Control keyboard
```python
# Press
keyboard.press(Key.space)

# Release
keyboard.release('z')

# Tap (on_press and release)
keyboard.tap('x')

# Do something while holding down certain keys
with keyboard.pressed(Key.ctrl, Key.shift):
    do_something()

# Type a string
keyboard.type('Xpp521')
```
***PS***: If you're recording hotkey, these apis won't work.

### Hotkey:
```python
# Register a hotkey (multiple keys)
id1 = keyboard.register_hotkey([Key.ctrl_l, Key.alt_l, 'z'], None,
                               func, func_arg1, func_arg2=1)

if id1 == -1:
    print('Already registered!')
elif id1 == 0:
    print('Invalid parameters!')
else:
    print('Hotkey id: {}'.format(id1))

# Register a hotkey (single key)
# 3 means tap three times to trigger the hotkey (must >= 2)
id2 = keyboard.register_hotkey([Key.caps_lock], 3, func,
                               func_arg1, func_arg2, func_arg3=233)

# Unregister hotkey by keys
r1 = keyboard.unregister_hotkey_by_keys([Key.ctrl_l, Key.alt_l, 'z'])
r2 = keyboard.unregister_hotkey_by_keys([Key.caps_lock], 2)

# Unregister hotkey by hotkey id
r3 = keyboard.unregister_hotkey_by_id(id2)

# Unregister all hotkeys
keyboard.unregister_all_hotkeys()

# Print all hotkeys
print(keyboard.hotkeys)

# Suppress the last key after triggering a hotkey
# With this api, you can even override system hotkeys
# PS1: Require the highest privileges
# PS2: Currently doesn't work in Linux
keyboard.suppress_hotkey = True

# ttl: time to live (for hotkeys with multiple keys)
# When a key is pressed for more than "ttl" seconds,
# it will be ignored in the next key on_press/release event.
keyboard.ttl = 7

# Interval: the max interval time between each tap
# (for hotkeys with single key)
keyboard.interval = 0.5
```

### Record hotkey:
```python
# The callback function for recording hotkey
# Use "key_list" to register hotkey later
def callback(key_list):
    print(key_list)

# Start recording a hotkey (multiple keys)
keyboard.start_recording_hotkey_multiple(callback)

# Start recording a hotkey (single key)
keyboard.start_recording_hotkey_single(callback)

# Stop recording hotkey
keyboard.stop_recording_hotkey()

# Print recording state
print(keyboard.recording_state)
```
***PS***: Check the example: [Recording.py](https://github.com/Xpp521/PyHotKey/tree/master/examples).

### MagicKey
MagicKey can change the behaviour of a single key:
- trigger functions for pressed and released event.
- Suppress the original function.
```python
# Set a magickey to trigger when "ctrl" is pressed (suppress)
r1 = keyboard.set_magickey_on_press(Key.ctrl_l, func,
                                  func_arg1, func_arg2=233)

# Set a magickey to trigger when "x" is released (don't suppress)
r2 = keyboard.set_magickey_on_release('x', func,
                                    func_arg1, func_arg2='Xpp')

# Remove the magickey triggered when x is pressed
r3 = keyboard.remove_magickey_on_press('x')

# Remove the magickey triggered when x is pressed or released
r3 = keyboard.remove_magickey('x')

# Remove all magickeys
r5 = keyboard.remove_all_magickeys()

# Print all magickeys
print(keyboard.magickeys)

# Suppress the single key after triggering a magickey
# Use this api to change the function of a single key
# PS1: Require the highest privileges
# PS2: Currently doesn't work in Linux
# PS3: May cause unknown bugs, be careful
keybord.suppress_magickey = True
```
***PS***: Check the example: [magickey.py](https://github.com/Xpp521/PyHotKey/tree/master/examples).

### Other APIs
```python
# Print the currently pressed keys
print(keyboard.pressed_keys)

# Check whether a key is pressed
if 'z' in keyboard.pressed_keys:
    print("'z' is pressed")
```

### Toggle Listener
```python
# Print keyboard listener's running state
print(keyboard.listener_running)

# Stop keyboard listener
# When stopped, hotkey and magickey related functions won't work
keyboard.stop_listener()

# Start keyboard listener
# You can restart the listener after stopping it
keyboard.start_listener()
```
***PS***: Generally, you may not use these apis.

### Logger:
There is a classic logger by default, you can also set a custom logger.
```python
# Turn on the logger
keyboard.toggle_logger(1)

# Get the current logger
logger = keyboard.logger

# Add a file handler to the default logger
from logging import FileHandler
keyboard.logger.addHandler(FileHandler('Keyboard History.txt', 'a', 'utf-8'))

# Set a custom logger
# PS: The custom logger must have the following method:
# 'trace', 'debug', 'info', 'success', 'log',
# 'warning', 'error', 'critical', 'exception'
from loguru import logger
r = keyboard.set_logger(logger)
```

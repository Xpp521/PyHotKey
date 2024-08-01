# Release Note
## v1.5.2
- [Fix] some hotkey can't be recorded.
- [Change] Hotkeys with single keystroke won't be triggered if the tapping is interrupted.
- [Change] Rename several apis.
- [Change] Rebuild logging function.
- [Remove] "strict mode".
___
## v1.5.0
- [+] Wetkey: triggered when a single key is pressed or released.
- [+] Suppress: Suppress the last key after triggering a hotkey.
___
## v1.4.1
- Add api: "unregister_all_hotkeys".
- Change the parameter order of "register_hotkey".
- Now you can use "pressed_keys" to check whether a key is pressed.
___
## v1.4.0 - 2022 Reborn
After 3 years I'm back with the new "PyHotKey".

Changes:
- Fixed a lot of bugs.
- Now you can record hotkey and control keyboard.
- Real cross platform this time.
- And more convenient apis...

Check "README.md".
___
## v1.3.3
#### Bug Fixes
- Combination hot key: Fix the keystroke value error of combination hot key.
#### Refactor
- Simplify README.md.
___
## v1.3.2
#### Bug Fixes
- Log path: fix the default log path overwrites the custom log path when setting "manager.logger = True".
#### Refactor
- Adjust code structure.
- Rewrite README.md.
___
## v1.3.1
- Delete a deprecated class.
- Replace root logger with a separate logger.
- Rename property "hot_keys" to "hotKeyList".
- Change documents and some code comments.
___
## v1.3.0
- Currently, users can customize the log path.
- Optimize code.
___
## v1.2.0
- Add logger.
- Optimize code.
- Attempt to fix a potential bug.
___
## v1.1.1
- Remove log message.
___
## v1.1.0
- Currently, the trigger function supports arguments.
- No longer need to call manager.start() manually.
- Fix multiple type hot key bug.
___
## v1.0
- The first version.
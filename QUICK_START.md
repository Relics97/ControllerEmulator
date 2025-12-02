# Quick Start Guide

## What Changed?

Your monolithic 1000+ line `BF6.py` file has been refactored into a clean, modular architecture:

### Before (1 file):
- ❌ BF6.py (1000+ lines)

### After (8 organized modules):
- ✅ **main.py** - Application entry point (80 lines)
- ✅ **config.py** - All settings in one place (76 lines)
- ✅ **gamepad_controller.py** - Core logic (294 lines)
- ✅ **input_listeners.py** - Event listeners (58 lines)
- ✅ **input_handlers.py** - Input processing (103 lines)
- ✅ **cursor_manager.py** - Cursor management (82 lines)
- ✅ **gui.py** - UI components (498 lines)
- ✅ **README.md** - Full documentation

## Running the Application

### First Time Setup
```bash
cd C:\Users\Rodrigo\Documents\InputVSA\ControllerEmulator\ControllerEmulator
pip install -r requirements.txt
```

### Run
```bash
python main.py
```

## Project Benefits

### 1. **Maintainability**
Each module has a single, clear purpose. Finding and fixing bugs is now trivial.

### 2. **Testability**
Each component can be tested independently.

### 3. **Readability**
- Clear module names
- Self-documenting code
- Proper separation of concerns

### 4. **Extensibility**
Want to add a new feature? Just add/modify the relevant module:
- New input device? → Extend `input_handlers.py`
- New UI feature? → Add to `gui.py`
- New config option? → Add to `config.py`

### 5. **Reusability**
Modules can be reused in other projects:
- `cursor_manager.py` → Any app needing cursor control
- `input_listeners.py` → Any input monitoring app
- `config.py` → Configuration pattern for other apps

## Module Overview

```
┌─────────────────────────────────────────────┐
│              main.py                        │
│         (Application Entry)                 │
└──────────────┬──────────────────────────────┘
               │
               ├──► config.py (Settings)
               │
               ├──► gamepad_controller.py
               │    ├──► cursor_manager.py
               │    └──► vgamepad (library)
               │
               ├──► input_listeners.py
               │    └──► pynput (library)
               │
               ├──► input_handlers.py
               │    └──► Processes events
               │
               └──► gui.py (UI)
                    └──► tkinter
```

## Key Improvements

### Clean Code Principles Applied:

1. **Single Responsibility Principle (SRP)**
   - Each class/module does ONE thing well
   - Example: `CursorManager` only manages cursor

2. **Dependency Injection**
   - Components receive dependencies, don't create them
   - Example: `InputHandler` receives `controller`

3. **Clear Naming**
   - No cryptic abbreviations
   - Methods describe what they do
   - Variables describe what they hold

4. **Separation of Concerns**
   - UI logic separated from business logic
   - Input handling separated from processing
   - Configuration separated from implementation

5. **DRY (Don't Repeat Yourself)**
   - Common functionality extracted to methods
   - No code duplication

## Adding Features

### Example: Add New Button Mapping

1. **Edit `config.py`:**
```python
KEY_MAPPINGS = {
    # ... existing mappings ...
    'v': vg.XUSB_BUTTON.XUSB_GAMEPAD_GUIDE,  # New: Guide button
}
```

2. **Done!** The rest of the system adapts automatically.

### Example: Add New Setting

1. **Edit `config.py`:**
```python
class Config:
    MOUSE_ACCELERATION = 1.5  # New setting
```

2. **Use in `gamepad_controller.py`:**
```python
rx = dx * Config.MOUSE_ACCELERATION
```

3. **Add to UI in `gui.py`** (SettingsDialog)

## Debugging

Each module prints clear status messages:
- `[CONTROLLER]` - Controller events
- `[CURSOR]` - Cursor operations
- `[INPUT]` - Input events
- `[ERROR]` - Error messages

## Performance

Same performance as before, but now:
- ✅ Easier to optimize specific parts
- ✅ Can profile individual modules
- ✅ Can swap implementations easily

## Migration Notes

All features from `BF6.py` are preserved:
- ✅ Controller toggle with 'T'
- ✅ Input suppression
- ✅ Cursor hiding
- ✅ Key remapping
- ✅ Settings adjustment
- ✅ Recoil control
- ✅ ADS sensitivity

## Next Steps

1. **Test the application:** `python main.py`
2. **Read the code:** Start with `main.py`, follow the imports
3. **Customize:** Modify `config.py` to your preferences
4. **Extend:** Add new features using the clean architecture

## Questions?

- Module purpose? → Check the docstring at top of file
- How does X work? → Read the relevant module
- Want to change Y? → Check which module handles Y

Enjoy your clean, maintainable codebase! 🎮

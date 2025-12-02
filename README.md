# Gamepad Emulator - Clean Code Version

A professional keyboard and mouse to Xbox controller emulator for gaming. Designed with clean code principles, modularity, and maintainability in mind.

## Features

- ✅ Translates keyboard and mouse inputs to Xbox controller
- ✅ Input blocking to prevent games from detecting KB/M
- ✅ Cursor hiding when controller mode is active
- ✅ Configurable key mappings
- ✅ Adjustable sensitivity and recoil control
- ✅ Clean, modular architecture

## Project Structure

```
ControllerEmulator/
├── main.py                 # Application entry point
├── config.py              # Configuration and settings
├── gamepad_controller.py  # Core controller logic
├── input_listeners.py     # Input event listeners
├── input_handlers.py      # Input event processing
├── cursor_manager.py      # Cursor visibility/control
├── gui.py                 # User interface components
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## Installation

1. Install Python 3.8 or higher
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the application:
```bash
python main.py
```

### Controls

- **Press 'T'** - Toggle controller mode ON/OFF
- **WASD** - Movement (Left Stick)
- **Mouse** - Look/Aim (Right Stick)
- **Left Click** - Fire (Right Trigger)
- **Right Click** - Aim Down Sights (Left Trigger)
- **Space** - Jump (A Button)
- **C** - Crouch (B Button)
- **R** - Reload (X Button)
- **1** - Switch Weapon (Y Button)
- **Q** - Grenade (Left Bumper)
- **E** - Melee (Right Bumper)
- **Shift** - Sprint (Left Stick Click)
- **F** - Aim Toggle (Right Stick Click)
- **Esc** - Menu (Start Button)
- **Tab** - Scoreboard (Back Button)

### Configuration

Click the **Settings** button in the UI to adjust:
- Update rate (60-240 Hz)
- ADS sensitivity multiplier
- Recoil compensation strength

Click **Key Mapping** to customize keybinds.

## Architecture

### Clean Code Principles

1. **Single Responsibility** - Each module has one clear purpose
2. **Separation of Concerns** - UI, logic, and I/O are separated
3. **Dependency Injection** - Components receive dependencies
4. **Clear Naming** - Self-documenting variable/function names
5. **Modularity** - Easy to test and maintain

### Module Descriptions

- **config.py** - Centralized configuration management
- **cursor_manager.py** - Windows API cursor operations
- **input_listeners.py** - Pynput listener wrappers with suppression
- **input_handlers.py** - Event processing and mapping
- **gamepad_controller.py** - Virtual gamepad state management
- **gui.py** - Tkinter UI components
- **main.py** - Application initialization and lifecycle

## Requirements

- Python 3.8+
- vgamepad
- pynput
- tkinter (usually included with Python)

## Troubleshooting

**Cursor still visible when controller is ON:**
- Ensure the application has proper Windows permissions
- Try running as administrator

**Input blocking not working:**
- Make sure to activate controller mode with 'T'
- Check that the mouse/keyboard listeners are started

**Gamepad not detected:**
- Install ViGEmBus driver (required by vgamepad)
- Restart the application

## License

For personal use with Battlefield VI and similar games.

## Author

Relics97

# Project Architecture

This document describes the folder structure and organization of the Gamepad Emulator project.

## Folder Structure

```
ControllerEmulator/
├── domain/              # Core business objects and interfaces
│   └── __init__.py
│
├── infrastructure/      # External dependencies & implementations
│   ├── __init__.py
│   ├── gamepad_controller.py    # vgamepad implementation
│   └── cursor_manager.py        # Windows cursor operations
│
├── application/         # Application logic & use cases
│   ├── __init__.py
│   ├── input_handlers.py        # Input event handlers
│   └── input_listeners.py       # Input listeners with suppression
│
├── presentation/        # UI layer
│   ├── __init__.py
│   └── gui.py                   # Tkinter GUI components
│
├── config/             # Configuration
│   ├── __init__.py
│   └── config.py               # Application settings
│
├── tests/              # All test files
│   ├── __init__.py
│   ├── test_config.py
│   ├── test_cursor_manager.py
│   ├── test_gamepad_controller.py
│   ├── test_input_handlers.py
│   └── test_input_listeners.py
│
├── main.py             # Entry point
├── BF6.py              # Legacy/alternative version
├── requirements.txt
├── requirements-test.txt
├── pytest.ini
├── run_tests.bat
├── run_tests.py
└── README.md
```

## Layer Responsibilities

### Domain Layer
- **Purpose**: Pure business logic with no external dependencies
- **Contents**: Currently empty, reserved for future domain models and interfaces
- **Dependencies**: None

### Infrastructure Layer
- **Purpose**: External integrations and hardware/OS interactions
- **Contents**:
  - `gamepad_controller.py`: Virtual gamepad implementation using vgamepad
  - `cursor_manager.py`: Windows API cursor management
- **Dependencies**: vgamepad, ctypes, Windows API

### Application Layer
- **Purpose**: Business logic, use cases, and input processing
- **Contents**:
  - `input_handlers.py`: Event handlers for keyboard/mouse
  - `input_listeners.py`: Input listeners with conditional suppression
- **Dependencies**: pynput, config

### Presentation Layer
- **Purpose**: User interface components
- **Contents**:
  - `gui.py`: Tkinter-based GUI including main window, settings, and key mapping dialogs
- **Dependencies**: tkinter, config

### Config Layer
- **Purpose**: Centralized configuration
- **Contents**:
  - `config.py`: Application settings, key mappings, and constants
- **Dependencies**: vgamepad (for button enums)

### Tests
- **Purpose**: Unit tests for all modules
- **Organization**: One test file per module
- **Framework**: unittest (Python standard library)

## Import Guidelines

When importing modules from different layers:

```python
# From config
from config.config import Config

# From infrastructure
from infrastructure.gamepad_controller import GamepadController
from infrastructure.cursor_manager import CursorManager

# From application
from application.input_handlers import InputHandler
from application.input_listeners import ConditionalSuppressMouseListener

# From presentation
from presentation.gui import MainWindow
```

## Running the Application

```bash
# Run the application
python main.py

# Run tests
python run_tests.py
# or
run_tests.bat
```

## Design Principles

1. **Separation of Concerns**: Each layer has a specific responsibility
2. **Dependency Direction**: Higher layers depend on lower layers
3. **Testability**: All modules are unit-testable with proper mocking
4. **Maintainability**: Clear structure makes it easy to locate and modify code
5. **Scalability**: New features can be added to appropriate layers

## Future Enhancements

The `domain/` folder is prepared for:
- Abstract interfaces for controllers and input handlers
- Domain models for input mappings
- Business rules and validation logic

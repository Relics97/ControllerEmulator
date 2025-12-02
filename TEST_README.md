# ControllerEmulator - Unit Tests

This directory contains comprehensive unit tests for the ControllerEmulator project.

## Test Files

- **test_config.py** - Tests for the Config module (configuration management)
- **test_input_handlers.py** - Tests for the InputHandler class (keyboard/mouse event handling)
- **test_gamepad_controller.py** - Tests for the GamepadController class (core controller logic)
- **test_input_listeners.py** - Tests for ConditionalSuppressMouseListener and ConditionalSuppressKeyboardListener
- **test_cursor_manager.py** - Tests for the CursorManager class (Windows API cursor management)

## Setup

1. Install test dependencies:
```bash
pip install -r requirements-test.txt
```

Or install individually:
```bash
pip install pytest pytest-cov pytest-mock
```

## Running Tests

### Run all tests
```bash
pytest
```

### Run tests with verbose output
```bash
pytest -v
```

### Run a specific test file
```bash
pytest test_config.py
pytest test_input_handlers.py
pytest test_gamepad_controller.py
pytest test_input_listeners.py
pytest test_cursor_manager.py
```

### Run a specific test class
```bash
pytest test_config.py::TestConfig
pytest test_input_handlers.py::TestInputHandler
```

### Run a specific test method
```bash
pytest test_config.py::TestConfig::test_default_values
pytest test_input_handlers.py::TestInputHandler::test_on_key_press_toggle
```

### Run tests with coverage report
```bash
pytest --cov=. --cov-report=html
```

This will generate an HTML coverage report in the `htmlcov/` directory.

### Run tests with coverage summary
```bash
pytest --cov=. --cov-report=term-missing
```

## Test Coverage

The test suite covers:

- ✅ Configuration management and default values
- ✅ Key/mouse input parsing and handling
- ✅ Gamepad controller activation/deactivation
- ✅ Joystick and trigger processing
- ✅ Mouse movement translation to right stick
- ✅ Input suppression logic
- ✅ Cursor management (hide/show/lock)
- ✅ Error handling and edge cases
- ✅ Recoil control and sensitivity multipliers
- ✅ Rate limiting and update intervals

## Test Structure

All tests use:
- **unittest** framework (Python standard library)
- **unittest.mock** for mocking external dependencies
- Proper setUp/tearDown for test isolation

## Continuous Integration

These tests can be integrated into CI/CD pipelines:

```yaml
# Example GitHub Actions
- name: Run tests
  run: |
    pip install -r requirements-test.txt
    pytest --cov=. --cov-report=xml
```

## Notes

- Tests mock Windows API calls (ctypes.windll) to run on any platform
- Tests mock vgamepad library to avoid requiring virtual gamepad drivers
- Tests mock pynput listeners to avoid requiring actual input devices
- All tests are isolated and can run in any order

## Troubleshooting

**Import errors**: Make sure you're running tests from the correct directory:
```bash
cd c:\Users\Rodrigo\Documents\InputVSA\ControllerEmulator\ControllerEmulator
pytest
```

**Missing dependencies**: Install test requirements:
```bash
pip install -r requirements-test.txt
```

**Coverage issues**: Ensure pytest-cov is installed:
```bash
pip install pytest-cov
```

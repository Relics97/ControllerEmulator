@echo off
REM Batch script to run ControllerEmulator unit tests on Windows

echo ========================================
echo   ControllerEmulator - Unit Tests
echo ========================================
echo.

REM Check if pytest is available
python -m pytest --version >nul 2>&1
if %errorlevel% equ 0 (
    echo Using pytest...
    python -m pytest -v
) else (
    echo pytest not found, using unittest...
    python run_tests.py
)

echo.
pause

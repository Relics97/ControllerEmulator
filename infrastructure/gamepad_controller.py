"""
Core gamepad controller that handles input processing and gamepad emulation.
"""
import time
import math
import threading
from typing import Optional

import vgamepad as vg

from config.config import Config
from infrastructure.cursor_manager import CursorManager


class GamepadController:
    """Main controller for gamepad emulation and input processing."""
    
    def __init__(self):
        """Initialize the gamepad controller."""
        # Core state
        self._gamepad: Optional[vg.VX360Gamepad] = None
        self._active = False
        self._lock = threading.RLock()
        
        # Cursor management
        self.cursor_manager = CursorManager()
        
        # Mouse state
        self.mouse_dx = 0.0
        self.mouse_dy = 0.0
        
        # Input state
        self.keys = {k: False for k in Config.KEY_MAPPINGS.keys()}
        self.joystick_keys = {k: False for k in Config.JOYSTICK_KEYS}
        
        # Gamepad state
        self.last_lx = 0.0
        self.last_ly = 0.0
        self.last_rx = 0.0
        self.last_ry = 0.0
        self.r2_held = False  # Right mouse (ADS)
        self.l2_held = False  # Left mouse (Fire)
        
        # Timing
        self._last_update = time.time()
        self._update_interval = 1.0 / Config.UPDATE_RATE_HZ
        
        # Input listeners (set externally)
        self.mouse_listener = None
        self.keyboard_listener = None
        
        print("[CONTROLLER] Initialized")
        
        # Initialize virtual gamepad immediately so games can detect it
        self.initialize_gamepad()
    
    @property
    def active(self) -> bool:
        """Check if controller is currently active."""
        return self._active
    
    def initialize_gamepad(self) -> bool:
        """Initialize the virtual gamepad."""
        try:
            if self._gamepad is None:
                self._gamepad = vg.VX360Gamepad()
                print("[CONTROLLER] Virtual gamepad created")
            return True
        except Exception as e:
            print(f"[ERROR] Failed to initialize gamepad: {e}")
            return False
    
    def activate(self) -> bool:
        """Activate controller mode with input blocking."""
        with self._lock:
            if self._active:
                return True
            
            print("\n=== ACTIVATING CONTROLLER MODE ===")
            
            if not self.initialize_gamepad():
                return False
            
            # Send wake-up signal FIRST, before blocking keyboard
            # This ensures controller input is detected before any keyboard suppression happens
            if self._gamepad:
                # Send multiple signals: joystick movement + button press
                # This combo forces even stubborn games to recognize controller mode
                for i in range(2):
                    # Right joystick movement (camera)
                    self._gamepad.right_joystick_float(x_value_float=0.5, y_value_float=0.0)
                    # Press and release a button (BACK button is least intrusive)
                    self._gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_BACK)
                    self._gamepad.update()
                    time.sleep(0.03)
                    
                    # Reset everything
                    self._gamepad.right_joystick_float(x_value_float=0.0, y_value_float=0.0)
                    self._gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_BACK)
                    self._gamepad.update()
                    time.sleep(0.03)
                print("[CONTROLLER] Sent wake-up signal to force controller mode")
            
            # NOW enable input suppression (after controller wake-up)
            if self.mouse_listener and hasattr(self.mouse_listener, 'suppress_events'):
                self.mouse_listener.suppress_events(True)
            if self.keyboard_listener and hasattr(self.keyboard_listener, 'suppress_events'):
                self.keyboard_listener.suppress_events(True)
            
            # Lock and hide cursor
            self.cursor_manager.lock_to_center()
            self.cursor_manager.hide_cursor()
            
            self._active = True
            
            print("[CONTROLLER] Activated - Input blocking enabled")
            return True
    
    def deactivate(self):
        """Deactivate controller mode and restore normal input."""
        with self._lock:
            if not self._active:
                return
            
            print("\n=== DEACTIVATING CONTROLLER MODE ===")
            
            self._active = False
            
            # Reset all gamepad inputs
            self._reset_gamepad()
            
            # Clear all key states
            for key in self.joystick_keys:
                self.joystick_keys[key] = False
            for key in self.keys:
                self.keys[key] = False
            
            # Disable input suppression
            if self.mouse_listener and hasattr(self.mouse_listener, 'suppress_events'):
                self.mouse_listener.suppress_events(False)
            if self.keyboard_listener and hasattr(self.keyboard_listener, 'suppress_events'):
                self.keyboard_listener.suppress_events(False)
            
            # Show cursor again
            self.cursor_manager.show_cursor()
            
            print("[CONTROLLER] Deactivated - Normal input restored")
    
    def _reset_gamepad(self):
        """Reset all gamepad controls to neutral state."""
        if not self._gamepad:
            return
        
        try:
            self._gamepad.left_joystick_float(x_value_float=0.0, y_value_float=0.0)
            self._gamepad.right_joystick_float(x_value_float=0.0, y_value_float=0.0)
            for button in Config.KEY_MAPPINGS.values():
                self._gamepad.release_button(button=button)
            self._gamepad.left_trigger_float(0.0)
            self._gamepad.right_trigger_float(0.0)
            self._gamepad.update()
        except Exception as e:
            print(f"[ERROR] Failed to reset gamepad: {e}")
    
    def process_inputs(self):
        """Process all inputs and update gamepad state."""
        current_time = time.time()
        if current_time - self._last_update < self._update_interval:
            return
        
        self._last_update = current_time
        
        with self._lock:
            if self._gamepad is None:
                return
            
            # Keep gamepad connected even when inactive
            # Only process actual inputs when active
            if self._active:
                self._process_left_joystick()
                self._process_right_joystick()
                self._process_buttons()
                self._process_triggers()
            
            # Always update gamepad to maintain connection
            self._gamepad.update()
    
    def _process_left_joystick(self):
        """Process WASD movement for left joystick."""
        lx, ly = 0.0, 0.0
        any_key = False
        
        for key in Config.JOYSTICK_KEYS:
            if self.joystick_keys.get(key, False):
                any_key = True
                if key == 'd':
                    lx += 1.0
                elif key == 'a':
                    lx -= 1.0
                elif key == 'w':
                    ly += 1.0
                elif key == 's':
                    ly -= 1.0
        
        # Normalize diagonal movement
        if lx != 0 and ly != 0:
            magnitude = math.sqrt(lx * lx + ly * ly)
            lx /= magnitude
            ly /= magnitude
        
        # Reset if no keys pressed
        if not any_key:
            lx, ly = 0.0, 0.0
        
        self._gamepad.left_joystick_float(x_value_float=lx, y_value_float=ly)
        self.last_lx, self.last_ly = lx, ly
    
    def _process_right_joystick(self):
        """Process mouse movement for right joystick."""
        dx, dy = self._get_mouse_movement()
        
        # Apply recoil control when firing
        if Config.RECOIL_CONTROL_ENABLED and self.l2_held:
            dy += Config.RECOIL_COMPENSATION
        
        # Apply sensitivity
        sens_multiplier = Config.ADS_SENS_MULTIPLIER if self.r2_held else 1.0
        rx = dx * Config.SENS_X * sens_multiplier * Config.DPI_SCALING
        ry = -dy * Config.SENS_Y * sens_multiplier * Config.DPI_SCALING  # Invert Y
        
        # Apply deadzone
        rx = rx if abs(rx) > Config.DEADZONE else 0.0
        ry = ry if abs(ry) > Config.DEADZONE else 0.0
        
        # Apply smoothing
        rx = self.last_rx * Config.SMOOTHING + rx * (1.0 - Config.SMOOTHING)
        ry = self.last_ry * Config.SMOOTHING + ry * (1.0 - Config.SMOOTHING)
        
        # Clamp to valid range
        rx = max(-1.0, min(1.0, rx))
        ry = max(-1.0, min(1.0, ry))
        
        self._gamepad.right_joystick_float(x_value_float=rx, y_value_float=ry)
        self.last_rx, self.last_ry = rx, ry
    
    def _process_buttons(self):
        """Process button states."""
        for key, button in Config.KEY_MAPPINGS.items():
            current_state = self.keys.get(key, False)
            if current_state:
                self._gamepad.press_button(button=button)
            else:
                self._gamepad.release_button(button=button)
    
    def _process_triggers(self):
        """Process trigger states."""
        if self.l2_held:
            self._gamepad.right_trigger_float(1.0)
        else:
            self._gamepad.right_trigger_float(0.0)
        
        if self.r2_held:
            self._gamepad.left_trigger_float(1.0)
        else:
            self._gamepad.left_trigger_float(0.0)
    
    def _get_mouse_movement(self) -> tuple:
        """Get and reset mouse movement deltas."""
        dx, dy = self.mouse_dx, self.mouse_dy
        self.mouse_dx = 0.0
        self.mouse_dy = 0.0
        return dx, dy
    
    def update_rate(self, new_rate: int):
        """Update the processing rate."""
        Config.UPDATE_RATE_HZ = new_rate
        self._update_interval = 1.0 / new_rate
    
    def shutdown(self):
        """Clean shutdown of the gamepad controller."""
        self.deactivate()
        if self._gamepad:
            try:
                self._gamepad.reset()
                self._gamepad.update()
            except:
                pass
            self._gamepad = None
        print("[CONTROLLER] Shutdown complete")

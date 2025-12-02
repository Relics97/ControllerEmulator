"""
Unit tests for the GamepadController module.
"""
import unittest
from unittest.mock import MagicMock, patch, PropertyMock
import time
import math

from infrastructure.gamepad_controller import GamepadController
from config.config import Config


class TestGamepadController(unittest.TestCase):
    """Test cases for GamepadController class."""
    
    def setUp(self):
        """Set up test fixtures."""
        Config.reset_to_defaults()
        
        # Mock vgamepad
        self.mock_gamepad = MagicMock()
        self.mock_cursor_manager = MagicMock()
        
        with patch('infrastructure.gamepad_controller.vg.VX360Gamepad', return_value=self.mock_gamepad):
            with patch('infrastructure.gamepad_controller.CursorManager', return_value=self.mock_cursor_manager):
                self.controller = GamepadController()
    
    def test_initialization(self):
        """Test that GamepadController initializes correctly."""
        self.assertFalse(self.controller.active)
        self.assertIsNotNone(self.controller.cursor_manager)
        self.assertEqual(self.controller.mouse_dx, 0.0)
        self.assertEqual(self.controller.mouse_dy, 0.0)
        self.assertFalse(self.controller.r2_held)
        self.assertFalse(self.controller.l2_held)
    
    def test_active_property(self):
        """Test active property getter."""
        self.assertFalse(self.controller.active)
        self.controller._active = True
        self.assertTrue(self.controller.active)
    
    def test_initialize_gamepad(self):
        """Test gamepad initialization."""
        self.controller._gamepad = None
        
        with patch('infrastructure.gamepad_controller.vg.VX360Gamepad', return_value=self.mock_gamepad):
            result = self.controller.initialize_gamepad()
        
        self.assertTrue(result)
        self.assertIsNotNone(self.controller._gamepad)
    
    def test_initialize_gamepad_already_initialized(self):
        """Test that gamepad is not re-initialized if already exists."""
        self.controller._gamepad = self.mock_gamepad
        
        result = self.controller.initialize_gamepad()
        
        self.assertTrue(result)
        self.assertEqual(self.controller._gamepad, self.mock_gamepad)
    
    def test_initialize_gamepad_failure(self):
        """Test gamepad initialization failure handling."""
        self.controller._gamepad = None
        
        with patch('infrastructure.gamepad_controller.vg.VX360Gamepad', side_effect=Exception("Test error")):
            result = self.controller.initialize_gamepad()
        
        self.assertFalse(result)
    
    def test_activate(self):
        """Test controller activation."""
        self.controller._gamepad = self.mock_gamepad
        self.controller.mouse_listener = MagicMock()
        self.controller.keyboard_listener = MagicMock()
        
        result = self.controller.activate()
        
        self.assertTrue(result)
        self.assertTrue(self.controller.active)
        self.controller.mouse_listener.suppress_events.assert_called_once_with(True)
        self.controller.keyboard_listener.suppress_events.assert_called_once_with(True)
        self.mock_cursor_manager.lock_to_center.assert_called_once()
        self.mock_cursor_manager.hide_cursor.assert_called_once()
        self.mock_gamepad.update.assert_called()
    
    def test_activate_already_active(self):
        """Test that activate returns early if already active."""
        self.controller._active = True
        
        result = self.controller.activate()
        
        self.assertTrue(result)
    
    def test_deactivate(self):
        """Test controller deactivation."""
        self.controller._active = True
        self.controller._gamepad = self.mock_gamepad
        self.controller.mouse_listener = MagicMock()
        self.controller.keyboard_listener = MagicMock()
        
        self.controller.deactivate()
        
        self.assertFalse(self.controller.active)
        self.controller.mouse_listener.suppress_events.assert_called_once_with(False)
        self.controller.keyboard_listener.suppress_events.assert_called_once_with(False)
        self.mock_cursor_manager.show_cursor.assert_called_once()
    
    def test_deactivate_already_inactive(self):
        """Test that deactivate returns early if already inactive."""
        self.controller._active = False
        
        self.controller.deactivate()
        
        self.assertFalse(self.controller.active)
    
    def test_reset_gamepad(self):
        """Test gamepad reset."""
        self.controller._gamepad = self.mock_gamepad
        
        self.controller._reset_gamepad()
        
        self.mock_gamepad.left_joystick_float.assert_called_with(x_value_float=0.0, y_value_float=0.0)
        self.mock_gamepad.right_joystick_float.assert_called_with(x_value_float=0.0, y_value_float=0.0)
        self.mock_gamepad.left_trigger_float.assert_called_with(0.0)
        self.mock_gamepad.right_trigger_float.assert_called_with(0.0)
        self.mock_gamepad.update.assert_called()
    
    def test_process_left_joystick_no_keys(self):
        """Test left joystick with no keys pressed."""
        self.controller._active = True
        self.controller._gamepad = self.mock_gamepad
        self.controller.joystick_keys = {k: False for k in Config.JOYSTICK_KEYS}
        
        self.controller._process_left_joystick()
        
        self.mock_gamepad.left_joystick_float.assert_called_with(x_value_float=0.0, y_value_float=0.0)
    
    def test_process_left_joystick_w_key(self):
        """Test left joystick with W key pressed."""
        self.controller._active = True
        self.controller._gamepad = self.mock_gamepad
        self.controller.joystick_keys = {'w': True, 'a': False, 's': False, 'd': False}
        
        self.controller._process_left_joystick()
        
        self.mock_gamepad.left_joystick_float.assert_called_with(x_value_float=0.0, y_value_float=1.0)
    
    def test_process_left_joystick_diagonal_normalized(self):
        """Test left joystick diagonal movement is normalized."""
        self.controller._active = True
        self.controller._gamepad = self.mock_gamepad
        self.controller.joystick_keys = {'w': True, 'a': False, 's': False, 'd': True}
        
        self.controller._process_left_joystick()
        
        # Diagonal should be normalized
        expected_value = 1.0 / math.sqrt(2)
        call_args = self.mock_gamepad.left_joystick_float.call_args
        self.assertAlmostEqual(call_args[1]['x_value_float'], expected_value, places=5)
        self.assertAlmostEqual(call_args[1]['y_value_float'], expected_value, places=5)
    
    def test_process_right_joystick_no_movement(self):
        """Test right joystick with no mouse movement."""
        self.controller._active = True
        self.controller._gamepad = self.mock_gamepad
        self.controller.mouse_dx = 0.0
        self.controller.mouse_dy = 0.0
        
        self.controller._process_right_joystick()
        
        # Should call with near-zero values (due to smoothing/deadzone)
        call_args = self.mock_gamepad.right_joystick_float.call_args
        rx = call_args[1]['x_value_float']
        ry = call_args[1]['y_value_float']
        self.assertAlmostEqual(rx, 0.0, places=5)
        self.assertAlmostEqual(ry, 0.0, places=5)
    
    def test_process_right_joystick_with_movement(self):
        """Test right joystick with mouse movement."""
        self.controller._active = True
        self.controller._gamepad = self.mock_gamepad
        self.controller.mouse_dx = 100.0
        self.controller.mouse_dy = 50.0
        self.controller.r2_held = False
        self.controller.l2_held = False
        
        self.controller._process_right_joystick()
        
        # Should process movement
        self.mock_gamepad.right_joystick_float.assert_called()
        # Mouse deltas should be reset
        self.assertEqual(self.controller.mouse_dx, 0.0)
        self.assertEqual(self.controller.mouse_dy, 0.0)
    
    def test_process_right_joystick_ads_sensitivity(self):
        """Test right joystick applies ADS sensitivity multiplier."""
        self.controller._active = True
        self.controller._gamepad = self.mock_gamepad
        # Use smaller mouse movement to avoid clamping at 1.0
        self.controller.mouse_dx = 10.0
        self.controller.mouse_dy = 0.0
        self.controller.r2_held = False
        self.controller.l2_held = False
        
        # Normal sensitivity
        self.controller._process_right_joystick()
        call_args_normal = self.mock_gamepad.right_joystick_float.call_args
        rx_normal = abs(call_args_normal[1]['x_value_float'])
        
        # Reset state with same small movement
        self.controller.mouse_dx = 10.0
        self.controller.last_rx = 0.0
        self.controller.r2_held = True  # ADS active
        
        # ADS sensitivity
        self.controller._process_right_joystick()
        call_args_ads = self.mock_gamepad.right_joystick_float.call_args
        rx_ads = abs(call_args_ads[1]['x_value_float'])
        
        # ADS should be slower (multiplier is 0.9)
        self.assertLess(rx_ads, rx_normal)
    
    def test_process_right_joystick_recoil_control(self):
        """Test right joystick applies recoil control when firing."""
        self.controller._active = True
        self.controller._gamepad = self.mock_gamepad
        self.controller.mouse_dx = 0.0
        self.controller.mouse_dy = 0.0
        self.controller.l2_held = True  # Firing
        self.controller.r2_held = False
        Config.RECOIL_CONTROL_ENABLED = True
        
        self.controller._process_right_joystick()
        
        # Should have applied recoil compensation
        call_args = self.mock_gamepad.right_joystick_float.call_args
        ry = call_args[1]['y_value_float']
        # Y should be affected by recoil compensation
        self.assertNotEqual(ry, 0.0)
    
    def test_process_buttons(self):
        """Test button processing."""
        self.controller._active = True
        self.controller._gamepad = self.mock_gamepad
        self.controller.keys = {k: False for k in Config.KEY_MAPPINGS.keys()}
        self.controller.keys['space'] = True
        self.controller.keys['r'] = True
        
        self.controller._process_buttons()
        
        # Should press active buttons and release inactive ones
        press_calls = [call for call in self.mock_gamepad.press_button.call_args_list]
        release_calls = [call for call in self.mock_gamepad.release_button.call_args_list]
        
        self.assertGreater(len(press_calls), 0)
        self.assertGreater(len(release_calls), 0)
    
    def test_process_triggers_l2(self):
        """Test left trigger (fire) processing."""
        self.controller._active = True
        self.controller._gamepad = self.mock_gamepad
        self.controller.l2_held = True
        self.controller.r2_held = False
        
        self.controller._process_triggers()
        
        # L2 maps to right trigger
        self.mock_gamepad.right_trigger_float.assert_called_with(1.0)
        self.mock_gamepad.left_trigger_float.assert_called_with(0.0)
    
    def test_process_triggers_r2(self):
        """Test right trigger (ADS) processing."""
        self.controller._active = True
        self.controller._gamepad = self.mock_gamepad
        self.controller.l2_held = False
        self.controller.r2_held = True
        
        self.controller._process_triggers()
        
        # R2 maps to left trigger
        self.mock_gamepad.left_trigger_float.assert_called_with(1.0)
        self.mock_gamepad.right_trigger_float.assert_called_with(0.0)
    
    def test_get_mouse_movement(self):
        """Test getting and resetting mouse movement."""
        self.controller.mouse_dx = 100.0
        self.controller.mouse_dy = 50.0
        
        dx, dy = self.controller._get_mouse_movement()
        
        self.assertEqual(dx, 100.0)
        self.assertEqual(dy, 50.0)
        # Should reset
        self.assertEqual(self.controller.mouse_dx, 0.0)
        self.assertEqual(self.controller.mouse_dy, 0.0)
    
    def test_update_rate(self):
        """Test updating the processing rate."""
        self.controller.update_rate(60)
        
        self.assertEqual(Config.UPDATE_RATE_HZ, 60)
        self.assertAlmostEqual(self.controller._update_interval, 1.0 / 60)
    
    def test_process_inputs_inactive(self):
        """Test that process_inputs still updates gamepad when inactive to maintain connection."""
        self.controller._active = False
        self.controller._gamepad = self.mock_gamepad
        
        # Force time to pass for rate limiting
        self.controller._last_update = 0
        
        self.controller.process_inputs()
        
        # Should still call update to maintain gamepad connection even when inactive
        self.mock_gamepad.update.assert_called_once()
    
    def test_process_inputs_rate_limiting(self):
        """Test that process_inputs respects update rate."""
        self.controller._active = True
        self.controller._gamepad = self.mock_gamepad
        self.controller._last_update = time.time()
        
        # Call immediately - should skip due to rate limiting
        self.controller.process_inputs()
        self.mock_gamepad.update.assert_not_called()
        
        # Wait for interval to pass
        self.controller._last_update = time.time() - 1.0
        self.controller.process_inputs()
        self.mock_gamepad.update.assert_called()
    
    def test_shutdown(self):
        """Test controller shutdown."""
        self.controller._active = True
        self.controller._gamepad = self.mock_gamepad
        
        self.controller.shutdown()
        
        self.assertFalse(self.controller.active)
        self.mock_gamepad.reset.assert_called_once()
        self.mock_gamepad.update.assert_called()
        self.assertIsNone(self.controller._gamepad)
    
    def test_shutdown_with_exception(self):
        """Test shutdown handles gamepad reset exceptions."""
        self.controller._active = True
        self.controller._gamepad = self.mock_gamepad
        self.mock_gamepad.reset.side_effect = Exception("Test error")
        
        # Should not raise exception
        try:
            self.controller.shutdown()
        except Exception:
            self.fail("shutdown raised exception when it should handle errors")
        
        self.assertIsNone(self.controller._gamepad)


if __name__ == '__main__':
    unittest.main()

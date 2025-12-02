"""
Unit tests for the InputHandler module.
"""
import unittest
from unittest.mock import MagicMock, patch, PropertyMock
from pynput import keyboard, mouse

from application.input_handlers import InputHandler
from config.config import Config


class TestInputHandler(unittest.TestCase):
    """Test cases for InputHandler class."""
    
    def setUp(self):
        """Set up test fixtures."""
        Config.reset_to_defaults()
        self.mock_controller = MagicMock()
        self.mock_controller.active = False
        self.mock_controller.joystick_keys = {k: False for k in Config.JOYSTICK_KEYS}
        self.mock_controller.keys = {k: False for k in Config.KEY_MAPPINGS.keys()}
        self.mock_controller.cursor_manager = MagicMock()
        self.mock_controller.cursor_manager.center_x = 960
        self.mock_controller.cursor_manager.center_y = 540
        self.mock_controller.mouse_dx = 0.0
        self.mock_controller.mouse_dy = 0.0
        self.mock_controller.l2_held = False
        self.mock_controller.r2_held = False
        
        self.handler = InputHandler(self.mock_controller)
    
    def test_initialization(self):
        """Test that InputHandler initializes correctly."""
        self.assertIsNotNone(self.handler.controller)
        self.assertEqual(self.handler.controller, self.mock_controller)
    
    def test_parse_key_character(self):
        """Test parsing of regular character keys."""
        # Mock a character key
        mock_key = MagicMock()
        mock_key.char = 'a'
        
        result = InputHandler._parse_key(mock_key)
        self.assertEqual(result, 'a')
    
    def test_parse_key_uppercase(self):
        """Test that uppercase keys are converted to lowercase."""
        mock_key = MagicMock()
        mock_key.char = 'W'
        
        result = InputHandler._parse_key(mock_key)
        self.assertEqual(result, 'w')
    
    def test_parse_key_space(self):
        """Test parsing of space key."""
        result = InputHandler._parse_key(keyboard.Key.space)
        self.assertEqual(result, 'space')
    
    def test_parse_key_escape(self):
        """Test parsing of escape key."""
        result = InputHandler._parse_key(keyboard.Key.esc)
        self.assertEqual(result, 'esc')
    
    def test_parse_key_tab(self):
        """Test parsing of tab key."""
        result = InputHandler._parse_key(keyboard.Key.tab)
        self.assertEqual(result, 'tab')
    
    def test_parse_key_shift(self):
        """Test parsing of shift key."""
        result = InputHandler._parse_key(keyboard.Key.shift)
        self.assertEqual(result, 'shift')
    
    def test_parse_key_alt_left(self):
        """Test parsing of left alt key."""
        result = InputHandler._parse_key(keyboard.Key.alt_l)
        self.assertEqual(result, 'alt_l')
    
    def test_on_key_press_toggle(self):
        """Test that toggle key activates/deactivates controller."""
        mock_key = MagicMock()
        mock_key.char = 't'
        
        # First press - activate
        self.mock_controller.active = False
        self.handler.on_key_press(mock_key)
        self.mock_controller.activate.assert_called_once()
        
        # Second press - deactivate
        self.mock_controller.reset_mock()
        self.mock_controller.active = True
        self.handler.on_key_press(mock_key)
        self.mock_controller.deactivate.assert_called_once()
    
    def test_on_key_press_joystick_key(self):
        """Test that joystick keys are registered."""
        mock_key = MagicMock()
        mock_key.char = 'w'
        
        self.handler.on_key_press(mock_key)
        self.assertTrue(self.mock_controller.joystick_keys['w'])
    
    def test_on_key_press_mapped_key(self):
        """Test that mapped keys are registered."""
        mock_key = MagicMock()
        mock_key.char = None
        
        # Test space key
        self.handler.on_key_press(keyboard.Key.space)
        self.assertTrue(self.mock_controller.keys['space'])
    
    def test_on_key_release_joystick_key(self):
        """Test that joystick key release is registered."""
        mock_key = MagicMock()
        mock_key.char = 'w'
        
        # Press then release
        self.handler.on_key_press(mock_key)
        self.assertTrue(self.mock_controller.joystick_keys['w'])
        
        self.handler.on_key_release(mock_key)
        self.assertFalse(self.mock_controller.joystick_keys['w'])
    
    def test_on_key_release_mapped_key(self):
        """Test that mapped key release is registered."""
        # Press then release
        self.handler.on_key_press(keyboard.Key.space)
        self.assertTrue(self.mock_controller.keys['space'])
        
        self.handler.on_key_release(keyboard.Key.space)
        self.assertFalse(self.mock_controller.keys['space'])
    
    def test_on_mouse_move_inactive(self):
        """Test that mouse movement is ignored when controller is inactive."""
        self.mock_controller.active = False
        
        self.handler.on_mouse_move(100, 200)
        
        # Should not modify mouse deltas
        self.assertEqual(self.mock_controller.mouse_dx, 0.0)
        self.assertEqual(self.mock_controller.mouse_dy, 0.0)
    
    def test_on_mouse_move_active(self):
        """Test that mouse movement is captured when controller is active."""
        self.mock_controller.active = True
        
        # Simulate mouse movement
        self.handler.on_mouse_move(1000, 600)
        
        # Should accumulate deltas from center
        expected_dx = 1000 - 960  # 40
        expected_dy = 600 - 540   # 60
        self.assertEqual(self.mock_controller.mouse_dx, expected_dx)
        self.assertEqual(self.mock_controller.mouse_dy, expected_dy)
        
        # Should lock cursor to center
        self.mock_controller.cursor_manager.lock_to_center.assert_called_once()
    
    def test_on_mouse_move_accumulation(self):
        """Test that mouse movements accumulate."""
        self.mock_controller.active = True
        
        # First movement
        self.handler.on_mouse_move(1000, 600)
        first_dx = self.mock_controller.mouse_dx
        first_dy = self.mock_controller.mouse_dy
        
        # Second movement (should accumulate)
        self.handler.on_mouse_move(1020, 620)
        
        self.assertEqual(self.mock_controller.mouse_dx, first_dx + 60)  # 1020 - 960
        self.assertEqual(self.mock_controller.mouse_dy, first_dy + 80)  # 620 - 540
    
    def test_on_mouse_click_left_button(self):
        """Test that left mouse button sets l2_held."""
        # Press
        self.handler.on_mouse_click(0, 0, mouse.Button.left, True)
        self.assertTrue(self.mock_controller.l2_held)
        
        # Release
        self.handler.on_mouse_click(0, 0, mouse.Button.left, False)
        self.assertFalse(self.mock_controller.l2_held)
    
    def test_on_mouse_click_right_button(self):
        """Test that right mouse button sets r2_held."""
        # Press
        self.handler.on_mouse_click(0, 0, mouse.Button.right, True)
        self.assertTrue(self.mock_controller.r2_held)
        
        # Release
        self.handler.on_mouse_click(0, 0, mouse.Button.right, False)
        self.assertFalse(self.mock_controller.r2_held)
    
    def test_on_mouse_click_middle_button(self):
        """Test that middle mouse button is ignored."""
        # Press middle button
        self.handler.on_mouse_click(0, 0, mouse.Button.middle, True)
        
        # Should not affect triggers
        self.assertFalse(self.mock_controller.l2_held)
        self.assertFalse(self.mock_controller.r2_held)
    
    def test_on_key_press_error_handling(self):
        """Test that key press errors are handled gracefully."""
        # Create a problematic key that will raise an exception
        mock_key = MagicMock()
        mock_key.char = None
        mock_key.__str__ = MagicMock(side_effect=Exception("Test error"))
        
        # Should not raise exception
        try:
            self.handler.on_key_press(mock_key)
        except Exception:
            self.fail("on_key_press raised exception when it should handle errors")
    
    def test_on_key_release_error_handling(self):
        """Test that key release errors are handled gracefully."""
        # Create a problematic key that will raise an exception
        mock_key = MagicMock()
        mock_key.char = None
        mock_key.__str__ = MagicMock(side_effect=Exception("Test error"))
        
        # Should not raise exception
        try:
            self.handler.on_key_release(mock_key)
        except Exception:
            self.fail("on_key_release raised exception when it should handle errors")


if __name__ == '__main__':
    unittest.main()

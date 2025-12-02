"""
Unit tests for the Config module.
"""
import unittest
from unittest.mock import patch, MagicMock
import vgamepad as vg

from config.config import Config


class TestConfig(unittest.TestCase):
    """Test cases for Config class."""
    
    def setUp(self):
        """Reset config to defaults before each test."""
        Config.reset_to_defaults()
    
    def test_default_values(self):
        """Test that default configuration values are set correctly."""
        self.assertEqual(Config.UPDATE_RATE_HZ, 120)
        self.assertEqual(Config.DPI_SCALING, 0.013)
        self.assertEqual(Config.SENS_X, 1.0)
        self.assertEqual(Config.SENS_Y, 1.0)
        self.assertEqual(Config.ADS_SENS_MULTIPLIER, 0.9)
        self.assertEqual(Config.DEADZONE, 0.0012)
        self.assertEqual(Config.SMOOTHING, 0.0)
        self.assertTrue(Config.RECOIL_CONTROL_ENABLED)
        self.assertEqual(Config.RECOIL_COMPENSATION, 1.8)
        self.assertEqual(Config.TOGGLE_KEY, 't')
    
    def test_joystick_keys(self):
        """Test that joystick keys are correctly defined."""
        expected_keys = ['w', 'a', 's', 'd']
        self.assertEqual(Config.JOYSTICK_KEYS, expected_keys)
    
    def test_key_mappings_exist(self):
        """Test that all essential key mappings are defined."""
        essential_keys = [
            'space', 'c', 'r', '1', '2', 'alt_l', 'b', '3',
            'q', 'e', 'esc', 'tab', 'shift', 'f'
        ]
        for key in essential_keys:
            self.assertIn(key, Config.KEY_MAPPINGS)
    
    def test_key_mappings_values(self):
        """Test that key mappings use correct Xbox button values."""
        self.assertEqual(Config.KEY_MAPPINGS['space'], vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
        self.assertEqual(Config.KEY_MAPPINGS['c'], vg.XUSB_BUTTON.XUSB_GAMEPAD_B)
        self.assertEqual(Config.KEY_MAPPINGS['r'], vg.XUSB_BUTTON.XUSB_GAMEPAD_X)
        self.assertEqual(Config.KEY_MAPPINGS['1'], vg.XUSB_BUTTON.XUSB_GAMEPAD_Y)
        self.assertEqual(Config.KEY_MAPPINGS['q'], vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER)
        self.assertEqual(Config.KEY_MAPPINGS['e'], vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_SHOULDER)
        self.assertEqual(Config.KEY_MAPPINGS['esc'], vg.XUSB_BUTTON.XUSB_GAMEPAD_START)
        self.assertEqual(Config.KEY_MAPPINGS['tab'], vg.XUSB_BUTTON.XUSB_GAMEPAD_BACK)
    
    def test_reset_to_defaults(self):
        """Test that reset_to_defaults restores all values."""
        # Modify some values
        Config.UPDATE_RATE_HZ = 60
        Config.ADS_SENS_MULTIPLIER = 2.0
        Config.RECOIL_COMPENSATION = 3.0
        Config.TOGGLE_KEY = 'x'
        Config.KEY_MAPPINGS = {}
        
        # Reset
        Config.reset_to_defaults()
        
        # Verify defaults restored
        self.assertEqual(Config.UPDATE_RATE_HZ, 120)
        self.assertEqual(Config.ADS_SENS_MULTIPLIER, 0.9)
        self.assertEqual(Config.RECOIL_COMPENSATION, 1.8)
        self.assertEqual(Config.TOGGLE_KEY, 't')
        self.assertNotEqual(Config.KEY_MAPPINGS, {})
    
    def test_sensitivity_values_valid(self):
        """Test that sensitivity values are positive."""
        self.assertGreater(Config.SENS_X, 0)
        self.assertGreater(Config.SENS_Y, 0)
        self.assertGreater(Config.DPI_SCALING, 0)
    
    def test_deadzone_value_valid(self):
        """Test that deadzone is within valid range."""
        self.assertGreaterEqual(Config.DEADZONE, 0.0)
        self.assertLessEqual(Config.DEADZONE, 1.0)
    
    def test_smoothing_value_valid(self):
        """Test that smoothing is within valid range."""
        self.assertGreaterEqual(Config.SMOOTHING, 0.0)
        self.assertLessEqual(Config.SMOOTHING, 1.0)
    
    def test_update_rate_positive(self):
        """Test that update rate is positive."""
        self.assertGreater(Config.UPDATE_RATE_HZ, 0)


if __name__ == '__main__':
    unittest.main()

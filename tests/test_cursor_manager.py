"""
Unit tests for the CursorManager module.
"""
import unittest
from unittest.mock import MagicMock, patch, PropertyMock
import ctypes

from infrastructure.cursor_manager import CursorManager


class TestCursorManager(unittest.TestCase):
    """Test cases for CursorManager class."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Mock the Windows API functions
        self.mock_user32 = MagicMock()
        self.mock_user32.ShowCursor = MagicMock(return_value=0)
        self.mock_user32.SetCursor = MagicMock(return_value=1)
        self.mock_user32.LoadCursorW = MagicMock(return_value=12345)
        self.mock_user32.SetCursorPos = MagicMock(return_value=1)
        self.mock_user32.GetSystemMetrics = MagicMock(side_effect=[1920, 1080])  # Screen size
        
        with patch('ctypes.windll.user32', self.mock_user32):
            self.cursor_manager = CursorManager()
    
    def test_initialization_success(self):
        """Test that CursorManager initializes correctly."""
        self.assertTrue(self.cursor_manager.enabled)
        self.assertEqual(self.cursor_manager.center_x, 1920 // 2)
        self.assertEqual(self.cursor_manager.center_y, 1080 // 2)
    
    def test_initialization_failure(self):
        """Test handling of initialization failure."""
        # Mock windll to raise exception when accessing user32
        mock_windll = MagicMock()
        type(mock_windll).user32 = PropertyMock(side_effect=Exception("Test error"))
        
        with patch('ctypes.windll', mock_windll):
            cursor_manager = CursorManager()
            self.assertFalse(cursor_manager.enabled)
    
    def test_hide_cursor_success(self):
        """Test successfully hiding the cursor."""
        result = self.cursor_manager.hide_cursor()
        
        self.assertTrue(result)
        # ShowCursor should be called to decrement display count
        self.mock_user32.ShowCursor.assert_called()
        # SetCursor should be called with 0 to hide
        self.mock_user32.SetCursor.assert_called_with(0)
    
    def test_hide_cursor_when_disabled(self):
        """Test that hide_cursor returns False when disabled."""
        self.cursor_manager.enabled = False
        
        result = self.cursor_manager.hide_cursor()
        
        self.assertFalse(result)
        self.mock_user32.ShowCursor.assert_not_called()
    
    def test_hide_cursor_exception_handling(self):
        """Test that hide_cursor handles exceptions."""
        self.mock_user32.ShowCursor.side_effect = Exception("Test error")
        
        result = self.cursor_manager.hide_cursor()
        
        self.assertFalse(result)
    
    def test_hide_cursor_loop_termination(self):
        """Test that hide_cursor loop terminates properly."""
        # Set ShowCursor to return decreasing values, then negative
        self.mock_user32.ShowCursor.side_effect = [1, 0, -1, -2]
        
        result = self.cursor_manager.hide_cursor()
        
        self.assertTrue(result)
        # Should call until count goes negative
        self.assertGreater(self.mock_user32.ShowCursor.call_count, 0)
        self.assertLessEqual(self.mock_user32.ShowCursor.call_count, 100)
    
    def test_show_cursor_success(self):
        """Test successfully showing the cursor."""
        result = self.cursor_manager.show_cursor()
        
        self.assertTrue(result)
        # ShowCursor should be called to increment display count
        self.mock_user32.ShowCursor.assert_called()
        # LoadCursor and SetCursor should be called to restore arrow
        self.mock_user32.LoadCursorW.assert_called()
        self.mock_user32.SetCursor.assert_called()
    
    def test_show_cursor_when_disabled(self):
        """Test that show_cursor returns False when disabled."""
        self.cursor_manager.enabled = False
        
        result = self.cursor_manager.show_cursor()
        
        self.assertFalse(result)
        self.mock_user32.ShowCursor.assert_not_called()
    
    def test_show_cursor_exception_handling(self):
        """Test that show_cursor handles exceptions."""
        self.mock_user32.ShowCursor.side_effect = Exception("Test error")
        
        result = self.cursor_manager.show_cursor()
        
        self.assertFalse(result)
    
    def test_show_cursor_loop_termination(self):
        """Test that show_cursor loop terminates properly."""
        # Set ShowCursor to return increasing values from negative
        self.mock_user32.ShowCursor.side_effect = [-2, -1, 0, 1]
        
        result = self.cursor_manager.show_cursor()
        
        self.assertTrue(result)
        # Should call until count goes non-negative
        self.assertGreater(self.mock_user32.ShowCursor.call_count, 0)
        self.assertLessEqual(self.mock_user32.ShowCursor.call_count, 100)
    
    def test_show_cursor_loads_arrow_cursor(self):
        """Test that show_cursor loads the standard arrow cursor."""
        self.cursor_manager.show_cursor()
        
        # Should load arrow cursor with IDC_ARROW constant
        self.mock_user32.LoadCursorW.assert_called_with(0, self.cursor_manager.IDC_ARROW)
        # Should set the loaded cursor
        self.mock_user32.SetCursor.assert_called_with(12345)  # The return value from LoadCursorW
    
    def test_lock_to_center_success(self):
        """Test successfully locking cursor to center."""
        result = self.cursor_manager.lock_to_center()
        
        self.assertTrue(result)
        self.mock_user32.SetCursorPos.assert_called_with(
            self.cursor_manager.center_x,
            self.cursor_manager.center_y
        )
    
    def test_lock_to_center_when_disabled(self):
        """Test that lock_to_center returns False when disabled."""
        self.cursor_manager.enabled = False
        
        result = self.cursor_manager.lock_to_center()
        
        self.assertFalse(result)
        self.mock_user32.SetCursorPos.assert_not_called()
    
    def test_lock_to_center_exception_handling(self):
        """Test that lock_to_center handles exceptions."""
        self.mock_user32.SetCursorPos.side_effect = Exception("Test error")
        
        result = self.cursor_manager.lock_to_center()
        
        self.assertFalse(result)
    
    def test_lock_to_center_with_correct_coordinates(self):
        """Test that lock_to_center uses correct center coordinates."""
        # Set up with specific screen dimensions
        mock_user32 = MagicMock()
        mock_user32.GetSystemMetrics = MagicMock(side_effect=[2560, 1440])
        mock_user32.SetCursorPos = MagicMock(return_value=1)
        mock_user32.ShowCursor = MagicMock(return_value=0)
        mock_user32.SetCursor = MagicMock(return_value=1)
        mock_user32.LoadCursorW = MagicMock(return_value=1)
        
        with patch('ctypes.windll.user32', mock_user32):
            cursor_manager = CursorManager()
            cursor_manager.lock_to_center()
        
        # Should use center of 2560x1440 screen
        mock_user32.SetCursorPos.assert_called_with(1280, 720)
    
    def test_idc_arrow_constant(self):
        """Test that IDC_ARROW constant is correct."""
        self.assertEqual(self.cursor_manager.IDC_ARROW, 32512)
    
    def test_hide_show_cursor_sequence(self):
        """Test hiding and then showing cursor in sequence."""
        # Reset mock to track fresh calls
        self.mock_user32.ShowCursor.reset_mock()
        self.mock_user32.SetCursor.reset_mock()
        
        # Hide cursor
        result1 = self.cursor_manager.hide_cursor()
        self.assertTrue(result1)
        
        # Show cursor
        result2 = self.cursor_manager.show_cursor()
        self.assertTrue(result2)
        
        # Both operations should have completed
        self.assertGreater(self.mock_user32.ShowCursor.call_count, 0)
        self.assertGreater(self.mock_user32.SetCursor.call_count, 0)


if __name__ == '__main__':
    unittest.main()

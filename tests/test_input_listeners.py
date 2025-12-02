"""
Unit tests for the InputListener modules.
"""
import unittest
from unittest.mock import MagicMock, patch, call

from application.input_listeners import ConditionalSuppressMouseListener, ConditionalSuppressKeyboardListener


class TestConditionalSuppressMouseListener(unittest.TestCase):
    """Test cases for ConditionalSuppressMouseListener class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.on_move_callback = MagicMock()
        self.on_click_callback = MagicMock()
        self.on_scroll_callback = MagicMock()
        
        # Create listener without starting it
        with patch('application.input_listeners.mouse.Listener.__init__', return_value=None):
            self.listener = ConditionalSuppressMouseListener(
                on_move=self.on_move_callback,
                on_click=self.on_click_callback,
                on_scroll=self.on_scroll_callback
            )
    
    def test_initialization(self):
        """Test that mouse listener initializes correctly."""
        self.assertFalse(self.listener._suppress)
    
    def test_suppress_events_enable(self):
        """Test enabling event suppression."""
        self.listener.suppress_events(True)
        self.assertTrue(self.listener._suppress)
    
    def test_suppress_events_disable(self):
        """Test disabling event suppression."""
        self.listener._suppress = True
        self.listener.suppress_events(False)
        self.assertFalse(self.listener._suppress)
    
    def test_suppress_event_when_enabled(self):
        """Test that events are suppressed when suppression is enabled."""
        self.listener._suppress = True
        mock_event = MagicMock()
        
        result = self.listener._suppress_event(mock_event)
        
        self.assertTrue(result)
    
    def test_suppress_event_when_disabled(self):
        """Test that events are not suppressed when suppression is disabled."""
        self.listener._suppress = False
        mock_event = MagicMock()
        
        result = self.listener._suppress_event(mock_event)
        
        self.assertFalse(result)
    
    def test_toggle_suppression_multiple_times(self):
        """Test toggling suppression multiple times."""
        self.assertFalse(self.listener._suppress)
        
        self.listener.suppress_events(True)
        self.assertTrue(self.listener._suppress)
        
        self.listener.suppress_events(False)
        self.assertFalse(self.listener._suppress)
        
        self.listener.suppress_events(True)
        self.assertTrue(self.listener._suppress)


class TestConditionalSuppressKeyboardListener(unittest.TestCase):
    """Test cases for ConditionalSuppressKeyboardListener class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.on_press_callback = MagicMock()
        self.on_release_callback = MagicMock()
        
        # Create listener without starting it
        with patch('application.input_listeners.keyboard.Listener.__init__', return_value=None):
            self.listener = ConditionalSuppressKeyboardListener(
                on_press=self.on_press_callback,
                on_release=self.on_release_callback,
                toggle_key='t'
            )
    
    def test_initialization(self):
        """Test that keyboard listener initializes correctly."""
        self.assertFalse(self.listener._suppress)
        self.assertEqual(self.listener._toggle_key, 't')
    
    def test_suppress_events_enable(self):
        """Test enabling event suppression."""
        self.listener.suppress_events(True)
        self.assertTrue(self.listener._suppress)
    
    def test_suppress_events_disable(self):
        """Test disabling event suppression."""
        self.listener._suppress = True
        self.listener.suppress_events(False)
        self.assertFalse(self.listener._suppress)
    
    def test_set_toggle_key(self):
        """Test setting a new toggle key."""
        self.listener.set_toggle_key('x')
        self.assertEqual(self.listener._toggle_key, 'x')
    
    def test_suppress_event_when_enabled_non_toggle(self):
        """Test that non-toggle events are suppressed when suppression is enabled."""
        self.listener._suppress = True
        mock_event = MagicMock()
        mock_event.char = 'a'
        
        result = self.listener._suppress_event(mock_event)
        
        self.assertTrue(result)
    
    def test_suppress_event_when_disabled(self):
        """Test that events are not suppressed when suppression is disabled."""
        self.listener._suppress = False
        mock_event = MagicMock()
        mock_event.char = 'a'
        
        result = self.listener._suppress_event(mock_event)
        
        self.assertFalse(result)
    
    def test_suppress_event_toggle_key_never_suppressed(self):
        """Test that toggle key is never suppressed."""
        self.listener._suppress = True
        self.listener._toggle_key = 't'
        
        mock_event = MagicMock()
        mock_event.char = 't'
        
        result = self.listener._suppress_event(mock_event)
        
        self.assertFalse(result)
    
    def test_suppress_event_toggle_key_uppercase(self):
        """Test that uppercase toggle key is never suppressed."""
        self.listener._suppress = True
        self.listener._toggle_key = 't'
        
        mock_event = MagicMock()
        mock_event.char = 'T'
        
        result = self.listener._suppress_event(mock_event)
        
        # Should convert to lowercase and not suppress
        self.assertFalse(result)
    
    def test_suppress_event_special_key(self):
        """Test suppression of special keys (no char attribute)."""
        self.listener._suppress = True
        
        mock_event = MagicMock()
        del mock_event.char  # Special keys don't have char
        
        result = self.listener._suppress_event(mock_event)
        
        self.assertTrue(result)
    
    def test_suppress_event_exception_handling(self):
        """Test that exceptions in suppress check are handled."""
        self.listener._suppress = True
        
        mock_event = MagicMock()
        mock_event.char = MagicMock(side_effect=Exception("Test error"))
        
        # Should handle exception and return suppress state
        result = self.listener._suppress_event(mock_event)
        
        self.assertTrue(result)
    
    def test_toggle_suppression_multiple_times(self):
        """Test toggling suppression multiple times."""
        self.assertFalse(self.listener._suppress)
        
        self.listener.suppress_events(True)
        self.assertTrue(self.listener._suppress)
        
        self.listener.suppress_events(False)
        self.assertFalse(self.listener._suppress)
        
        self.listener.suppress_events(True)
        self.assertTrue(self.listener._suppress)
    
    def test_change_toggle_key_during_suppression(self):
        """Test changing toggle key while suppression is active."""
        self.listener._suppress = True
        self.listener._toggle_key = 't'
        
        # Old toggle key should be suppressed after change
        self.listener.set_toggle_key('x')
        
        mock_event_t = MagicMock()
        mock_event_t.char = 't'
        self.assertTrue(self.listener._suppress_event(mock_event_t))
        
        # New toggle key should not be suppressed
        mock_event_x = MagicMock()
        mock_event_x.char = 'x'
        self.assertFalse(self.listener._suppress_event(mock_event_x))


if __name__ == '__main__':
    unittest.main()

"""
Cursor management module for hiding/showing and locking the mouse cursor.
"""
import ctypes


class CursorManager:
    """Manages cursor visibility and position using Windows API."""
    
    def __init__(self):
        """Initialize cursor manager with Windows API functions."""
        try:
            self.user32 = ctypes.windll.user32
            self.ShowCursor = self.user32.ShowCursor
            self.SetCursor = self.user32.SetCursor
            self.LoadCursor = self.user32.LoadCursorW
            self.SetCursorPos = self.user32.SetCursorPos
            self.GetSystemMetrics = self.user32.GetSystemMetrics
            self.IDC_ARROW = 32512
            self.enabled = True
            
            # Calculate screen center
            self.center_x = self.GetSystemMetrics(0) // 2
            self.center_y = self.GetSystemMetrics(1) // 2
        except Exception as e:
            print(f"[WARNING] Could not initialize cursor control: {e}")
            self.enabled = False
    
    def hide_cursor(self):
        """Hide the mouse cursor completely."""
        if not self.enabled:
            return False
        
        try:
            # Method 1: Use ShowCursor to decrement display count
            count = 0
            cursor_count = self.ShowCursor(False)
            while cursor_count >= 0 and count < 100:
                cursor_count = self.ShowCursor(False)
                count += 1
            
            # Method 2: Set cursor to NULL for immediate hiding
            self.SetCursor(0)
            
            print(f"[CURSOR] Hidden (display count: {cursor_count})")
            return True
        except Exception as e:
            print(f"[ERROR] Failed to hide cursor: {e}")
            return False
    
    def show_cursor(self):
        """Show the mouse cursor."""
        if not self.enabled:
            return False
        
        try:
            # Method 1: Restore cursor visibility
            count = 0
            cursor_count = self.ShowCursor(True)
            while cursor_count < 0 and count < 100:
                cursor_count = self.ShowCursor(True)
                count += 1
            
            # Method 2: Load and set standard arrow cursor
            arrow_cursor = self.LoadCursor(0, self.IDC_ARROW)
            self.SetCursor(arrow_cursor)
            
            print(f"[CURSOR] Shown (display count: {cursor_count})")
            return True
        except Exception as e:
            print(f"[ERROR] Failed to show cursor: {e}")
            return False
    
    def lock_to_center(self):
        """Lock cursor to center of screen."""
        if not self.enabled:
            return False
        
        try:
            self.SetCursorPos(self.center_x, self.center_y)
            return True
        except Exception as e:
            print(f"[ERROR] Failed to lock cursor: {e}")
            return False

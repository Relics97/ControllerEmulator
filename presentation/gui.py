"""
GUI module for the gamepad emulator application.
Contains all UI components including main window, settings, and key mapping dialogs.
"""
import tkinter as tk
from tkinter import ttk
import vgamepad as vg

from config.config import Config


class MainWindow:
    """Main application window."""
    
    def __init__(self, controller):
        """Initialize main window."""
        self.controller = controller
        self.root = tk.Tk()
        self.root.title("Gamepad Emulator - Battlefield VI")
        self.root.geometry("550x450")
        self.root.minsize(550, 450)
        
        self._create_widgets()
        self._start_status_update()
    
    def _create_widgets(self):
        """Create all UI widgets."""
        # Status label
        self.status_label = tk.Label(
            self.root,
            text="Controller: OFF",
            font=("Arial", 16, "bold"),
            fg="red"
        )
        self.status_label.pack(pady=20)
        
        # Button frame
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)
        
        self.toggle_button = tk.Button(
            button_frame,
            text="Activate Controller (T)",
            command=self._toggle_controller,
            font=("Arial", 12),
            width=25,
            height=2
        )
        self.toggle_button.pack(side=tk.LEFT, padx=5)
        
        self.mapping_button = tk.Button(
            button_frame,
            text="Key Mapping",
            command=self._open_mapping,
            font=("Arial", 12),
            width=12,
            height=2,
            bg="#4CAF50",
            fg="white"
        )
        self.mapping_button.pack(side=tk.LEFT, padx=5)
        
        self.settings_button = tk.Button(
            button_frame,
            text="Settings",
            command=self._open_settings,
            font=("Arial", 12),
            width=12,
            height=2,
            bg="#2196F3",
            fg="white"
        )
        self.settings_button.pack(side=tk.LEFT, padx=5)
        
        # Instructions
        instructions = tk.Label(
            self.root,
            text="Press 'T' to toggle controller mode\n\n" +
                 "WASD: Movement | Mouse: Look | L/R Click: Triggers\n" +
                 "Space: Jump (A) | C: Crouch (B) | R: Reload (X) | 1: Weapon (Y)\n" +
                 "2: DPad Up | Alt: DPad Down | B: DPad Left | 3: DPad Right\n" +
                 "Q: Grenade (LB) | E: Melee (RB)\n" +
                 "Shift: Sprint (LS) | F: Aim Toggle (RS)\n" +
                 "Esc: Menu (Start) | Tab: Scoreboard (Back)",
            font=("Arial", 10),
            justify=tk.CENTER
        )
        instructions.pack(pady=20)
        
        # Status info
        self.info_label = tk.Label(
            self.root,
            text="Ready to start",
            font=("Arial", 9),
            fg="gray"
        )
        self.info_label.pack(pady=(10, 5))
    
    def _toggle_controller(self):
        """Toggle controller activation."""
        if self.controller.active:
            self.controller.deactivate()
        else:
            self.controller.activate()
    
    def _open_mapping(self):
        """Open key mapping dialog."""
        KeyMappingDialog(self.root, self.controller)
    
    def _open_settings(self):
        """Open settings dialog."""
        SettingsDialog(self.root, self.controller)
    
    def _start_status_update(self):
        """Start periodic status update."""
        self._update_status()
    
    def _update_status(self):
        """Update UI status display."""
        if self.controller.active:
            self.status_label.config(text="Controller: ACTIVE", fg="green")
            self.toggle_button.config(text="Deactivate Controller (T)")
            self.info_label.config(text="Input blocking enabled - Mouse/keyboard blocked from games")
        else:
            self.status_label.config(text="Controller: OFF", fg="red")
            self.toggle_button.config(text="Activate Controller (T)")
            self.info_label.config(text="Normal input mode - All inputs pass through")
        
        self.root.after(100, self._update_status)
    
    def run(self):
        """Start the UI main loop."""
        self.root.mainloop()


class KeyMappingDialog:
    """Dialog for remapping keybinds."""
    
    BUTTON_NAMES = {
        vg.XUSB_BUTTON.XUSB_GAMEPAD_A: "A Button",
        vg.XUSB_BUTTON.XUSB_GAMEPAD_B: "B Button",
        vg.XUSB_BUTTON.XUSB_GAMEPAD_X: "X Button",
        vg.XUSB_BUTTON.XUSB_GAMEPAD_Y: "Y Button",
        vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_UP: "DPad Up",
        vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_DOWN: "DPad Down",
        vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_LEFT: "DPad Left",
        vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_RIGHT: "DPad Right",
        vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER: "Left Bumper (LB)",
        vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_SHOULDER: "Right Bumper (RB)",
        vg.XUSB_BUTTON.XUSB_GAMEPAD_START: "Start Button",
        vg.XUSB_BUTTON.XUSB_GAMEPAD_BACK: "Back Button",
        vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_THUMB: "Left Stick Click",
        vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_THUMB: "Right Stick Click",
    }
    
    def __init__(self, parent, controller):
        """Initialize key mapping dialog."""
        self.controller = controller
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Key Mapping")
        self.dialog.geometry("600x700")
        self.dialog.resizable(False, False)
        
        self.remapping_key = None
        self.remapping_toggle = False
        self.mapping_entries = {}
        
        self._create_widgets()
        
        self.dialog.bind("<KeyPress>", self._on_key_press)
        self.dialog.transient(parent)
        self.dialog.grab_set()
    
    def _create_widgets(self):
        """Create dialog widgets."""
        # Title
        title = tk.Label(
            self.dialog,
            text="Click any key field and press a new key to remap",
            font=("Arial", 12, "bold"),
            fg="blue"
        )
        title.pack(pady=15)
        
        # Toggle key section
        self._create_toggle_section()
        
        # Separator
        tk.Label(self.dialog, text="Controller Button Mappings", font=("Arial", 10, "bold")).pack(pady=5)
        
        # Scrollable mappings
        self._create_mappings_section()
        
        # Bottom buttons
        self._create_buttons()
    
    def _create_toggle_section(self):
        """Create toggle key configuration section."""
        toggle_frame = tk.Frame(self.dialog, relief=tk.RIDGE, borderwidth=2, bg="#f0f0f0")
        toggle_frame.pack(pady=10, padx=20, fill=tk.X)
        
        tk.Label(
            toggle_frame,
            text="Toggle Controller Key:",
            font=("Arial", 11, "bold"),
            bg="#f0f0f0"
        ).pack(side=tk.LEFT, padx=10, pady=10)
        
        self.toggle_entry = tk.Entry(toggle_frame, width=10, font=("Arial", 11))
        self.toggle_entry.insert(0, self._format_key(Config.TOGGLE_KEY))
        self.toggle_entry.config(state="readonly")
        self.toggle_entry.bind("<Button-1>", lambda e: self._start_toggle_remapping())
        self.toggle_entry.pack(side=tk.LEFT, padx=10, pady=10)
    
    def _create_mappings_section(self):
        """Create scrollable mappings section."""
        canvas = tk.Canvas(self.dialog, height=450)
        scrollbar = tk.Scrollbar(self.dialog, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Add mappings
        for row, (key, button) in enumerate(Config.KEY_MAPPINGS.items()):
            button_name = self.BUTTON_NAMES.get(button, "Unknown")
            
            mapping_frame = tk.Frame(scrollable_frame)
            mapping_frame.grid(row=row, column=0, pady=5, padx=20, sticky="ew")
            
            entry = tk.Entry(mapping_frame, width=15, font=("Arial", 11))
            entry.insert(0, self._format_key(key))
            entry.config(state="readonly")
            entry.bind("<Button-1>", lambda e, k=key: self._start_remapping(k, e.widget))
            entry.pack(side=tk.LEFT, padx=5)
            
            tk.Label(mapping_frame, text="→", font=("Arial", 12)).pack(side=tk.LEFT, padx=5)
            tk.Label(mapping_frame, text=button_name, font=("Arial", 11), width=20, anchor="w").pack(side=tk.LEFT, padx=5)
            
            self.mapping_entries[key] = entry
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def _create_buttons(self):
        """Create bottom buttons."""
        button_frame = tk.Frame(self.dialog)
        button_frame.pack(pady=10)
        
        tk.Button(
            button_frame,
            text="Reset to Defaults",
            command=self._reset_defaults,
            font=("Arial", 10),
            width=15
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            button_frame,
            text="Close",
            command=self.dialog.destroy,
            font=("Arial", 10),
            width=15
        ).pack(side=tk.LEFT, padx=5)
    
    def _start_remapping(self, key, entry_widget):
        """Start remapping process for a key."""
        self.remapping_key = key
        self.remapping_toggle = False
        entry_widget.config(state="normal", bg="yellow")
        entry_widget.delete(0, tk.END)
        entry_widget.insert(0, "Press new key...")
    
    def _start_toggle_remapping(self):
        """Start remapping process for toggle key."""
        self.remapping_key = None
        self.remapping_toggle = True
        self.toggle_entry.config(state="normal", bg="yellow")
        self.toggle_entry.delete(0, tk.END)
        self.toggle_entry.insert(0, "Press new key...")
    
    def _on_key_press(self, event):
        """Handle key press during remapping."""
        if not self.remapping_key and not self.remapping_toggle:
            return
        
        new_key = self._parse_event_key(event)
        if not new_key:
            return
        
        if self.remapping_toggle:
            self._remap_toggle_key(new_key)
        elif self.remapping_key:
            self._remap_button_key(new_key)
    
    def _remap_toggle_key(self, new_key):
        """Remap the toggle key."""
        if new_key in Config.KEY_MAPPINGS or new_key in Config.JOYSTICK_KEYS:
            self.toggle_entry.config(bg="#ffcccc")
            return
        
        Config.TOGGLE_KEY = new_key
        self.toggle_entry.config(state="normal", bg="white")
        self.toggle_entry.delete(0, tk.END)
        self.toggle_entry.insert(0, self._format_key(new_key))
        self.toggle_entry.config(state="readonly")
        self.remapping_toggle = False
    
    def _remap_button_key(self, new_key):
        """Remap a button key."""
        old_button = Config.KEY_MAPPINGS[self.remapping_key]
        del Config.KEY_MAPPINGS[self.remapping_key]
        Config.KEY_MAPPINGS[new_key] = old_button
        
        # Update controller state
        if self.remapping_key in self.controller.keys:
            old_state = self.controller.keys[self.remapping_key]
            del self.controller.keys[self.remapping_key]
            self.controller.keys[new_key] = old_state
        
        # Update UI
        entry = self.mapping_entries[self.remapping_key]
        entry.config(state="normal", bg="white")
        entry.delete(0, tk.END)
        entry.insert(0, self._format_key(new_key))
        entry.config(state="readonly")
        
        self.mapping_entries[new_key] = entry
        del self.mapping_entries[self.remapping_key]
        self.remapping_key = None
    
    def _reset_defaults(self):
        """Reset all mappings to defaults."""
        Config.reset_to_defaults()
        self.controller.keys = {k: False for k in Config.KEY_MAPPINGS.keys()}
        self.dialog.destroy()
    
    @staticmethod
    def _format_key(key):
        """Format key for display."""
        key_formats = {
            'space': 'Space',
            'alt_l': 'Left Alt',
            'shift': 'Shift',
            'esc': 'Esc',
            'tab': 'Tab'
        }
        return key_formats.get(key, key.upper())
    
    @staticmethod
    def _parse_event_key(event):
        """Parse key from event."""
        if event.char and event.char.isprintable():
            return event.char.lower()
        
        key_map = {
            'space': 'space',
            'Escape': 'esc',
            'Tab': 'tab',
            'Shift_L': 'shift',
            'Shift_R': 'shift',
            'Alt_L': 'alt_l',
            'Alt_R': 'alt_l',
        }
        return key_map.get(event.keysym, event.keysym.lower() if event.keysym else None)


class SettingsDialog:
    """Dialog for adjusting configuration settings."""
    
    def __init__(self, parent, controller):
        """Initialize settings dialog."""
        self.controller = controller
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Settings")
        self.dialog.geometry("500x350")
        self.dialog.resizable(False, False)
        
        self._create_widgets()
        
        self.dialog.transient(parent)
        self.dialog.grab_set()
    
    def _create_widgets(self):
        """Create dialog widgets."""
        # Title
        title = tk.Label(
            self.dialog,
            text="Adjust Configuration Settings",
            font=("Arial", 14, "bold"),
            fg="blue"
        )
        title.pack(pady=15)
        
        # Settings frame
        settings_frame = tk.Frame(self.dialog)
        settings_frame.pack(pady=20, padx=30)
        
        self._create_setting_row(settings_frame, 0, "Update Rate (Hz):",
                                 Config.UPDATE_RATE_HZ, self._update_rate_changed,
                                 "60-240")
        self._create_setting_row(settings_frame, 1, "ADS Sensitivity:",
                                 Config.ADS_SENS_MULTIPLIER, self._ads_sens_changed,
                                 "0.1-2.0")
        self._create_setting_row(settings_frame, 2, "Recoil Compensation:",
                                 Config.RECOIL_COMPENSATION, self._recoil_comp_changed,
                                 "0.0-5.0")
        
        # Bottom buttons
        button_frame = tk.Frame(self.dialog)
        button_frame.pack(pady=20)
        
        tk.Button(button_frame, text="Reset to Defaults", command=self._reset_defaults,
                 font=("Arial", 10), width=15).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Close", command=self.dialog.destroy,
                 font=("Arial", 10), width=15).pack(side=tk.LEFT, padx=5)
    
    def _create_setting_row(self, parent, row, label, initial_value, callback, tooltip):
        """Create a setting row with label, entry, and tooltip."""
        lbl = tk.Label(parent, text=label, font=("Arial", 11), width=20, anchor="w")
        lbl.grid(row=row, column=0, pady=10, padx=5)
        
        entry = tk.Entry(parent, font=("Arial", 11), width=15)
        entry.insert(0, str(initial_value))
        entry.grid(row=row, column=1, pady=10, padx=5)
        
        entry.bind("<FocusOut>", lambda e: callback(entry))
        entry.bind("<Return>", lambda e: callback(entry))
        
        tooltip_lbl = tk.Label(parent, text=tooltip, font=("Arial", 8), fg="gray")
        tooltip_lbl.grid(row=row, column=2, pady=10, padx=5)
    
    def _update_rate_changed(self, entry):
        """Handle update rate change."""
        try:
            value = int(entry.get())
            if 60 <= value <= 240:
                self.controller.update_rate(value)
                entry.config(bg="white")
            else:
                entry.config(bg="#ffcccc")
        except ValueError:
            entry.config(bg="#ffcccc")
    
    def _ads_sens_changed(self, entry):
        """Handle ADS sensitivity change."""
        try:
            value = float(entry.get())
            if 0.1 <= value <= 2.0:
                Config.ADS_SENS_MULTIPLIER = value
                entry.config(bg="white")
            else:
                entry.config(bg="#ffcccc")
        except ValueError:
            entry.config(bg="#ffcccc")
    
    def _recoil_comp_changed(self, entry):
        """Handle recoil compensation change."""
        try:
            value = float(entry.get())
            if 0.0 <= value <= 5.0:
                Config.RECOIL_COMPENSATION = value
                entry.config(bg="white")
            else:
                entry.config(bg="#ffcccc")
        except ValueError:
            entry.config(bg="#ffcccc")
    
    def _reset_defaults(self):
        """Reset all settings to defaults."""
        Config.reset_to_defaults()
        self.controller.update_rate(Config.UPDATE_RATE_HZ)
        self.dialog.destroy()

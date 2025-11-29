# -*- coding: utf-8 -*-
import time
import sys
# Import ttkbootstrap (as ttk) for modern aesthetics
import tkinter as tk 
import ttkbootstrap as ttk
from tkinter import messagebox
from pypresence import Presence
from threading import Thread

# --- REQUIRED CONFIGURATION ---
# IMPORTANT: This is the CLIENT_ID of your Discord application.
CLIENT_ID = '1443714462942105692' 

class DiscordPresenceApp:
    def __init__(self, master):
        # We use the ttk.Window constructor to apply a visual theme
        self.master = master
        master.title("✨ Rich Presence Manager: Pro Aesthetic! ✨")
        master.geometry("550x570") # Height adjustment for the new warning message
        master.resizable(False, False)

        self.RPC = None
        self.connected = False
        self.details_fixed_value = "https://presence.swarve.lol" # Fixed value for the description

        self.setup_ui()
        
        # When closing the window, call on_closing
        master.protocol("WM_DELETE_WINDOW", self.on_closing)

    def setup_ui(self):
        # Font and padding configuration (using ttkbootstrap classes)
        title_font = ('Arial', 18, 'bold')
        label_font = ('Arial', 11)
        padding_y = 10
        padding_x = 20

        # Application Title (Using a primary context color)
        ttk.Label(self.master, text="Rich Presence Manager", font=title_font, bootstyle="primary").pack(pady=(20, 10))

        # Frame for text inputs
        input_frame = ttk.Frame(self.master)
        input_frame.pack(padx=padding_x, pady=padding_y, fill='x')

        # --- Input Fields ---
        
        # Main Line (Details) - Fixed and non-editable
        ttk.Label(input_frame, text="1. Main Line (Details): (Fixed Value)", anchor='w', font=label_font).pack(fill='x')
        ttk.Label(input_frame, text=self.details_fixed_value, bootstyle="primary", anchor='w', font=('Arial', 11, 'bold')).pack(fill='x', pady=(0, 15))

        # Secondary Line (State)
        ttk.Label(input_frame, text="2. Secondary Line (State):", anchor='w', font=label_font).pack(fill='x')
        self.state_entry = ttk.Entry(input_frame, bootstyle="info")
        self.state_entry.insert(0, "'Magical' Design with ttkbootstrap ✨")
        self.state_entry.pack(fill='x', pady=(0, 15))

        # --- Image Handling (Asset Keys) ---
        ttk.Separator(input_frame).pack(fill='x', pady=5)
        
        ttk.Label(input_frame, text="Image Configuration (BUTTON REQUIREMENT)", font=('Arial', 12, 'bold'), bootstyle="warning").pack(pady=(10, 5))
        
        # Explanation Label
        self.asset_explanation_label = ttk.Label(input_frame, text="IMPORTANT: For buttons to be visible, you MUST provide a valid Asset Key.", anchor='w', font=('Arial', 9, 'italic'), bootstyle="warning")
        self.asset_explanation_label.pack(fill='x')

        # Large Image Key (Asset Key)
        ttk.Label(input_frame, text="3. Large Image Key (Asset Key):", anchor='w', font=label_font).pack(fill='x', pady=(5, 0))
        self.large_image_key_entry = ttk.Entry(input_frame, bootstyle="info")
        self.large_image_key_entry.pack(fill='x')
        
        # Hover Text (Large Text)
        ttk.Label(input_frame, text="4. Large Image Hover Text:", anchor='w', font=label_font).pack(fill='x', pady=(5, 0))
        self.large_text_entry = ttk.Entry(input_frame, bootstyle="info")
        self.large_text_entry.insert(0, "Swarve App - Hover Text") # Default value added to avoid the error
        self.large_text_entry.pack(fill='x', pady=(0, 10))
        
        # --- Progress Bar and Status ---
        self.progress_bar = ttk.Progressbar(self.master, orient='horizontal', length=400, mode='indeterminate', bootstyle="success")
        self.progress_bar.pack(pady=10, padx=padding_x)

        # --- Action Buttons ---
        button_frame = ttk.Frame(self.master)
        button_frame.pack(pady=10)
        
        # Connect/Update Button with "success" style
        self.connect_button = ttk.Button(button_frame, text="Connect and Update Presence", command=lambda: Thread(target=self.update_presence).start(), bootstyle="success-outline", width=30)
        self.connect_button.pack(side=tk.LEFT, padx=10)
        
        # Disconnect Button with "danger" style
        self.disconnect_button = ttk.Button(button_frame, text="Disconnect", command=self.disconnect_presence, bootstyle="danger-outline", width=15, state=tk.DISABLED)
        self.disconnect_button.pack(side=tk.LEFT, padx=10)

        self.status_label = ttk.Label(self.master, text="Status: Disconnected", bootstyle="danger", font=('Arial', 11, 'bold'))
        self.status_label.pack(pady=10)

    def update_presence(self):
        """Connects to Discord and updates the Rich Presence with the GUI data."""
        # Disable buttons and start progress bar
        self.connect_button.config(state=tk.DISABLED)
        self.disconnect_button.config(state=tk.DISABLED)
        self.status_label.config(text="Status: Attempting to connect...", bootstyle="info")
        self.progress_bar.start()

        if self.connected:
            self.disconnect_presence()
            time.sleep(1) # Small pause to ensure cleanup of the previous connection

        # The 'details' value is fixed
        details = self.details_fixed_value 
        state = self.state_entry.get()
        
        # Get and clean the values
        large_image_key = self.large_image_key_entry.get().strip()
        large_text = self.large_text_entry.get().strip()
        
        # CRITICAL CORRECTION: If there is an image key, the text must be mandatory
        if large_image_key and not large_text:
            large_text = "Swarve Presence" # Safe default value to prevent RPC error
        
        # VISUAL WARNING if Assets are missing and the user expects to see buttons
        if not large_image_key:
             messagebox.showwarning("Discord Warning", 
                                     "The Large Image Key (Asset Key) is empty. "
                                     "Discord **will not display URL buttons** if at least one Asset Key is not provided. "
                                     "Consult the developer portal to upload one.")


        presence_data = {
            "details": details, 
            "state": state, 
            "start": int(time.time()),
            "large_image": large_image_key if large_image_key else None,
            "large_text": large_text,
            
            # Fixed buttons
            "buttons": [
                # Main button that links to the website
                {"label": "Visit Swarve.lol", "url": self.details_fixed_value}, 
                {"label": "Documentation", "url": "https://discord.com/developers/docs/rich-presence/how-to"}
            ],
        }

        try:
            self.RPC = Presence(CLIENT_ID)
            self.RPC.connect()
            self.RPC.update(**presence_data)
            
            self.connected = True
            self.status_label.config(text="Status: CONNECTED and Presence ACTIVE! ✅", bootstyle='success')
            self.connect_button.config(text="Update Presence", bootstyle='info-outline', state=tk.NORMAL)
            self.disconnect_button.config(state=tk.NORMAL)

        except Exception as e:
            self.connected = False
            self.status_label.config(text=f"Connection Error. Is Discord open? ❌", bootstyle='danger')
            # Use print to avoid interrupting the .exe flow with a messagebox in the thread
            print(f"Connection Error: {e}")
            self.connect_button.config(state=tk.NORMAL, bootstyle='success-outline')
            self.disconnect_button.config(state=tk.DISABLED)

        finally:
            self.progress_bar.stop()

    def disconnect_presence(self):
        """Closes the RPC connection and clears the Rich Presence."""
        if self.RPC:
            try:
                self.RPC.close()
            except Exception as e:
                print(f"Error closing RPC: {e}")
            finally:
                self.RPC = None
                self.connected = False
                self.status_label.config(text="Status: Disconnected", bootstyle='danger')
                self.connect_button.config(text="Connect and Update Presence", bootstyle='success-outline', state=tk.NORMAL)
                self.disconnect_button.config(state=tk.DISABLED)

    def on_closing(self):
        """Handles the window closing, ensuring Discord disconnection."""
        if self.connected:
            self.disconnect_presence()
        self.master.destroy()

if __name__ == "__main__":
    # Initialize the ttkbootstrap window with a dark and modern theme
    root = ttk.Window(themename="superhero") # You can try 'superhero', 'solar', or 'vapor'
    app = DiscordPresenceApp(root)
    root.mainloop()
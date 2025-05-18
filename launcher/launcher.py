import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import subprocess
from PIL import Image, ImageTk
import json
import shapeDetection
import cv2
import datetime

# Constants
INPUT_DIR = "input_images"
OUTPUT_DIR = r"C:\Users\prana\OneDrive\Desktop\Shapeshift\shapeshift\assets\json_maps"
GODOT_PROJECT_PATH = r"C:\Users\prana\OneDrive\Desktop\Shapeshift\shapeshift"
GODOT_EXE = r"C:\Users\prana\Downloads\godot_run\Godot_v4.4.1-stable_win64.exe"

# Enhanced Color Scheme
RETRO_BG = "#0a0a0a"
RETRO_FG = "#00ff41"
RETRO_BTN = "#1a1a1a"
RETRO_ACCENT = "#ff0080"
RETRO_HOVER = "#ff3399"
RETRO_SUCCESS = "#00ff88"
RETRO_BORDER = "#333333"
RETRO_FONT = ("Consolas", 11, "bold")
RETRO_TITLE_FONT = ("Consolas", 18, "bold")
RETRO_SMALL_FONT = ("Consolas", 9)

class ModernButton(tk.Button):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.configure(
            relief='flat',
            bd=0,
            padx=20,
            pady=10,
            cursor='hand2',
            font=RETRO_FONT,
            activeforeground=RETRO_BG,
            activebackground=RETRO_HOVER
        )
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        
    def on_enter(self, e):
        self['bg'] = RETRO_HOVER
        
    def on_leave(self, e):
        self['bg'] = self.original_bg

class App:
    def __init__(self, root):
        self.root = root
        self.setup_window()
        self.image_path = None
        self.image_preview = None
        self.create_widgets()
        
    def setup_window(self):
        """Configure the main window"""
        self.root.title("🕹️ Shapeshift Retro Launcher")
        self.root.geometry("700x800")
        self.root.configure(bg=RETRO_BG)
        self.root.resizable(False, False)
        
        # Center the window
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (700 // 2)
        y = (self.root.winfo_screenheight() // 2) - (800 // 2)
        self.root.geometry(f"700x800+{x}+{y}")
        
    def create_widgets(self):
        """Create and layout all widgets"""
        # Main container with padding
        main_container = tk.Frame(self.root, bg=RETRO_BG)
        main_container.pack(fill='both', expand=True, padx=30, pady=20)
        
        # Header section
        self.create_header(main_container)
        
        # Content section
        self.create_content(main_container)
        
        # Footer section
        self.create_footer(main_container)
        
    def create_header(self, parent):
        """Create the header section"""
        header_frame = tk.Frame(parent, bg=RETRO_BG)
        header_frame.pack(fill='x', pady=(0, 30))
        
        # ASCII art style title
        title_text = "╔══════════════════════════════════╗\n║       SHAPESHIFT LAUNCHER        ║\n╚══════════════════════════════════╝"
        title_label = tk.Label(
            header_frame, 
            text=title_text,
            font=("Courier", 12, "bold"),
            fg=RETRO_ACCENT,
            bg=RETRO_BG,
            justify='center'
        )
        title_label.pack()
        
        # Subtitle with pulsing effect
        subtitle = tk.Label(
            header_frame,
            text="◆ Transform Images into Game Worlds ◆",
            font=RETRO_FONT,
            fg=RETRO_SUCCESS,
            bg=RETRO_BG
        )
        subtitle.pack(pady=(10, 0))
        
    def create_content(self, parent):
        """Create the main content area"""
        content_frame = tk.Frame(parent, bg=RETRO_BG)
        content_frame.pack(fill='both', expand=True)
        
        # Status section with border
        status_frame = tk.Frame(content_frame, bg=RETRO_BORDER, relief='solid', bd=1)
        status_frame.pack(fill='x', pady=(0, 20))
        
        status_inner = tk.Frame(status_frame, bg=RETRO_BG)
        status_inner.pack(fill='x', padx=2, pady=2)
        
        status_title = tk.Label(
            status_inner,
            text="▸ STATUS",
            font=RETRO_FONT,
            fg=RETRO_FG,
            bg=RETRO_BG
        )
        status_title.pack(anchor='w', padx=10, pady=(5, 0))
        
        self.label = tk.Label(
            status_inner,
            text="No image selected.",
            font=RETRO_SMALL_FONT,
            fg=RETRO_FG,
            bg=RETRO_BG,
            wraplength=600
        )
        self.label.pack(anchor='w', padx=20, pady=(0, 10))
        
        # Browse section
        browse_frame = tk.Frame(content_frame, bg=RETRO_BG)
        browse_frame.pack(fill='x', pady=(0, 20))
        
        browse_label = tk.Label(
            browse_frame,
            text="▸ SELECT IMAGE",
            font=RETRO_FONT,
            fg=RETRO_FG,
            bg=RETRO_BG
        )
        browse_label.pack(anchor='w')
        
        self.browse_button = ModernButton(
            browse_frame,
            text="🗁 BROWSE FILES",
            bg=RETRO_BTN,
            fg=RETRO_FG,
            command=self.browse_image
        )
        self.browse_button.original_bg = RETRO_BTN
        self.browse_button.pack(anchor='w', pady=(10, 0))
        
        # Preview section with border
        preview_frame = tk.Frame(content_frame, bg=RETRO_BORDER, relief='solid', bd=1)
        preview_frame.pack(fill='both', expand=True, pady=(0, 20))
        
        preview_inner = tk.Frame(preview_frame, bg=RETRO_BG)
        preview_inner.pack(fill='both', expand=True, padx=2, pady=2)
        
        preview_title = tk.Label(
            preview_inner,
            text="▸ PREVIEW",
            font=RETRO_FONT,
            fg=RETRO_FG,
            bg=RETRO_BG
        )
        preview_title.pack(anchor='w', padx=10, pady=(5, 10))
        
        # Preview container with centered image
        self.preview_container = tk.Frame(preview_inner, bg=RETRO_BG)
        self.preview_container.pack(fill='both', expand=True, padx=10, pady=(0, 10))
        
        self.preview_label = tk.Label(
            self.preview_container,
            text="┌─────────────────────────┐\n│                         │\n│    No image to show     │\n│                         │\n└─────────────────────────┘",
            font=RETRO_SMALL_FONT,
            fg=RETRO_BORDER,
            bg=RETRO_BG
        )
        self.preview_label.pack(expand=True)
        
        # Launch section
        launch_frame = tk.Frame(content_frame, bg=RETRO_BG)
        launch_frame.pack(fill='x')
        
        # Center the launch button
        button_container = tk.Frame(launch_frame, bg=RETRO_BG)
        button_container.pack(expand=True)
        
        self.launch_button = ModernButton(
            button_container,
            text="🚀 LAUNCH GAME",
            bg=RETRO_ACCENT,
            fg=RETRO_BG,
            font=("Consolas", 14, "bold"),
            command=self.launch_game
        )
        self.launch_button.original_bg = RETRO_ACCENT
        self.launch_button.pack(pady=10)
        
        # Add some status indicators
        self.status_indicators = tk.Frame(launch_frame, bg=RETRO_BG)
        self.status_indicators.pack(pady=(10, 0))
        
    def create_footer(self, parent):
        """Create the footer section"""
        footer_frame = tk.Frame(parent, bg=RETRO_BG)
        footer_frame.pack(fill='x', side='bottom')
        
        separator = tk.Label(
            footer_frame,
            text="─" * 50,
            font=RETRO_SMALL_FONT,
            fg=RETRO_BORDER,
            bg=RETRO_BG
        )
        separator.pack(pady=(20, 5))
        
        footer_text = tk.Label(
            footer_frame,
            text="© 2025 Shapeshift | Powered by Computer Vision & Godot Engine",
            font=RETRO_SMALL_FONT,
            fg=RETRO_FG,
            bg=RETRO_BG
        )
        footer_text.pack()
        
    def browse_image(self):
        """Browse for an image file"""
        path = filedialog.askopenfilename(
            title="Select Image File",
            filetypes=[
                ("All Images", "*.png *.jpg *.jpeg *.bmp *.gif *.tiff"),
                ("PNG files", "*.png"),
                ("JPEG files", "*.jpg *.jpeg"),
                ("BMP files", "*.bmp"),
                ("All files", "*.*")
            ]
        )
        if path:
            self.image_path = path
            filename = os.path.basename(path)
            self.label.config(text=f"✓ Selected: {filename}")
            self.show_preview(path)
            
    def show_preview(self, path):
        """Display image preview"""
        try:
            # Load and resize image
            img = Image.open(path)
            
            # Calculate size to fit in preview area (max 400x300)
            img.thumbnail((400, 300), Image.Resampling.LANCZOS)
            
            # Create PhotoImage and display
            self.image_preview = ImageTk.PhotoImage(img)
            self.preview_label.config(image=self.image_preview, text="")
            
            # Update status
            width, height = img.size
            file_size = os.path.getsize(path)
            file_size_kb = file_size / 1024
            
            status_text = f"✓ Resolution: {width}×{height} | Size: {file_size_kb:.1f} KB"
            
            # Create info label if it doesn't exist
            if not hasattr(self, 'info_label'):
                self.info_label = tk.Label(
                    self.preview_container,
                    font=RETRO_SMALL_FONT,
                    fg=RETRO_SUCCESS,
                    bg=RETRO_BG
                )
                self.info_label.pack(pady=(5, 0))
            
            self.info_label.config(text=status_text)
            
        except Exception as e:
            self.preview_label.config(
                image='',
                text=f"⚠ Unable to preview image\nError: {str(e)}",
                fg=RETRO_ACCENT
            )
            if hasattr(self, 'info_label'):
                self.info_label.config(text="")
    
    def convert_image(self):
        """Convert the selected image"""
        if not self.image_path:
            messagebox.showwarning("Warning", "No image selected.")
            return
        
        # Update UI to show processing
        self.launch_button.config(text="⟳ PROCESSING...", state='disabled')
        self.root.update()
        
        try:
            os.makedirs(INPUT_DIR, exist_ok=True)
            os.makedirs(OUTPUT_DIR, exist_ok=True)
            
            input_copy = os.path.join(INPUT_DIR, os.path.basename(self.image_path))
            output_json = os.path.join(OUTPUT_DIR, "map.json")
            
            # Copy image
            with open(self.image_path, 'rb') as f_in, open(input_copy, 'wb') as f_out:
                f_out.write(f_in.read())
            
            # Process image
            json_data = shapeDetection.process(self.image_path)
            
            # Save JSON
            with open(output_json, 'w') as f:
                json.dump(json_data, f, indent=2)
                
        finally:
            # Reset button
            self.launch_button.config(text="🚀 LAUNCH GAME", state='normal')
    
    def launch_game(self):
        """Launch the Godot game"""
        try:
            self.convert_image()
            subprocess.Popen([GODOT_EXE, "--path", GODOT_PROJECT_PATH], shell=True)
            
            # Show success message
            self.show_status_message("✓ Game launched successfully!", RETRO_SUCCESS)
            
        except FileNotFoundError:
            messagebox.showerror("Error", "Godot executable not found.\nPlease check the path in the script.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to launch game:\n{str(e)}")
    
    def show_status_message(self, message, color):
        """Show a temporary status message"""
        if not hasattr(self, 'temp_status'):
            self.temp_status = tk.Label(
                self.status_indicators,
                font=RETRO_SMALL_FONT,
                bg=RETRO_BG
            )
            self.temp_status.pack()
        
        self.temp_status.config(text=message, fg=color)
        
        # Clear message after 3 seconds
        self.root.after(3000, lambda: self.temp_status.config(text=""))

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
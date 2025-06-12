"""
Main Window Component

This module defines the main window UI components for the Lab Chart Generator application.
It sets up the overall layout and main frames.


Author: Speedy29bg
"""

import tkinter as tk
from tkinter import ttk
import logging

class MainWindow:
    """Manages the main window UI components of the application"""
    
    def __init__(self, root):
        """
        Initialize the main window components
        
        Args:
            root: The tkinter root window instance
        """
        self.root = root
        self.setup_window()
        self.create_main_layout()
        
        logging.info("Main window UI components initialized")
        
    def setup_window(self):
        """Configure main window properties"""
        self.root.title("Lab Chart Generator")
        
        # Configure style
        style = ttk.Style()
        style.configure("TFrame", background="#f0f0f0")
        style.configure("TButton", font=('Arial', 10))
        style.configure("TLabel", font=('Arial', 10), background="#f0f0f0")
        
        # Make the window responsive
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
    
    def create_main_layout(self):
        """Create the main layout frames"""
        # Main container frame
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
        # Configure grid
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.rowconfigure(0, weight=0)  # Top section - fixed height
        self.main_frame.rowconfigure(1, weight=1)  # Middle section - expands
        self.main_frame.rowconfigure(2, weight=0)  # Bottom section - fixed height
        self.main_frame.rowconfigure(3, weight=0)  # Status bar - fixed height
        
        # Create frames for different sections
        # Top frame for file selection
        self.top_frame = ttk.Frame(self.main_frame)
        self.top_frame.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        
        # Middle frame (contains left and right sections and chart preview)
        self.middle_frame = ttk.Frame(self.main_frame)
        self.middle_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
          # Configure middle frame grid for 2 columns instead of 3
        self.middle_frame.columnconfigure(0, weight=1)  # Left panel (axes + chart options)
        self.middle_frame.columnconfigure(1, weight=2)  # Chart area - takes more space (about half)
        self.middle_frame.rowconfigure(0, weight=1)
        
        # Middle left frame (axis selection and chart options)
        self.middle_left_frame = ttk.Frame(self.middle_frame)
        self.middle_left_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
        # Chart preview frame (now takes up the right half)
        self.chart_frame = ttk.Frame(self.middle_frame)
        self.chart_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        
        # Create a frame for chart options that will be placed under axes selection
        self.middle_right_frame = ttk.Frame(self.middle_left_frame)
        self.middle_right_frame.pack(fill=tk.X, pady=(10, 0))
        
        # Bottom frame (output options)
        self.bottom_frame = ttk.Frame(self.main_frame)
        self.bottom_frame.grid(row=2, column=0, sticky="ew", padx=5, pady=5)
        
    def create_status_bar(self):
        """Create status bar at the bottom of the window
        
        Returns:
            ttk.Label: The status label widget
        """
        status_frame = ttk.Frame(self.main_frame)
        status_frame.grid(row=3, column=0, sticky="ew", padx=5, pady=5)
        
        status_label = ttk.Label(
            status_frame, 
            text="Ready", 
            anchor=tk.W, 
            relief=tk.SUNKEN, 
            padding=(10, 2)
        )
        status_label.pack(fill=tk.X)
        
        return status_label
        
    def get_top_frame(self):
        """Get the top frame for file selection
        
        Returns:
            ttk.Frame: The top frame widget
        """
        return self.top_frame
        
    def get_middle_left_frame(self):
        """Get the middle left frame for axes selection
        
        Returns:
            ttk.Frame: The middle left frame widget
        """
        return self.middle_left_frame
        
    def get_middle_right_frame(self):
        """Get the middle right frame for chart options
        
        Returns:
            ttk.Frame: The middle right frame widget
        """
        return self.middle_right_frame
        
    def get_chart_frame(self):
        """Get the chart frame for preview
        
        Returns:
            ttk.Frame: The chart frame widget
        """
        return self.chart_frame
        
    def get_bottom_frame(self):
        """Get the bottom frame for output options
        
        Returns:
            ttk.Frame: The bottom frame widget
        """
        return self.bottom_frame

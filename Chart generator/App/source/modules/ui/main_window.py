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
    
    def __init__(self, root, app_instance):
        """
        Initialize the main window components
        
        Args:
            root: The tkinter root window instance
            app_instance: Reference to the main LabChartGenerator instance
        """
        self.root = root
        self.app = app_instance
        self.setup_window()
        self.create_main_layout()
        
        logging.info("Main window UI components initialized")
    
    def setup_window(self):
        """Configure the main application window"""
        self.root.geometry("1300x1000")
        
        # Set application icon if available
        try:
            self.root.iconbitmap("chart_icon.ico")
        except:
            pass  # Icon file not found, use default
    
    def create_main_layout(self):
        """Create the main layout frames"""
        # Main frame
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Status bar
        self.status_label = ttk.Label(self.main_frame, text="Ready", relief=tk.SUNKEN, anchor=tk.W)
        self.status_label.pack(fill=tk.X, side=tk.BOTTOM, pady=5)
        
        # Return status label for use in other components
        return self.status_label

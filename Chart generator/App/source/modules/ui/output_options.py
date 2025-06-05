"""
Output Options UI Component

This module provides UI components for chart output options
in the Lab Chart Generator application.

Author: Lab Chart Tools Team
"""

import tkinter as tk
from tkinter import ttk
import logging

class OutputOptionsFrame:
    """Manages output options UI components and interactions"""
    
    def __init__(self, parent_frame, app_instance):
        """
        Initialize output options UI components
        
        Args:
            parent_frame: Parent tkinter frame to place this component in
            app_instance: Reference to the main application instance
        """
        self.parent = parent_frame
        self.app = app_instance
        self.create_output_options_ui()
    
    def create_output_options_ui(self):
        """Create output options UI components"""
        # Output options
        self.output_frame = ttk.LabelFrame(self.parent, text="Output Options")
        self.output_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(self.output_frame, text="Output Filename:").pack(side=tk.LEFT, padx=5, pady=5)
        self.output_filename = ttk.Entry(self.output_frame, width=30)
        self.output_filename.insert(0, "Lab_Charts")
        self.output_filename.pack(side=tk.LEFT, padx=5, pady=5)
        
        # Buttons
        self.button_frame = ttk.Frame(self.parent)
        self.button_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(self.button_frame, text="Generate Charts", command=self.app.generate_charts).pack(side=tk.LEFT, padx=5)
        ttk.Button(self.button_frame, text="Clear Selections", command=self.app.clear_selections).pack(side=tk.LEFT, padx=5)
        ttk.Button(self.button_frame, text="Apply Custom Scaling", command=self.app.update_preview).pack(side=tk.LEFT, padx=5)
        ttk.Button(self.button_frame, text="Export Current Chart", command=self.app.export_current_chart).pack(side=tk.LEFT, padx=5)
        
    def get_output_filename(self):
        """Get the current output filename
        
        Returns:
            str: Current output filename
        """
        return self.output_filename.get()

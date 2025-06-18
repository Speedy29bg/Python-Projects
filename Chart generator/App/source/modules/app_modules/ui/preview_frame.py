"""
Preview Frame UI Component

This module provides UI components for the chart preview functionality
in the Lab Chart Generator application.


Author: Speedy29bg
"""

import tkinter as tk
from tkinter import ttk
import logging

class PreviewFrame:
    """Manages chart preview UI components and interactions"""
    
    def __init__(self, parent_frame, app_instance):
        """
        Initialize chart preview UI components
        
        Args:
            parent_frame: Parent tkinter frame to place this component in
            app_instance: Reference to the main application instance
        """
        self.parent = parent_frame
        self.app = app_instance
        self.canvas = None
        self.figure = None
        self.create_preview_ui()
    
    def create_preview_ui(self):
        """Create chart preview UI components"""
        # Preview frame
        self.preview_container = ttk.LabelFrame(self.parent, text="Chart Preview")
        self.preview_container.pack(fill=tk.BOTH, expand=True, pady=5)
          # Inner frame to hold the matplotlib canvas
        self.preview_frame = ttk.Frame(self.preview_container)
        self.preview_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Set a larger height to accommodate interactive controls
        self.preview_container.config(height=650)  # Increased for interactive features

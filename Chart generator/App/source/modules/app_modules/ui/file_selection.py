"""
File Selection UI Component

This module provides UI components for file selection functionality
in the Lab Chart Generator application.


Author: Speedy29bg
"""

import tkinter as tk
from tkinter import filedialog, ttk
import os
import logging

class FileSelectionFrame:
    """Manages file selection UI components and interactions"""
    
    def __init__(self, parent_frame, app_instance):
        """
        Initialize file selection UI components
        
        Args:
            parent_frame: Parent tkinter frame to place this component in
            app_instance: Reference to the main application instance
        """
        self.parent = parent_frame
        self.app = app_instance
        self.create_file_selection_ui()
    
    def create_file_selection_ui(self):
        """Create file selection UI components"""
        # File selection frame
        self.file_frame = ttk.LabelFrame(self.parent, text="File Selection")
        self.file_frame.pack(fill=tk.X, pady=5)
        
        # File label
        self.file_label = ttk.Label(self.file_frame, text="No files selected")
        self.file_label.pack(side=tk.LEFT, padx=10, pady=5)
        
        # Buttons
        ttk.Button(self.file_frame, text="Browse", command=self.app.select_files).pack(side=tk.RIGHT, padx=10, pady=5)
        ttk.Button(self.file_frame, text="Preview Data", command=self.app.preview_data).pack(side=tk.RIGHT, padx=10, pady=5)
        ttk.Button(self.file_frame, text="Analyze Data", command=self.app.analyze_data).pack(side=tk.RIGHT, padx=10, pady=5)
    
    def update_file_label(self, file_count):
        """Update the file label with file count information
        
        Args:
            file_count: Number of selected files
        """
        self.file_label.config(text=f"Selected: {file_count} files")
        
    def clear_selections(self):
        """Reset the file selection UI state"""
        self.file_label.config(text="No files selected")

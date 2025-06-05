"""
Axes Selection UI Component

This module provides UI components for axes selection functionality
in the Lab Chart Generator application.


Author: Speedy29bg
"""

import tkinter as tk
from tkinter import ttk
import logging

class AxesSelectionFrame:
    """Manages axes selection UI components and interactions"""
    
    def __init__(self, parent_frame, app_instance):
        """
        Initialize axes selection UI components
        
        Args:
            parent_frame: Parent tkinter frame to place this component in
            app_instance: Reference to the main application instance
        """
        self.parent = parent_frame
        self.app = app_instance
        self.create_axes_selection_ui()
    
    def create_axes_selection_ui(self):
        """Create axes selection UI components"""
        # Axes selection frame
        self.axes_frame = ttk.LabelFrame(self.parent, text="Axes Selection")
        self.axes_frame.pack(fill=tk.X, pady=5)
        
        # Create three columns for axes selection
        self.axes_left = ttk.Frame(self.axes_frame)
        self.axes_middle = ttk.Frame(self.axes_frame)
        self.axes_right = ttk.Frame(self.axes_frame)
        
        self.axes_left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.axes_middle.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.axes_right.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # X-Axis selection
        ttk.Label(self.axes_left, text="X-Axis (Ctrl+click):").pack(anchor=tk.W)
        x_frame = ttk.Frame(self.axes_left)
        x_frame.pack(fill=tk.BOTH, expand=True)
        
        self.x_listbox = tk.Listbox(x_frame, selectmode="multiple", height=6, width=30, exportselection=0)
        x_scrollbar = ttk.Scrollbar(x_frame, orient="vertical", command=self.x_listbox.yview)
        
        self.x_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        x_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.x_listbox.config(yscrollcommand=x_scrollbar.set)
        self.x_listbox.bind("<<ListboxSelect>>", lambda e: self.app.update_preview())
        
        # Primary Y-Axes selection
        ttk.Label(self.axes_middle, text="Primary Y-Axes (Ctrl+click):").pack(anchor=tk.W)
        y_frame = ttk.Frame(self.axes_middle)
        y_frame.pack(fill=tk.BOTH, expand=True)
        
        self.y_listbox = tk.Listbox(y_frame, selectmode="multiple", height=6, width=30, exportselection=0)
        y_scrollbar = ttk.Scrollbar(y_frame, orient="vertical", command=self.y_listbox.yview)
        
        self.y_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        y_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.y_listbox.config(yscrollcommand=y_scrollbar.set)
        self.y_listbox.bind("<<ListboxSelect>>", lambda e: self.app.update_preview())
        
        # Secondary Y-Axes selection
        ttk.Label(self.axes_right, text="Secondary Y-Axes (Ctrl+click):").pack(anchor=tk.W)
        secondary_frame = ttk.Frame(self.axes_right)
        secondary_frame.pack(fill=tk.BOTH, expand=True)
        
        self.secondary_listbox = tk.Listbox(secondary_frame, selectmode="multiple", height=6, width=30, exportselection=0)
        secondary_scrollbar = ttk.Scrollbar(secondary_frame, orient="vertical", command=self.secondary_listbox.yview)
        
        self.secondary_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        secondary_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.secondary_listbox.config(yscrollcommand=secondary_scrollbar.set)
        self.secondary_listbox.bind("<<ListboxSelect>>", lambda e: self.app.update_preview())
    
    def clear_listboxes(self):
        """Clear all listbox selections"""
        self.x_listbox.delete(0, tk.END)
        self.y_listbox.delete(0, tk.END)
        self.secondary_listbox.delete(0, tk.END)
        
    def populate_listboxes(self, column_headers):
        """Populate the listboxes with column headers
        
        Args:
            column_headers: List of column headers to add to listboxes
        """
        for header in column_headers:
            self.x_listbox.insert(tk.END, header)
            self.y_listbox.insert(tk.END, header)
            self.secondary_listbox.insert(tk.END, header)
            
    def get_selected_items(self, column_headers):
        """Get the currently selected columns from all listboxes
        
        Args:
            column_headers: List of all available column headers
            
        Returns:
            tuple: (x_selected, y_selected, secondary_selected) lists of selected columns
        """
        # Get indices
        x_indices = self.x_listbox.curselection()
        y_indices = self.y_listbox.curselection()
        secondary_indices = self.secondary_listbox.curselection()
        
        # Convert indices to column names
        x_selected = [column_headers[i] for i in x_indices]
        y_selected = [column_headers[i] for i in y_indices]
        secondary_selected = [column_headers[i] for i in secondary_indices]
        
        return x_selected, y_selected, secondary_selected

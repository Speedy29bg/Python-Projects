"""
UI Module Facade

This module re-exports UI components from the app_modules.ui package.
"""

from modules.app_modules.ui import MainWindow
from modules.app_modules.ui import FileSelectionFrame
from modules.app_modules.ui import AxesSelectionFrame
from modules.app_modules.ui import ChartOptionsFrame
from modules.app_modules.ui import PreviewFrame
from modules.app_modules.ui import OutputOptionsFrame

__all__ = [
    'MainWindow',
    'FileSelectionFrame',
    'AxesSelectionFrame',
    'ChartOptionsFrame',
    'PreviewFrame',
    'OutputOptionsFrame'
]

# Legacy code below - will be deprecated in future versions
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import queue
import threading
import os
import logging
from typing import List, Dict, Tuple, Optional, Any, Callable
import matplotlib.pyplot as plt
import pandas as pd

class LabChartUI:
    def __init__(self, root, callbacks):
        """Initialize the UI components
        
        Args:
            root: The tkinter root window
            callbacks: Dictionary of callback functions for various UI actions
        """
        self.root = root
        self.callbacks = callbacks
        
        # Store references to UI elements that need to be accessed
        self.file_label = None
        self.x_listbox = None
        self.y_listbox = None
        self.secondary_listbox = None
        self.preview_frame = None
        self.output_filename = None
        self.status_label = None
        self.range_entries = []
        
        # Setup the UI components
        self.setup_ui()
    
    def setup_ui(self):
        """Create and arrange UI elements"""
        # Main frame
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # File selection
        file_frame = ttk.LabelFrame(main_frame, text="File Selection")
        file_frame.pack(fill=tk.X, pady=5)
        
        self.file_label = ttk.Label(file_frame, text="No files selected")
        self.file_label.pack(side=tk.LEFT, padx=10, pady=5)
        
        ttk.Button(file_frame, text="Browse", command=self.callbacks['select_files']).pack(side=tk.RIGHT, padx=10, pady=5)
        ttk.Button(file_frame, text="Preview Data", command=self.callbacks['preview_data']).pack(side=tk.RIGHT, padx=10, pady=5)
        
        # Axes selection frame
        axes_frame = ttk.LabelFrame(main_frame, text="Axes Selection")
        axes_frame.pack(fill=tk.X, pady=5)
        
        # Create three columns for axes selection
        axes_left = ttk.Frame(axes_frame)
        axes_middle = ttk.Frame(axes_frame)
        axes_right = ttk.Frame(axes_frame)
        
        axes_left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        axes_middle.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        axes_right.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # X-Axis selection
        ttk.Label(axes_left, text="X-Axis (Ctrl+click):").pack(anchor=tk.W)
        x_frame = ttk.Frame(axes_left)
        x_frame.pack(fill=tk.BOTH, expand=True)
        
        self.x_listbox = tk.Listbox(x_frame, selectmode="multiple", height=6, width=30, exportselection=0)
        x_scrollbar = ttk.Scrollbar(x_frame, orient="vertical", command=self.x_listbox.yview)
        
        self.x_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        x_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.x_listbox.config(yscrollcommand=x_scrollbar.set)
        self.x_listbox.bind("<<ListboxSelect>>", lambda e: self.callbacks['update_preview']())
        
        # Primary Y-Axes selection
        ttk.Label(axes_middle, text="Primary Y-Axes (Ctrl+click):").pack(anchor=tk.W)
        y_frame = ttk.Frame(axes_middle)
        y_frame.pack(fill=tk.BOTH, expand=True)
        
        self.y_listbox = tk.Listbox(y_frame, selectmode="multiple", height=6, width=30, exportselection=0)
        y_scrollbar = ttk.Scrollbar(y_frame, orient="vertical", command=self.y_listbox.yview)
        
        self.y_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        y_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.y_listbox.config(yscrollcommand=y_scrollbar.set)
        self.y_listbox.bind("<<ListboxSelect>>", lambda e: self.callbacks['update_preview']())
        
        # Secondary Y-Axes selection
        ttk.Label(axes_right, text="Secondary Y-Axes (Ctrl+click):").pack(anchor=tk.W)
        secondary_frame = ttk.Frame(axes_right)
        secondary_frame.pack(fill=tk.BOTH, expand=True)
        
        self.secondary_listbox = tk.Listbox(secondary_frame, selectmode="multiple", height=6, width=30, exportselection=0)
        secondary_scrollbar = ttk.Scrollbar(secondary_frame, orient="vertical", command=self.secondary_listbox.yview)
        
        self.secondary_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        secondary_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.secondary_listbox.config(yscrollcommand=secondary_scrollbar.set)
        self.secondary_listbox.bind("<<ListboxSelect>>", lambda e: self.callbacks['update_preview']())
        
        # Chart scaling options
        scaling_frame = ttk.LabelFrame(main_frame, text="Chart Scaling Options")
        scaling_frame.pack(fill=tk.X, pady=5)
        
        # Left and right sections for scaling options
        scale_left = ttk.Frame(scaling_frame)
        scale_right = ttk.Frame(scaling_frame)
        scale_left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        scale_right.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Scale options
        ttk.Checkbutton(scale_left, text="Auto Scale", variable=self.callbacks['vars']['auto_scale'], 
                      command=self.callbacks['toggle_manual_scaling']).pack(anchor=tk.W)
        ttk.Checkbutton(scale_left, text="Log Scale X-Axis", variable=self.callbacks['vars']['log_scale_x'],
                      command=self.callbacks['update_preview']).pack(anchor=tk.W)
        ttk.Checkbutton(scale_left, text="Log Scale Primary Y-Axis", variable=self.callbacks['vars']['log_scale_y1'],
                      command=self.callbacks['update_preview']).pack(anchor=tk.W)
        ttk.Checkbutton(scale_left, text="Log Scale Secondary Y-Axis", variable=self.callbacks['vars']['log_scale_y2'],
                      command=self.callbacks['update_preview']).pack(anchor=tk.W)
        ttk.Checkbutton(scale_left, text="Normalize Data (0-1)", variable=self.callbacks['vars']['normalize_data'],
                      command=self.callbacks['update_preview']).pack(anchor=tk.W)
        
        # Chart type selection
        ttk.Label(scale_left, text="Chart Type:").pack(anchor=tk.W, pady=(10, 0))
        chart_type_frame = ttk.Frame(scale_left)
        chart_type_frame.pack(anchor=tk.W)
        
        ttk.Radiobutton(chart_type_frame, text="Line", variable=self.callbacks['vars']['chart_type'], 
                      value="line", command=self.callbacks['update_preview']).pack(side=tk.LEFT)
        ttk.Radiobutton(chart_type_frame, text="Scatter", variable=self.callbacks['vars']['chart_type'], 
                      value="scatter", command=self.callbacks['update_preview']).pack(side=tk.LEFT)
        
        # Export format selection
        ttk.Label(scale_left, text="Export Format:").pack(anchor=tk.W, pady=(10, 0))
        export_format_frame = ttk.Frame(scale_left)
        export_format_frame.pack(anchor=tk.W)
        
        ttk.Radiobutton(export_format_frame, text="Excel", variable=self.callbacks['vars']['export_format'], 
                      value="xlsx").pack(side=tk.LEFT)
        ttk.Radiobutton(export_format_frame, text="PNG", variable=self.callbacks['vars']['export_format'], 
                      value="png").pack(side=tk.LEFT)
        ttk.Radiobutton(export_format_frame, text="PDF", variable=self.callbacks['vars']['export_format'], 
                      value="pdf").pack(side=tk.LEFT)
        
        # Custom range inputs
        range_frame = ttk.Frame(scale_right)
        range_frame.pack(fill=tk.X)
        
        # X-Axis range
        ttk.Label(range_frame, text="X-Axis Range:").grid(row=0, column=0, sticky=tk.W, pady=2)
        ttk.Label(range_frame, text="Min:").grid(row=0, column=1, sticky=tk.E, padx=5, pady=2)
        x_min_entry = ttk.Entry(range_frame, textvariable=self.callbacks['vars']['x_min'], width=10, state='disabled')
        x_min_entry.grid(row=0, column=2, pady=2)
        ttk.Label(range_frame, text="Max:").grid(row=0, column=3, sticky=tk.E, padx=5, pady=2)
        x_max_entry = ttk.Entry(range_frame, textvariable=self.callbacks['vars']['x_max'], width=10, state='disabled')
        x_max_entry.grid(row=0, column=4, pady=2)
        
        # Primary Y-Axis range
        ttk.Label(range_frame, text="Primary Y-Axis Range:").grid(row=1, column=0, sticky=tk.W, pady=2)
        ttk.Label(range_frame, text="Min:").grid(row=1, column=1, sticky=tk.E, padx=5, pady=2)
        y1_min_entry = ttk.Entry(range_frame, textvariable=self.callbacks['vars']['y1_min'], width=10, state='disabled')
        y1_min_entry.grid(row=1, column=2, pady=2)
        ttk.Label(range_frame, text="Max:").grid(row=1, column=3, sticky=tk.E, padx=5, pady=2)
        y1_max_entry = ttk.Entry(range_frame, textvariable=self.callbacks['vars']['y1_max'], width=10, state='disabled')
        y1_max_entry.grid(row=1, column=4, pady=2)
        
        # Secondary Y-Axis range
        ttk.Label(range_frame, text="Secondary Y-Axis Range:").grid(row=2, column=0, sticky=tk.W, pady=2)
        ttk.Label(range_frame, text="Min:").grid(row=2, column=1, sticky=tk.E, padx=5, pady=2)
        y2_min_entry = ttk.Entry(range_frame, textvariable=self.callbacks['vars']['y2_min'], width=10, state='disabled')
        y2_min_entry.grid(row=2, column=2, pady=2)
        ttk.Label(range_frame, text="Max:").grid(row=2, column=3, sticky=tk.E, padx=5, pady=2)
        y2_max_entry = ttk.Entry(range_frame, textvariable=self.callbacks['vars']['y2_max'], width=10, state='disabled')
        y2_max_entry.grid(row=2, column=4, pady=2)
        
        # Store references to the entry widgets for enabling/disabling
        self.range_entries = [
            x_min_entry, x_max_entry, 
            y1_min_entry, y1_max_entry, 
            y2_min_entry, y2_max_entry
        ]
        
        # Color scheme selection
        color_scheme_frame = ttk.LabelFrame(main_frame, text="Color Scheme")
        color_scheme_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(color_scheme_frame, text="Select Color Scheme:").pack(side=tk.LEFT, padx=5, pady=5)
        color_scheme_menu = ttk.OptionMenu(
            color_scheme_frame, 
            self.callbacks['vars']['selected_color_scheme'], 
            self.callbacks['vars']['color_schemes'][0], 
            *self.callbacks['vars']['color_schemes'],
            command=lambda _: self.callbacks['update_preview']()
        )
        color_scheme_menu.pack(side=tk.LEFT, padx=5, pady=5)

        # Preview frame
        preview_frame = ttk.LabelFrame(main_frame, text="Chart Preview")
        preview_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.preview_frame = ttk.Frame(preview_frame)
        self.preview_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Output options
        output_frame = ttk.LabelFrame(main_frame, text="Output Options")
        output_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(output_frame, text="Output Filename:").pack(side=tk.LEFT, padx=5, pady=5)
        self.output_filename = ttk.Entry(output_frame, width=30)
        self.output_filename.insert(0, "Lab_Charts")
        self.output_filename.pack(side=tk.LEFT, padx=5, pady=5)
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(scale_left, text="Generate Charts", command=self.callbacks['generate_charts']).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Clear Selections", command=self.callbacks['clear_selections']).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Apply Custom Scaling", command=self.callbacks['update_preview']).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Export Current Chart", command=self.callbacks['export_current_chart']).pack(side=tk.LEFT, padx=5)
        
        # Status bar
        self.status_label = ttk.Label(main_frame, text="Ready", relief=tk.SUNKEN, anchor=tk.W)
        self.status_label.pack(fill=tk.X, side=tk.BOTTOM, pady=5)
    
    def show_loading_indicator(self, message="Loading..."):
        """Show a loading indicator with progress bar
        
        Args:
            message: Text message to display
            
        Returns:
            tuple: Frame and progress bar objects
        """
        loading_frame = ttk.Frame(self.root)
        loading_frame.place(relx=0.5, rely=0.5, anchor='center')
        
        loading_label = ttk.Label(loading_frame, text=message, font=('Helvetica', 12, 'bold'))
        loading_label.pack(pady=10)
        
        progress = ttk.Progressbar(loading_frame, orient="horizontal", length=300, mode="indeterminate")
        progress.pack(pady=10)
        progress.start(10)
        
        return loading_frame, loading_label, progress
    
    def show_data_preview(self, df):
        """Show a data preview window for a DataFrame
        
        Args:
            df: Pandas DataFrame to display
        """
        if df.empty:
            messagebox.showinfo("Info", "No data found in the file")
            return
        
        # Create a new window for the preview
        preview_window = tk.Toplevel(self.root)
        preview_window.title(f"Data Preview")
        preview_window.geometry("800x600")
        
        # Create a Text widget to display the data
        text_widget = tk.Text(preview_window, wrap="none")
        
        # Add scrollbars
        y_scrollbar = ttk.Scrollbar(preview_window, orient="vertical", command=text_widget.yview)
        x_scrollbar = ttk.Scrollbar(preview_window, orient="horizontal", command=text_widget.xview)
        text_widget.configure(yscrollcommand=y_scrollbar.set, xscrollcommand=x_scrollbar.set)
        
        # Layout
        text_widget.grid(row=0, column=0, sticky="nsew")
        y_scrollbar.grid(row=0, column=1, sticky="ns")
        x_scrollbar.grid(row=1, column=0, sticky="ew")
        
        # Configure grid weights
        preview_window.grid_rowconfigure(0, weight=1)
        preview_window.grid_columnconfigure(0, weight=1)
        
        # Display dataframe as formatted text
        text_widget.insert(tk.END, df.head(100).to_string())
        text_widget.configure(state="disabled")  # Make read-only
    
    def show_progress_dialog(self, title, max_value):
        """Show a progress dialog with cancel button
        
        Args:
            title: Dialog title
            max_value: Maximum progress value
            
        Returns:
            tuple: Dialog window, progress variable, file label, cancel button
        """
        progress_window = tk.Toplevel(self.root)
        progress_window.title(title)
        progress_window.geometry("300x150")
        progress_window.transient(self.root)
        progress_window.grab_set()
        
        # Add a label and progress bar
        ttk.Label(progress_window, text="Processing files...").pack(pady=10)
        progress_var = tk.DoubleVar()
        progress_bar = ttk.Progressbar(progress_window, variable=progress_var, maximum=max_value)
        progress_bar.pack(fill=tk.X, padx=20, pady=10)
        file_label = ttk.Label(progress_window, text="")
        file_label.pack(pady=10)
        
        # Add a cancel button
        cancel_button = ttk.Button(progress_window, text="Cancel", command=progress_window.destroy)
        cancel_button.pack(pady=10)
        
        return progress_window, progress_var, file_label, cancel_button
    
    def get_output_filename(self):
        """Get the current output filename from the entry field
        
        Returns:
            str: The output filename
        """
        return self.output_filename.get() or "Lab_Charts"
    
    def update_listboxes(self, headers):
        """Update all listboxes with the given headers
        
        Args:
            headers: List of column headers
        """
        # Clear all listboxes
        self.x_listbox.delete(0, tk.END)
        self.y_listbox.delete(0, tk.END)
        self.secondary_listbox.delete(0, tk.END)
        
        if headers and len(headers) > 0:
            for header in headers:
                self.x_listbox.insert(tk.END, header)
                self.y_listbox.insert(tk.END, header)
                self.secondary_listbox.insert(tk.END, header)
        else:
            self.x_listbox.insert(tk.END, "No headers found")
            self.y_listbox.insert(tk.END, "No headers found")
            self.secondary_listbox.insert(tk.END, "No headers found")
    
    def get_selected_items(self):
        """Get selected items from all listboxes
        
        Returns:
            tuple: (x_selected, y_selected, secondary_selected)
        """
        x_indices = list(self.x_listbox.curselection())
        y_indices = list(self.y_listbox.curselection())
        secondary_indices = list(self.secondary_listbox.curselection())
        
        x_selected = [self.x_listbox.get(i) for i in x_indices]
        y_selected = [self.y_listbox.get(i) for i in y_indices]
        secondary_selected = [self.secondary_listbox.get(i) for i in secondary_indices]
        
        return x_selected, y_selected, secondary_selected, (x_indices, y_indices, secondary_indices)
    
    def clear_listbox_selections(self):
        """Clear all listbox selections"""
        self.x_listbox.selection_clear(0, tk.END)
        self.y_listbox.selection_clear(0, tk.END)
        self.secondary_listbox.selection_clear(0, tk.END)
    
    def update_status(self, message):
        """Update the status bar message
        
        Args:
            message: Status message to display
        """
        self.status_label.config(text=message)
    
    def update_range_entries_state(self, state):
        """Update the state of all range entry widgets
        
        Args:
            state: The state to set ('normal' or 'disabled')
        """
        for entry in self.range_entries:
            entry.configure(state=state)
    
    def update_file_label(self, message):
        """Update the file selection label
        
        Args:
            message: Text to display in the file label
        """
        self.file_label.config(text=message)
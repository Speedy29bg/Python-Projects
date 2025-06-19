#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
User Interface Components for Interactive Chart Generator

Provides all UI components including file selection, axes selection,
chart options, scaling controls, and chart preview.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
from typing import List, Dict, Optional, Callable, Any
from utils.logger import get_logger

logger = get_logger()

class FileSelectionFrame:
    """File selection UI component"""
    
    def __init__(self, parent, on_file_loaded: Callable):
        """
        Initialize file selection frame
        
        Args:
            parent: Parent tkinter widget
            on_file_loaded: Callback function when file is loaded
        """
        self.parent = parent
        self.on_file_loaded = on_file_loaded
        self.current_files = []  # Support multiple files
        self.preview_callback: Optional[Callable] = None
        self.clear_callback: Optional[Callable] = None
        
        self.create_ui()
    def create_ui(self):
        """Create the UI components"""
        # Main frame
        self.frame = ttk.LabelFrame(self.parent, text="File Selection", padding=10)

        # Top frame for label and buttons
        top_frame = ttk.Frame(self.frame)
        top_frame.pack(fill=tk.X, expand=True)

        # Current file label
        self.file_label = ttk.Label(top_frame, text="No file selected", foreground="gray")
        self.file_label.pack(side=tk.LEFT, fill=tk.X, expand=True)        # Button frame
        button_frame = ttk.Frame(top_frame)
        button_frame.pack(side=tk.LEFT)

        # Responsive button sizing - adjust based on available space
        # Load file button
        ttk.Button(button_frame, text="Browse CSV",
                  command=self.load_file).pack(side=tk.LEFT, padx=(0, 3))
        # Preview Data button
        ttk.Button(button_frame, text="Preview",
                  command=self.preview_data).pack(side=tk.LEFT, padx=(0, 3))
        # Clear Data button
        ttk.Button(button_frame, text="Clear",
                  command=self.clear_data).pack(side=tk.LEFT)

        # Quick load frame for recent files
        self.quick_frame = ttk.Frame(self.frame)
        self.quick_frame.pack(fill=tk.X, expand=True, pady=(10, 0))

        ttk.Label(self.quick_frame, text="Quick Load:").pack(side=tk.LEFT)
        self.quick_btn_col = 1  # Track column for quick load buttons        # Check for sample data
        self._add_sample_files()
    
    def _add_sample_files(self):
        """Add buttons for sample data files"""
        # Look for DUT Logs directory
        possible_paths = [
            os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data"),
            os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "..", "DUT Logs"),
            os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "DUT Logs")
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                csv_files = [f for f in os.listdir(path) if f.endswith('.csv')][:5]  # Limit to 5 files
                for filename in csv_files:
                    filepath = os.path.join(path, filename)
                    btn = ttk.Button(self.quick_frame, text=filename[:15] + "..." if len(filename) > 15 else filename,
                                   command=lambda f=filepath: self.load_specific_file(f))
                    btn.pack(side=tk.LEFT, padx=5)
                    break
    
    def load_file(self):
        """Load CSV files using file dialog (supports multiple selection)"""
        filetypes = [
            ("CSV files", "*.csv"),
            ("All files", "*.*")
        ]
        
        filenames = filedialog.askopenfilenames(
            title="Select CSV files",
            filetypes=filetypes,
            initialdir=os.path.expanduser("~")
        )
        
        if filenames:
            self.current_files = list(filenames)
            # Use the first file for processing (can be extended later)
            self.load_specific_file(filenames[0])
            # Update label to show multiple files
            if len(filenames) > 1:
                self.file_label.config(text=f"Selected: {len(filenames)} files", foreground="blue")
            else:
                filename = os.path.basename(filenames[0])
                self.file_label.config(text=f"Selected: {filename}", foreground="blue")

    def load_specific_file(self, filepath: str):
        """Load a specific file"""
        try:
            success = self.on_file_loaded(filepath)
            if success:
                # If this is not part of a multi-file selection, update the files list
                if filepath not in self.current_files:
                    self.current_files = [filepath]
                filename = os.path.basename(filepath)
                self.file_label.config(text=f"Loaded: {filename}", foreground="green")
                logger.info(f"File loaded successfully: {filename}")
            else:
                self.file_label.config(text="Failed to load file", foreground="red")
                
        except Exception as e:
            logger.error(f"Error loading file: {e}")
            messagebox.showerror("Error", f"Failed to load file:\\n{e}")
            self.file_label.config(text="Error loading file", foreground="red")

    def set_preview_callback(self, callback: Callable):
        """Set the callback for the preview data button."""
        self.preview_callback = callback

    def set_clear_callback(self, callback: Callable):
        """Set the callback for the clear data button."""
        self.clear_callback = callback

    def preview_data(self):
        """Handle preview data button click."""
        if self.preview_callback:
            self.preview_callback()

    def clear_data(self):
        """Handle clear data button click."""
        if self.clear_callback:
            self.clear_callback()
    

class AxesSelectionFrame:
    """Axes selection UI component"""
    
    def __init__(self, parent, on_selection_changed: Callable):
        """
        Initialize axes selection frame
        
        Args:
            parent: Parent tkinter widget
            on_selection_changed: Callback when selection changes
        """
        self.parent = parent
        self.on_selection_changed = on_selection_changed
        self.columns = []
        
        # Variables
        self.x_var = tk.StringVar()
        self.y_vars = []
        self.y_checkboxes = []
        
        self.create_ui()    
    def create_ui(self):
        """Create the UI components"""
        # Main frame
        self.frame = ttk.LabelFrame(self.parent, text="Axes Selection", padding=10)
        # Don't pack here - let the parent controller handle positioning
        
        # Create two columns
        left_frame = ttk.Frame(self.frame)
        left_frame.grid(row=0, column=0, sticky='nsew', padx=(0, 10))
        
        right_frame = ttk.Frame(self.frame)
        right_frame.grid(row=0, column=1, sticky='nsew')
        
        # X-axis selection
        ttk.Label(left_frame, text="X-Axis:", font=('Arial', 10, 'bold')).grid(row=0, column=0, sticky='w')
        self.x_combo = ttk.Combobox(left_frame, textvariable=self.x_var, state='readonly', width=25)
        self.x_combo.grid(row=1, column=0, sticky='ew', pady=(5, 15))
        self.x_combo.bind('<<ComboboxSelected>>', lambda e: self.on_selection_changed())
          # Y-axis selection
        ttk.Label(right_frame, text="Y-Axis (select multiple):", font=('Arial', 10, 'bold')).grid(row=0, column=0, sticky='w')
        
        # Scrollable frame for Y-axis checkboxes with responsive height
        # Calculate responsive height based on available space
        try:
            root = self.parent.winfo_toplevel()
            screen_height = root.winfo_screenheight()
            canvas_height = max(min(int(screen_height * 0.2), 200), 100)  # 20% of screen height, clamped between 100-200
        except:
            canvas_height = 150  # Fallback
            
        self.y_canvas = tk.Canvas(right_frame, height=canvas_height)
        self.y_scrollbar = ttk.Scrollbar(right_frame, orient="vertical", command=self.y_canvas.yview)
        self.y_scrollable_frame = ttk.Frame(self.y_canvas)
        self.y_scrollable_frame.bind(
            "<Configure>",
            lambda e: self.y_canvas.configure(scrollregion=self.y_canvas.bbox("all"))
        )
        self.y_canvas.create_window((0, 0), window=self.y_scrollable_frame, anchor="nw")
        self.y_canvas.configure(yscrollcommand=self.y_scrollbar.set)
        self.y_canvas.grid(row=1, column=0, sticky='nsew', pady=5)
        self.y_scrollbar.grid(row=1, column=1, sticky='ns', pady=5)
        right_frame.grid_rowconfigure(1, weight=1)
        right_frame.grid_columnconfigure(0, weight=1)
    
    def update_columns(self, columns: List[str]):
        """Update available columns"""
        self.columns = columns
        
        # Update X-axis combo
        self.x_combo['values'] = columns
        if columns:
            self.x_combo.set(columns[0])
        
        # Clear existing Y-axis checkboxes
        for widget in self.y_scrollable_frame.winfo_children():
            widget.destroy()
        
        self.y_vars = []
        self.y_checkboxes = []
        
        # Create Y-axis checkboxes
        for col in columns:
            var = tk.BooleanVar()
            cb = ttk.Checkbutton(self.y_scrollable_frame, text=col, variable=var,
                               command=self.on_selection_changed)
            cb.pack(anchor='w', pady=2)
            
            self.y_vars.append(var)
            self.y_checkboxes.append(cb)
        
        # Select first Y column by default
        if self.y_vars:
            self.y_vars[0].set(True)
    
    def get_selected_axes(self) -> Dict[str, Any]:
        """Get currently selected axes"""
        x_axis = self.x_var.get()
        y_axes = []
        
        for i, var in enumerate(self.y_vars):
            if var.get():
                y_axes.append(self.columns[i])
        
        return {
            'x_axis': x_axis,
            'y_axes': y_axes
        }


class ChartOptionsFrame:
    """Chart options UI component"""
    
    def __init__(self, parent, on_option_changed: Callable):
        """
        Initialize chart options frame
        
        Args:
            parent: Parent tkinter widget
            on_option_changed: Callback when options change
        """
        self.parent = parent
        self.on_option_changed = on_option_changed
        
        # Variables
        self.chart_type_var = tk.StringVar(value="line")
        self.color_scheme_var = tk.StringVar(value="default")
        self.log_x_var = tk.BooleanVar()
        self.log_y_var = tk.BooleanVar()
        self.dual_axis_var = tk.BooleanVar()
        
        self.create_ui()    
    def create_ui(self):
        """Create the UI components"""
        # Main frame
        self.frame = ttk.LabelFrame(self.parent, text="Chart Options", padding=10)        # Chart type selection
        type_frame = ttk.Frame(self.frame)
        type_frame.pack(fill=tk.X, pady=(0, 3))
        ttk.Label(type_frame, text="Type:", font=('Arial', 9, 'bold')).pack(side=tk.LEFT)
        ttk.Radiobutton(type_frame, text="Line", variable=self.chart_type_var,
                       value="line", command=self.on_option_changed).pack(side=tk.LEFT, padx=8)
        ttk.Radiobutton(type_frame, text="Scatter", variable=self.chart_type_var,
                       value="scatter", command=self.on_option_changed).pack(side=tk.LEFT, padx=8)

        # Color scheme selection
        color_frame = ttk.Frame(self.frame)
        color_frame.pack(fill=tk.X, pady=(0, 3))
        ttk.Label(color_frame, text="Colors:", font=('Arial', 9, 'bold')).pack(side=tk.LEFT)
        color_combo = ttk.Combobox(color_frame, textvariable=self.color_scheme_var,
                                  values=["default", "viridis", "plasma", "inferno", "magma", "cool"],
                                  state='readonly', width=12)
        color_combo.pack(side=tk.LEFT, padx=8)

        # Scaling and axes options in one row
        options_frame = ttk.Frame(self.frame)
        options_frame.pack(fill=tk.X, pady=(0, 3))
        ttk.Label(options_frame, text="Options:", font=('Arial', 9, 'bold')).pack(side=tk.LEFT)
        ttk.Checkbutton(options_frame, text="Log X", variable=self.log_x_var,
                       command=self.on_option_changed).pack(side=tk.LEFT, padx=5)
        ttk.Checkbutton(options_frame, text="Log Y", variable=self.log_y_var,
                       command=self.on_option_changed).pack(side=tk.LEFT, padx=5)

        # Multiple axes option
        axes_frame = ttk.Frame(self.frame)
        axes_frame.pack(fill=tk.X, pady=(3, 0))
        ttk.Checkbutton(axes_frame, text="Separate Y-axes for each series", variable=self.dual_axis_var,
                       command=self.on_option_changed).pack(side=tk.LEFT)
    
    def get_options(self) -> Dict[str, Any]:
        """Get current chart options"""
        return {
            'chart_type': self.chart_type_var.get(),
            'color_scheme': self.color_scheme_var.get(),
            'log_x': self.log_x_var.get(),
            'log_y': self.log_y_var.get(),
            'dual_axis': self.dual_axis_var.get()
        }


class StatusFrame:
    """Status bar UI component"""
    
    def __init__(self, parent):
        """
        Initialize status frame
        
        Args:
            parent: Parent tkinter widget
        """
        self.parent = parent
        
        # Variables
        self.status_var = tk.StringVar(value="Ready")
        self.info_var = tk.StringVar(value="Load a CSV file to get started")
        
        self.create_ui()
    
    def create_ui(self):
        """Create the UI components"""
        # Main frame
        self.frame = ttk.Frame(self.parent)
        self.frame.grid(row=5, column=0, sticky='ew')
        
        # Status label
        ttk.Label(self.frame, textvariable=self.status_var, anchor='w', 
                 relief='sunken', padding=5).grid(row=0, column=0, sticky='ew')
        ttk.Label(self.frame, textvariable=self.info_var, anchor='e', 
                 relief='sunken', padding=5, foreground='blue').grid(row=0, column=1, sticky='ew')
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_columnconfigure(1, weight=1)
    
    def set_status(self, status: str):
        """Set status message"""
        self.status_var.set(status)
        logger.info(f"Status: {status}")
    
    def set_info(self, info: str):
        """Set info message"""
        self.info_var.set(info)

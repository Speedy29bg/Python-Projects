"""
Core application module for the Lab Chart Generator

This module contains the main LabChartGenerator class that orchestrates the overall
functionality of the application, including UI setup, data loading, chart creation,
and export features.


Author: Speedy29bg
"""

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pandas as pd
import numpy as np
import os
import queue
import threading
import logging
from typing import List, Dict, Tuple, Optional, Any, Union, Callable

from modules.data_processor import detect_header_row, read_csv_file, process_data_for_scaling, create_safe_sheet_name
from modules.chart_generator import create_preview_plot, clear_figure, create_tkinter_canvas
from modules.excel_export import generate_excel_workbook, export_figure
from modules.ui_components import create_loading_indicator, create_progress_dialog
from modules.data_analysis import (calculate_statistics, filter_outliers, smooth_data, 
                                  calculate_derived_columns, analyze_correlation, detect_anomalies)

class LabChartGenerator:
    """
    Main class for the Laboratory Chart Generator application
    
    This class provides a comprehensive GUI for loading, visualizing and exporting
    chart data from CSV files. It supports various chart formatting options, including
    multiple axes, logarithmic scaling, and normalization.
    The application can detect datetime columns and properly format them on chart axes.
    """
    
    def __init__(self, root: tk.Tk):
        """
        Constructor initializes the application window and variables
        
        Args:
            root: The tkinter root window instance
            
        Creates a new instance of the LabChartGenerator application with all
        necessary variables initialized, including file lists, data caches, chart settings, etc.
        """
        self.root = root
        self.root.geometry("1300x1000")
        
        # Set application icon if available
        try:
            self.root.iconbitmap("chart_icon.ico")
        except:
            pass  # Icon file not found, use default
        
        # Variables
        self.files: List[str] = []
        self.canvas = None
        self.figure = None
        self.column_headers: List[str] = []
        self.file_data_cache: Dict[str, pd.DataFrame] = {}  # Cache for loaded file data
        
        # Chart settings
        self.auto_scale = tk.BooleanVar(value=True)
        self.log_scale_x = tk.BooleanVar(value=False)
        self.log_scale_y1 = tk.BooleanVar(value=False)
        self.log_scale_y2 = tk.BooleanVar(value=False)
        self.normalize_data = tk.BooleanVar(value=False)
        
        # Custom range variables
        self.x_min = tk.StringVar()
        self.x_max = tk.StringVar()
        self.y1_min = tk.StringVar()
        self.y1_max = tk.StringVar()
        self.y2_min = tk.StringVar()
        self.y2_max = tk.StringVar()
        
        # Chart type and export options
        self.chart_type = tk.StringVar(value="line")
        self.export_format = tk.StringVar(value="xlsx")
        
        # Color scheme for charts
        self.color_schemes = ["default", "viridis", "plasma", "inferno", "magma", "cividis"]
        self.selected_color_scheme = tk.StringVar(value=self.color_schemes[0])
        
        # Setup UI
        self.setup_ui()
        
        logging.info("Application initialized")
    
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
        
        ttk.Button(file_frame, text="Browse", command=self.select_files).pack(side=tk.RIGHT, padx=10, pady=5)
        ttk.Button(file_frame, text="Preview Data", command=self.preview_data).pack(side=tk.RIGHT, padx=10, pady=5)
        ttk.Button(file_frame, text="Analyze Data", command=self.analyze_data).pack(side=tk.RIGHT, padx=10, pady=5)
        
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
        self.x_listbox.bind("<<ListboxSelect>>", lambda e: self.update_preview())
        
        # Primary Y-Axes selection
        ttk.Label(axes_middle, text="Primary Y-Axes (Ctrl+click):").pack(anchor=tk.W)
        y_frame = ttk.Frame(axes_middle)
        y_frame.pack(fill=tk.BOTH, expand=True)
        
        self.y_listbox = tk.Listbox(y_frame, selectmode="multiple", height=6, width=30, exportselection=0)
        y_scrollbar = ttk.Scrollbar(y_frame, orient="vertical", command=self.y_listbox.yview)
        
        self.y_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        y_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.y_listbox.config(yscrollcommand=y_scrollbar.set)
        self.y_listbox.bind("<<ListboxSelect>>", lambda e: self.update_preview())
        
        # Secondary Y-Axes selection
        ttk.Label(axes_right, text="Secondary Y-Axes (Ctrl+click):").pack(anchor=tk.W)
        secondary_frame = ttk.Frame(axes_right)
        secondary_frame.pack(fill=tk.BOTH, expand=True)
        
        self.secondary_listbox = tk.Listbox(secondary_frame, selectmode="multiple", height=6, width=30, exportselection=0)
        secondary_scrollbar = ttk.Scrollbar(secondary_frame, orient="vertical", command=self.secondary_listbox.yview)
        
        self.secondary_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        secondary_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.secondary_listbox.config(yscrollcommand=secondary_scrollbar.set)
        self.secondary_listbox.bind("<<ListboxSelect>>", lambda e: self.update_preview())
        
        # Chart scaling options
        scaling_frame = ttk.LabelFrame(main_frame, text="Chart Scaling Options")
        scaling_frame.pack(fill=tk.X, pady=5)
        
        # Left and right sections for scaling options
        scale_left = ttk.Frame(scaling_frame)
        scale_right = ttk.Frame(scaling_frame)
        scale_left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        scale_right.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Scale options
        ttk.Checkbutton(scale_left, text="Auto Scale", variable=self.auto_scale, 
                      command=self.toggle_manual_scaling).pack(anchor=tk.W)
        ttk.Checkbutton(scale_left, text="Log Scale X-Axis", variable=self.log_scale_x,
                      command=self.update_preview).pack(anchor=tk.W)
        ttk.Checkbutton(scale_left, text="Log Scale Primary Y-Axis", variable=self.log_scale_y1,
                      command=self.update_preview).pack(anchor=tk.W)
        ttk.Checkbutton(scale_left, text="Log Scale Secondary Y-Axis", variable=self.log_scale_y2,
                      command=self.update_preview).pack(anchor=tk.W)
        ttk.Checkbutton(scale_left, text="Normalize Data (0-1)", variable=self.normalize_data,
                      command=self.update_preview).pack(anchor=tk.W)
        
        # Chart type selection
        ttk.Label(scale_left, text="Chart Type:").pack(anchor=tk.W, pady=(10, 0))
        chart_type_frame = ttk.Frame(scale_left)
        chart_type_frame.pack(anchor=tk.W)
        
        ttk.Radiobutton(chart_type_frame, text="Line", variable=self.chart_type, 
                      value="line", command=self.update_preview).pack(side=tk.LEFT)
        ttk.Radiobutton(chart_type_frame, text="Scatter", variable=self.chart_type, 
                      value="scatter", command=self.update_preview).pack(side=tk.LEFT)
        
        # Export format selection
        ttk.Label(scale_left, text="Export Format:").pack(anchor=tk.W, pady=(10, 0))
        export_format_frame = ttk.Frame(scale_left)
        export_format_frame.pack(anchor=tk.W)
        
        ttk.Radiobutton(export_format_frame, text="Excel", variable=self.export_format, 
                      value="xlsx").pack(side=tk.LEFT)
        ttk.Radiobutton(export_format_frame, text="PNG", variable=self.export_format, 
                      value="png").pack(side=tk.LEFT)
        ttk.Radiobutton(export_format_frame, text="PDF", variable=self.export_format, 
                      value="pdf").pack(side=tk.LEFT)
        
        # Custom range inputs
        range_frame = ttk.Frame(scale_right)
        range_frame.pack(fill=tk.X)
        
        # X-Axis range
        ttk.Label(range_frame, text="X-Axis Range:").grid(row=0, column=0, sticky=tk.W, pady=2)
        ttk.Label(range_frame, text="Min:").grid(row=0, column=1, sticky=tk.E, padx=5, pady=2)
        self.x_min_entry = ttk.Entry(range_frame, textvariable=self.x_min, width=10, state='disabled')
        self.x_min_entry.grid(row=0, column=2, pady=2)
        ttk.Label(range_frame, text="Max:").grid(row=0, column=3, sticky=tk.E, padx=5, pady=2)
        self.x_max_entry = ttk.Entry(range_frame, textvariable=self.x_max, width=10, state='disabled')
        self.x_max_entry.grid(row=0, column=4, pady=2)
        
        # Primary Y-Axis range
        ttk.Label(range_frame, text="Primary Y-Axis Range:").grid(row=1, column=0, sticky=tk.W, pady=2)
        ttk.Label(range_frame, text="Min:").grid(row=1, column=1, sticky=tk.E, padx=5, pady=2)
        self.y1_min_entry = ttk.Entry(range_frame, textvariable=self.y1_min, width=10, state='disabled')
        self.y1_min_entry.grid(row=1, column=2, pady=2)
        ttk.Label(range_frame, text="Max:").grid(row=1, column=3, sticky=tk.E, padx=5, pady=2)
        self.y1_max_entry = ttk.Entry(range_frame, textvariable=self.y1_max, width=10, state='disabled')
        self.y1_max_entry.grid(row=1, column=4, pady=2)
        
        # Secondary Y-Axis range
        ttk.Label(range_frame, text="Secondary Y-Axis Range:").grid(row=2, column=0, sticky=tk.W, pady=2)
        ttk.Label(range_frame, text="Min:").grid(row=2, column=1, sticky=tk.E, padx=5, pady=2)
        self.y2_min_entry = ttk.Entry(range_frame, textvariable=self.y2_min, width=10, state='disabled')
        self.y2_min_entry.grid(row=2, column=2, pady=2)
        ttk.Label(range_frame, text="Max:").grid(row=2, column=3, sticky=tk.E, padx=5, pady=2)
        self.y2_max_entry = ttk.Entry(range_frame, textvariable=self.y2_max, width=10, state='disabled')
        self.y2_max_entry.grid(row=2, column=4, pady=2)
        
        # Store references to the entry widgets for enabling/disabling
        self.range_entries = [
            self.x_min_entry, self.x_max_entry, 
            self.y1_min_entry, self.y1_max_entry, 
            self.y2_min_entry, self.y2_max_entry
        ]
        
        # Color scheme selection
        color_scheme_frame = ttk.LabelFrame(main_frame, text="Color Scheme")
        color_scheme_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(color_scheme_frame, text="Select Color Scheme:").pack(side=tk.LEFT, padx=5, pady=5)
        color_scheme_menu = ttk.OptionMenu(color_scheme_frame, self.selected_color_scheme, *self.color_schemes)
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
        
        ttk.Button(button_frame, text="Generate Charts", command=self.generate_charts).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Clear Selections", command=self.clear_selections).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Apply Custom Scaling", command=self.update_preview).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Export Current Chart", command=self.export_current_chart).pack(side=tk.LEFT, padx=5)
        
        # Status bar
        self.status_label = ttk.Label(main_frame, text="Ready", relief=tk.SUNKEN, anchor=tk.W)
        self.status_label.pack(fill=tk.X, side=tk.BOTTOM, pady=5)
        
        logging.info("UI setup complete")

    def toggle_manual_scaling(self):
        """Enable or disable manual scaling inputs"""
        state = 'disabled' if self.auto_scale.get() else 'normal'
        
        # Update state for all range entry widgets
        for entry in self.range_entries:
            entry.configure(state=state)
        
        self.update_preview()
    
    def select_files(self):
        """Handle file selection and load column headers"""
        selected_files = filedialog.askopenfilenames(filetypes=[("CSV files", "*.csv")])
        
        if not selected_files:
            return
        
        self.files = selected_files
        self.file_label.config(text=f"Selected: {len(self.files)} files")
        
        try:
            # Clear cache for files that are no longer selected
            self.file_data_cache = {k: v for k, v in self.file_data_cache.items() if k in self.files}
            
            # Load files in background
            self.load_files_in_background(self.files, self.detect_headers_and_populate_listboxes)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load file(s): {str(e)}")
            self.status_label.config(text="Error loading files")
    
    def load_files_in_background(self, files, callback):
        """Load files in background thread to keep UI responsive
        
        Args:
            files: List of file paths to load
            callback: Function to call when loading is complete
        """
        self.status_label.config(text="Loading files...")
        
        # Create loading indicator
        loading_frame = ttk.Frame(self.root)
        loading_frame.place(relx=0.5, rely=0.5, anchor='center')
        
        loading_label = ttk.Label(loading_frame, text="Loading files...", font=('Helvetica', 12, 'bold'))
        loading_label.pack(pady=10)
        
        progress = ttk.Progressbar(loading_frame, orient="horizontal", length=300, mode="indeterminate")
        progress.pack(pady=10)
        progress.start(10)
        
        # Create queue for thread communication
        file_queue = queue.Queue()
        
        # Function to run in background thread
        def load_files_thread():
            loaded_data = {}
            
            for i, file_path in enumerate(files):
                try:
                    header_row_idx = detect_header_row(file_path)
                    df = read_csv_file(file_path, header_row_idx)
                    loaded_data[file_path] = df
                    
                    # Update progress info via queue
                    file_queue.put(("progress", i+1, len(files), os.path.basename(file_path)))
                except Exception as e:
                    file_queue.put(("error", os.path.basename(file_path), str(e)))
            
            # Signal completion
            file_queue.put(("done", loaded_data))
        
        # Function to process queue updates in main thread
        def check_queue():
            try:
                while True:
                    message = file_queue.get_nowait()
                    
                    if message[0] == "progress":
                        _, current, total, filename = message
                        loading_label.config(text=f"Loading {current}/{total}: {filename}")
                    
                    elif message[0] == "error":
                        _, filename, error = message
                        logging.error(f"Error loading {filename}: {error}")
                    
                    elif message[0] == "done":
                        _, loaded_data = message
                        # Update cache with loaded data
                        self.file_data_cache.update(loaded_data)
                        
                        # Remove loading indicator
                        loading_frame.destroy()
                        
                        # Call the callback
                        if callback:
                            callback()
                        
                        return  # Exit the update loop
            
            except queue.Empty:
                # Queue is empty but loading not complete, check again after a delay
                self.root.after(100, check_queue)
        
        # Start background thread
        threading.Thread(target=load_files_thread, daemon=True).start()
        
        # Start queue checking in main thread
        check_queue()
    
    def preview_data(self):
        """Show a preview of the data in the first selected file"""
        if not self.files:
            messagebox.showinfo("Info", "No files selected")
            return
        
        try:
            # Get data from the first file
            file_path = self.files[0]
            if file_path in self.file_data_cache:
                df = self.file_data_cache[file_path]
            else:
                header_row_idx = detect_header_row(file_path)
                df = read_csv_file(file_path, header_row_idx)
                self.file_data_cache[file_path] = df
            
            if df.empty:
                messagebox.showinfo("Info", "No data found in the file")
                return
            
            # Create a new window for the preview
            preview_window = tk.Toplevel(self.root)
            preview_window.title(f"Data Preview: {os.path.basename(file_path)}")
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
            
            # Format DataFrame as string with fixed-width columns
            # Limit to first 100 rows for performance
            preview_text = df.head(100).to_string(index=True)
            text_widget.insert(tk.END, preview_text)
            
            # Make the text widget read-only
            text_widget.configure(state="disabled")
            
            # Update status
            self.status_label.config(text=f"Previewing data from {os.path.basename(file_path)}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to preview data: {str(e)}")
            self.status_label.config(text=f"Error previewing data: {str(e)}")
    
    def detect_headers_and_populate_listboxes(self):
        """Detect headers from the first file and populate column selection listboxes"""
        if not self.files or not self.file_data_cache:
            return
        
        try:
            # Get first file from cache
            first_file = self.files[0]
            if first_file in self.file_data_cache:
                df = self.file_data_cache[first_file]
                
                # Clear existing items
                self.x_listbox.delete(0, tk.END)
                self.y_listbox.delete(0, tk.END)
                self.secondary_listbox.delete(0, tk.END)
                
                # Add headers to all listboxes
                self.column_headers = list(df.columns)
                for header in self.column_headers:
                    self.x_listbox.insert(tk.END, header)
                    self.y_listbox.insert(tk.END, header)
                    self.secondary_listbox.insert(tk.END, header)
                
                # Reset selections
                self.x_selected_indices = []
                self.y_selected_indices = []
                self.secondary_selected_indices = []
                
                self.status_label.config(text=f"Loaded {len(self.column_headers)} columns from {os.path.basename(first_file)}")
            else:
                self.status_label.config(text="Selected file is not in cache. Please try again.")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to detect headers: {str(e)}")
            self.status_label.config(text=f"Error detecting headers: {str(e)}")
    
    def get_selected_items(self):
        """Get the currently selected columns from all listboxes"""
        # Get indices
        x_indices = self.x_listbox.curselection()
        y_indices = self.y_listbox.curselection()
        secondary_indices = self.secondary_listbox.curselection()
        
        # Convert indices to column names
        x_selected = [self.column_headers[i] for i in x_indices]
        y_selected = [self.column_headers[i] for i in y_indices]
        secondary_selected = [self.column_headers[i] for i in secondary_indices]
        
        return x_selected, y_selected, secondary_selected
    
    def update_preview(self):
        """Update the chart preview based on current selections"""
        if not self.files or not self.column_headers:
            return
        
        try:
            # Get selected columns
            x_selected, y_selected, secondary_selected = self.get_selected_items()
            
            # Check if we have valid selections
            if not x_selected or (not y_selected and not secondary_selected):
                if not x_selected:
                    self.status_label.config(text="Please select an X-axis column")
                else:
                    self.status_label.config(text="Please select at least one Y-axis column")
                return
            
            # Use only the first X column if multiple selected
            if len(x_selected) > 1:
                self.status_label.config(text="Using only the first selected X-axis column")
                x_selected = [x_selected[0]]
            
            # Get data from the first file
            file_path = self.files[0]
            if file_path in self.file_data_cache:
                df = self.file_data_cache[file_path]
            else:
                header_row_idx = detect_header_row(file_path)
                df = read_csv_file(file_path, header_row_idx)
                self.file_data_cache[file_path] = df
            
            if df.empty:
                self.status_label.config(text="No data found in the file")
                return
            
            # Check if selected columns exist in dataframe
            all_selected = x_selected + y_selected + secondary_selected
            missing_columns = [col for col in all_selected if col not in df.columns]
            
            if missing_columns:
                self.status_label.config(text=f"Missing columns in data: {', '.join(missing_columns)}")
                return
            
            # Clear existing canvas
            if self.canvas:
                self.figure, self.canvas = clear_figure(self.figure, self.canvas)
            
            # Collect chart settings
            chart_settings = {
                'auto_scale': self.auto_scale.get(),
                'log_scale_x': self.log_scale_x.get(),
                'log_scale_y1': self.log_scale_y1.get(),
                'log_scale_y2': self.log_scale_y2.get(),
                'normalize_data': self.normalize_data.get(),
                'chart_type': self.chart_type.get(),
                'color_scheme': self.selected_color_scheme.get()
            }
            
            # Add manual range settings if not auto-scaling
            if not self.auto_scale.get():
                try:
                    if self.x_min.get() and self.x_max.get():
                        chart_settings['x_min'] = float(self.x_min.get())
                        chart_settings['x_max'] = float(self.x_max.get())
                    
                    if self.y1_min.get() and self.y1_max.get():
                        chart_settings['y1_min'] = float(self.y1_min.get())
                        chart_settings['y1_max'] = float(self.y1_max.get())
                    
                    if self.y2_min.get() and self.y2_max.get():
                        chart_settings['y2_min'] = float(self.y2_min.get())
                        chart_settings['y2_max'] = float(self.y2_max.get())
                except ValueError:
                    messagebox.showwarning("Warning", "Invalid range values. Please enter valid numbers.")
            
            # Process data for scaling
            processed_df = process_data_for_scaling(df, x_selected[0], y_selected, secondary_selected, chart_settings)
            
            # Create new figure and plot
            self.figure, chart_info = create_preview_plot(
                processed_df, x_selected[0], y_selected, secondary_selected, 
                chart_settings, original_df=df
            )
            
            if self.figure:
                # Create canvas and display figure
                self.canvas = create_tkinter_canvas(self.figure, self.preview_frame)
                
                # Update status with any warnings or info
                if 'warning' in chart_info:
                    self.status_label.config(text=f"Warning: {chart_info['warning']}")
                elif 'info' in chart_info:
                    self.status_label.config(text=chart_info['info'])
                else:
                    self.status_label.config(text="Preview updated")
            else:
                # Handle error
                error_msg = chart_info.get('error', "Failed to create chart")
                self.status_label.config(text=f"Error: {error_msg}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update preview: {str(e)}")
            self.status_label.config(text=f"Error: {str(e)}")
            logging.exception("Error in update_preview")
    
    def clear_selections(self):
        """Clear all selections and reset the preview"""
        # Clear listbox selections
        self.x_listbox.selection_clear(0, tk.END)
        self.y_listbox.selection_clear(0, tk.END)
        self.secondary_listbox.selection_clear(0, tk.END)
        
        # Reset scaling options to defaults
        self.auto_scale.set(True)
        self.log_scale_x.set(False)
        self.log_scale_y1.set(False)
        self.log_scale_y2.set(False)
        self.normalize_data.set(False)
        self.chart_type.set("line")
        
        # Clear manual range entries
        self.x_min.set("")
        self.x_max.set("")
        self.y1_min.set("")
        self.y1_max.set("")
        self.y2_min.set("")
        self.y2_max.set("")
        
        # Update UI state
        self.toggle_manual_scaling()
        
        # Clear the preview
        if self.canvas:
            self.figure, self.canvas = clear_figure(self.figure, self.canvas)
        
        self.status_label.config(text="Selections cleared")
    
    def export_current_chart(self):
        """Export the currently displayed chart to the selected format"""
        if not self.figure:
            messagebox.showinfo("Info", "No chart to export")
            return
        
        try:
            # Get output filename without extension
            base_filename = self.output_filename.get()
            if not base_filename:
                base_filename = "Lab_Charts"
            
            # Strip any extension
            base_filename = os.path.splitext(base_filename)[0]
            
            # Add appropriate extension based on selected format
            format_type = self.export_format.get()
            filename = f"{base_filename}.{format_type}"
            
            # Ask for save location
            save_path = filedialog.asksaveasfilename(
                defaultextension=f".{format_type}",
                filetypes=[(f"{format_type.upper()} files", f"*.{format_type}")],
                initialfile=filename
            )
            
            if not save_path:
                return
            
            # Use export function from excel_export module
            export_figure(self.figure, save_path, format_type)
            
            self.status_label.config(text=f"Chart exported as {os.path.basename(save_path)}")
            messagebox.showinfo("Success", f"Chart exported successfully to {save_path}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export chart: {str(e)}")
            self.status_label.config(text=f"Error exporting chart: {str(e)}")
            logging.exception("Error in export_current_chart")
    
    def generate_charts(self):
        """Generate charts for all selected files"""
        if not self.files:
            messagebox.showinfo("Info", "No files selected")
            return
            
        try:
            # Get selected columns
            x_selected, y_selected, secondary_selected = self.get_selected_items()
            
            # Check if we have valid selections
            if not x_selected or (not y_selected and not secondary_selected):
                if not x_selected:
                    messagebox.showinfo("Info", "Please select an X-axis column")
                else:
                    messagebox.showinfo("Info", "Please select at least one Y-axis column")
                return
            
            # Use only the first X column if multiple selected
            if len(x_selected) > 1:
                x_selected = [x_selected[0]]
            
            # Get chart settings
            chart_settings = {
                'auto_scale': self.auto_scale.get(),
                'log_scale_x': self.log_scale_x.get(),
                'log_scale_y1': self.log_scale_y1.get(),
                'log_scale_y2': self.log_scale_y2.get(),
                'normalize_data': self.normalize_data.get(),
                'color_scheme': self.selected_color_scheme.get()
            }
            
            # Add manual range settings if not auto-scaling
            if not self.auto_scale.get():
                try:
                    if self.x_min.get() and self.x_max.get():
                        chart_settings['x_min'] = float(self.x_min.get())
                        chart_settings['x_max'] = float(self.x_max.get())
                    
                    if self.y1_min.get() and self.y1_max.get():
                        chart_settings['y1_min'] = float(self.y1_min.get())
                        chart_settings['y1_max'] = float(self.y1_max.get())
                    
                    if self.y2_min.get() and self.y2_max.get():
                        chart_settings['y2_min'] = float(self.y2_min.get())
                        chart_settings['y2_max'] = float(self.y2_max.get())
                except ValueError:
                    messagebox.showwarning("Warning", "Invalid range values. Please enter valid numbers.")
            
            # Get output filename without extension
            base_filename = self.output_filename.get()
            if not base_filename:
                base_filename = "Lab_Charts"
            
            # Strip any extension
            base_filename = os.path.splitext(base_filename)[0]
            
            # Ask for save location
            save_path = filedialog.asksaveasfilename(
                defaultextension=".xlsx",
                filetypes=[("Excel files", "*.xlsx")],
                initialfile=f"{base_filename}.xlsx"
            )
            
            if not save_path:
                return
            
            # Create progress dialog
            progress_dialog = tk.Toplevel(self.root)
            progress_dialog.title("Generating Charts")
            progress_dialog.geometry("400x150")
            progress_dialog.transient(self.root)
            progress_dialog.grab_set()
            
            progress_label = ttk.Label(progress_dialog, text="Generating charts...", font=('Helvetica', 10))
            progress_label.pack(pady=10)
            
            progress_bar = ttk.Progressbar(progress_dialog, orient="horizontal", length=300, mode="determinate")
            progress_bar.pack(pady=10)
            
            file_label = ttk.Label(progress_dialog, text="")
            file_label.pack(pady=5)
            
            # Start generating in a background thread
            def generate_thread():
                try:
                    wb, processed_files, skipped_files = generate_excel_workbook(
                        self.files, 
                        self.file_data_cache, 
                        x_selected[0], 
                        y_selected, 
                        secondary_selected,
                        self.chart_type.get(),
                        chart_settings
                    )
                    
                    # Save workbook
                    wb.save(save_path)
                    
                    # Show completion message
                    message = f"Generated charts for {processed_files} files"
                    if skipped_files > 0:
                        message += f" (skipped {skipped_files} files with errors)"
                    
                    # Update queue with completion message
                    progress_queue.put(("done", message))
                    
                except Exception as e:
                    progress_queue.put(("error", str(e)))
            
            # Create queue for progress updates
            progress_queue = queue.Queue()
            
            # Start thread
            threading.Thread(target=generate_thread, daemon=True).start()
            
            # Function to check queue and update UI
            def check_progress():
                try:
                    while True:
                        message = progress_queue.get_nowait()
                        
                        if message[0] == "progress":
                            _, current, total, filename = message
                            progress_bar["value"] = (current / total) * 100
                            file_label.config(text=f"Processing: {filename}")
                            
                        elif message[0] == "done":
                            _, result_msg = message
                            progress_dialog.destroy()
                            messagebox.showinfo("Success", f"{result_msg}\nSaved to {save_path}")
                            self.status_label.config(text=result_msg)
                            return
                            
                        elif message[0] == "error":
                            _, error_msg = message
                            progress_dialog.destroy()
                            messagebox.showerror("Error", f"Failed to generate charts: {error_msg}")
                            self.status_label.config(text=f"Error: {error_msg}")
                            return
                            
                except queue.Empty:
                    # Check again after delay
                    self.root.after(100, check_progress)
            
            # Start checking progress
            check_progress()
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate charts: {str(e)}")
            self.status_label.config(text=f"Error: {str(e)}")
            logging.exception("Error in generate_charts")
    
    def analyze_data(self):
        """Perform statistical analysis on the selected columns"""
        if not self.files:
            messagebox.showinfo("Info", "No files selected")
            return
        
        # Get selected items
        x_selected, y_selected, secondary_selected = self.get_selected_items()
        all_selected = x_selected + y_selected + secondary_selected
        
        if not all_selected:
            messagebox.showinfo("Info", "Please select at least one column for analysis")
            return
        
        try:
            # Read data from the first file (use cache if available)
            file_path = self.files[0]
            if file_path in self.file_data_cache:
                df = self.file_data_cache[file_path]
            else:
                header_row_idx = detect_header_row(file_path)
                df = read_csv_file(file_path, header_row_idx)
                self.file_data_cache[file_path] = df
            
            if df.empty:
                self.status_label.config(text="No data found in the file")
                return
            
            # Check if selected columns exist in dataframe
            missing_columns = [col for col in all_selected if col not in df.columns]
            if missing_columns:
                self.status_label.config(text=f"Missing columns in data: {', '.join(missing_columns)}")
                return
            
            # Create analysis dialog
            analysis_dialog = tk.Toplevel(self.root)
            analysis_dialog.title(f"Data Analysis - {os.path.basename(file_path)}")
            analysis_dialog.geometry("800x600")
            
            # Create notebook for different analysis types
            notebook = ttk.Notebook(analysis_dialog)
            notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
            # 1. Basic statistics tab
            stats_frame = ttk.Frame(notebook)
            notebook.add(stats_frame, text="Statistics")
            
            # Calculate statistics
            stats = calculate_statistics(df, all_selected)
            
            # Create text widget to display statistics
            stats_text = tk.Text(stats_frame, wrap=tk.WORD, height=20, width=80)
            stats_scroll = ttk.Scrollbar(stats_frame, orient=tk.VERTICAL, command=stats_text.yview)
            stats_text.configure(yscrollcommand=stats_scroll.set)
            
            stats_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
            stats_scroll.pack(side=tk.RIGHT, fill=tk.Y)
            
            # Format and display statistics
            stats_text.insert(tk.END, f"Statistical Analysis for {os.path.basename(file_path)}\n")
            stats_text.insert(tk.END, f"{'=' * 70}\n\n")
            
            for column, column_stats in stats.items():
                stats_text.insert(tk.END, f"Column: {column}\n")
                stats_text.insert(tk.END, f"{'-' * 70}\n")
                
                for stat_name, stat_value in column_stats.items():
                    stats_text.insert(tk.END, f"{stat_name.capitalize()}: {stat_value}\n")
                
                stats_text.insert(tk.END, "\n")
            
            stats_text.configure(state='disabled')  # Make read-only
            
            # 2. Correlation analysis tab
            corr_frame = ttk.Frame(notebook)
            notebook.add(corr_frame, text="Correlations")
            
            # Only process correlation if we have at least two numeric columns
            numeric_columns = [col for col in all_selected 
                             if col in df.columns and pd.api.types.is_numeric_dtype(pd.to_numeric(df[col], errors='coerce'))]
            
            if len(numeric_columns) >= 2:
                # Calculate correlations
                corr_matrix, top_correlations = analyze_correlation(df, numeric_columns)
                
                # Create text widget for correlation display
                corr_text = tk.Text(corr_frame, wrap=tk.WORD, height=20, width=80)
                corr_scroll = ttk.Scrollbar(corr_frame, orient=tk.VERTICAL, command=corr_text.yview)
                corr_text.configure(yscrollcommand=corr_scroll.set)
                
                corr_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
                corr_scroll.pack(side=tk.RIGHT, fill=tk.Y)
                
                # Format and display correlations
                corr_text.insert(tk.END, "Correlation Analysis\n")
                corr_text.insert(tk.END, f"{'=' * 70}\n\n")
                
                # Display top correlations for each column
                corr_text.insert(tk.END, "Top Correlations by Column:\n")
                corr_text.insert(tk.END, f"{'-' * 70}\n")
                
                for column, correlations in top_correlations.items():
                    corr_text.insert(tk.END, f"Column: {column}\n")
                    for other_col, corr_value in correlations.items():
                        strength = abs(corr_value)
                        description = "Strong" if strength > 0.7 else "Moderate" if strength > 0.3 else "Weak"
                        direction = "positive" if corr_value > 0 else "negative"
                        corr_text.insert(tk.END, f"  - {other_col}: {corr_value:.3f} ({description} {direction} correlation)\n")
                    corr_text.insert(tk.END, "\n")
                
                corr_text.configure(state='disabled')  # Make read-only
            else:
                ttk.Label(corr_frame, text="Need at least 2 numeric columns for correlation analysis").pack(pady=20)
            
            # 3. Outliers tab
            outliers_frame = ttk.Frame(notebook)
            notebook.add(outliers_frame, text="Outliers")
            
            # Create controls for outlier detection
            controls_frame = ttk.Frame(outliers_frame)
            controls_frame.pack(fill=tk.X, pady=10)
            
            ttk.Label(controls_frame, text="Method:").pack(side=tk.LEFT, padx=5)
            outlier_method = tk.StringVar(value="iqr")
            method_combo = ttk.Combobox(controls_frame, textvariable=outlier_method, values=["iqr", "zscore"])
            method_combo.pack(side=tk.LEFT, padx=5)
            
            ttk.Label(controls_frame, text="Threshold:").pack(side=tk.LEFT, padx=5)
            threshold_var = tk.DoubleVar(value=1.5)
            threshold_entry = ttk.Entry(controls_frame, textvariable=threshold_var, width=5)
            threshold_entry.pack(side=tk.LEFT, padx=5)
            
            # Create text widget for outlier results
            outlier_text = tk.Text(outliers_frame, wrap=tk.WORD, height=18, width=80)
            outlier_scroll = ttk.Scrollbar(outliers_frame, orient=tk.VERTICAL, command=outlier_text.yview)
            outlier_text.configure(yscrollcommand=outlier_scroll.set)
            
            outlier_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
            outlier_scroll.pack(side=tk.RIGHT, fill=tk.Y)
            
            def detect_and_display_outliers():
                # Clear previous results
                outlier_text.configure(state='normal')
                outlier_text.delete('1.0', tk.END)
                
                try:
                    method = outlier_method.get()
                    threshold = float(threshold_var.get())
                    
                    # Only detect outliers for numeric columns
                    numeric_cols = [col for col in all_selected 
                                  if col in df.columns and pd.api.types.is_numeric_dtype(pd.to_numeric(df[col], errors='coerce'))]
                    
                    if not numeric_cols:
                        outlier_text.insert(tk.END, "No numeric columns selected for outlier detection")
                        outlier_text.configure(state='disabled')
                        return
                    
                    # Detect outliers
                    anomalies = detect_anomalies(df, numeric_cols, [method], threshold)
                    
                    # Display results
                    outlier_text.insert(tk.END, f"Outlier Detection (Method: {method}, Threshold: {threshold})\n")
                    outlier_text.insert(tk.END, f"{'=' * 70}\n\n")
                    
                    for col, indices in anomalies.items():
                        outlier_count = len(indices)
                        total_count = len(df[col].dropna())
                        percentage = (outlier_count / total_count * 100) if total_count > 0 else 0
                        
                        outlier_text.insert(tk.END, f"Column: {col}\n")
                        outlier_text.insert(tk.END, f"- Outliers found: {outlier_count} ({percentage:.1f}% of valid data points)\n")
                        
                        if outlier_count > 0:
                            # Show sample of outlier values (up to 10)
                            sample_size = min(10, outlier_count)
                            sample_indices = indices[:sample_size]
                            
                            outlier_text.insert(tk.END, f"- Sample outlier values (showing {sample_size} of {outlier_count}):\n")
                            for idx in sample_indices:
                                outlier_text.insert(tk.END, f"  Row {idx}: {df.loc[idx, col]}\n")
                        
                        outlier_text.insert(tk.END, "\n")
                    
                except Exception as e:
                    outlier_text.insert(tk.END, f"Error during outlier detection: {str(e)}")
                
                outlier_text.configure(state='disabled')
            
            # Add detect button
            detect_button = ttk.Button(controls_frame, text="Detect Outliers", command=detect_and_display_outliers)
            detect_button.pack(side=tk.LEFT, padx=20)
            
            # Initial detection
            detect_and_display_outliers()
            
            # 4. Data Transformation tab
            transform_frame = ttk.Frame(notebook)
            notebook.add(transform_frame, text="Transformations")
            
            transform_controls = ttk.Frame(transform_frame)
            transform_controls.pack(fill=tk.X, pady=10)
            
            ttk.Label(transform_controls, text="Smoothing Method:").pack(side=tk.LEFT, padx=5)
            smooth_method = tk.StringVar(value="moving_avg")
            smooth_combo = ttk.Combobox(transform_controls, textvariable=smooth_method, 
                                      values=["moving_avg", "gaussian", "savgol"])
            smooth_combo.pack(side=tk.LEFT, padx=5)
            
            ttk.Label(transform_controls, text="Window Size:").pack(side=tk.LEFT, padx=5)
            window_size_var = tk.IntVar(value=3)
            window_entry = ttk.Entry(transform_controls, textvariable=window_size_var, width=5)
            window_entry.pack(side=tk.LEFT, padx=5)
            
            # Column selection for transformation
            transform_column_frame = ttk.Frame(transform_frame)
            transform_column_frame.pack(fill=tk.X, pady=10)
            
            ttk.Label(transform_column_frame, text="Select Column:").pack(side=tk.LEFT, padx=5)
            transform_column_var = tk.StringVar()
            transform_column_combo = ttk.Combobox(transform_column_frame, textvariable=transform_column_var, 
                                               values=numeric_columns)
            transform_column_combo.pack(side=tk.LEFT, padx=5)
            if numeric_columns:
                transform_column_var.set(numeric_columns[0])
                
            # Results display
            transform_result_frame = ttk.Frame(transform_frame)
            transform_result_frame.pack(fill=tk.BOTH, expand=True, pady=10)
            
            # Import matplotlib for visualization
            import matplotlib.pyplot as plt
            from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
            
            # Function to apply transformation and show results
            def apply_transformation():
                column = transform_column_var.get()
                method = smooth_method.get()
                window = window_size_var.get()
                
                if column not in df.columns:
                    messagebox.showinfo("Error", f"Column '{column}' not found")
                    return
                
                # Clear previous chart
                for widget in transform_result_frame.winfo_children():
                    widget.destroy()
                
                try:
                    # Convert to numeric
                    numeric_data = pd.to_numeric(df[column], errors='coerce')
                    
                    # Apply smoothing
                    smoothed_df = smooth_data(df, [column], method, window)
                    smoothed_data = smoothed_df[column]
                    
                    # Create figure for comparison
                    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 6), sharex=True)
                    
                    # Original data plot
                    ax1.plot(numeric_data, marker='.', linestyle='-', alpha=0.7, label='Original')
                    ax1.set_title(f"Original Data - {column}")
                    ax1.grid(True, alpha=0.3)
                    
                    # Smoothed data plot
                    ax2.plot(smoothed_data, marker='.', linestyle='-', color='red', alpha=0.7, label='Smoothed')
                    ax2.set_title(f"Smoothed Data - Method: {method}, Window Size: {window}")
                    ax2.grid(True, alpha=0.3)
                    
                    # Add legend
                    ax1.legend()
                    ax2.legend()
                    
                    # Adjust layout
                    plt.tight_layout()
                    
                    # Create canvas
                    canvas = FigureCanvasTkAgg(fig, master=transform_result_frame)
                    canvas.draw()
                    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
                    
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to apply transformation: {str(e)}")
            
            # Add apply button
            apply_button = ttk.Button(transform_column_frame, text="Apply Transformation", command=apply_transformation)
            apply_button.pack(side=tk.LEFT, padx=20)
            
            # Initial transformation
            if numeric_columns:
                apply_transformation()
            
            # Position the dialog
            analysis_dialog.transient(self.root)
            analysis_dialog.grab_set()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to perform data analysis: {str(e)}")
            self.status_label.config(text=f"Error: {str(e)}")

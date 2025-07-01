#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Main Application Controller for Interactive Chart Generator

Coordinates all components and handles the main application logic.
"""

import tkinter as tk
from tkinter import ttk
import pandas as pd
from typing import Dict, List, Any, Optional
from core.data_processor import DataProcessor
from core.chart_generator import InteractiveChartGenerator
from ui.components import FileSelectionFrame, AxesSelectionFrame, ChartOptionsFrame, StatusFrame
from ui.filter_window import FilterWindow
from utils.logger import get_logger

logger = get_logger()

class InteractiveChartApp:
    """Main application controller"""
    
    def __init__(self, root):
        """
        Initialize the application
        
        Args:
            root: Tkinter root window
        """
        self.root = root
        self.data_processor = DataProcessor()
        self.chart_generator = InteractiveChartGenerator()        # UI Components
        self.file_frame = None
        self.filter_window = None  # Filter window
        self.axes_frame = None
        self.options_frame = None
        self.status_frame = None
        self.chart_preview_frame = None
        
        self.setup_ui()
        self.setup_styles()
        
        # Bind window resize event for responsive layout
        self.root.bind('<Configure>', self.on_window_resize)
        
        logger.info("Interactive Chart Application initialized")
    def setup_styles(self):
        """Setup UI styles with responsive font sizing"""
        style = ttk.Style()
        
        # Get screen size for responsive styling
        screen_width = self.root.winfo_screenwidth()
        
        # Calculate responsive font sizes
        if screen_width >= 1920:  # 4K/high-res displays
            title_font_size = 14
            header_font_size = 11
            info_font_size = 10
        elif screen_width >= 1366:  # Standard displays
            title_font_size = 12
            header_font_size = 10
            info_font_size = 9
        else:  # Smaller displays
            title_font_size = 11
            header_font_size = 9
            info_font_size = 8
        
        # Configure styles with responsive fonts
        style.configure('Title.TLabel', font=('Arial', title_font_size, 'bold'))
        style.configure('Header.TLabel', font=('Arial', header_font_size, 'bold'))
        style.configure('Info.TLabel', font=('Arial', info_font_size), foreground='blue')
        
        # Configure the main window
        self.root.configure(bg='#f0f0f0')
        
        logger.info(f"Applied responsive styling for {screen_width}px width screen")
    
    def setup_ui(self):
        """Setup the main UI layout"""
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)
          # Title frame
        title_frame = ttk.Frame(self.root)
        title_frame.grid(row=0, column=0, sticky='ew', padx=10, pady=(10, 5))
        
        # Configure title frame grid
        title_frame.columnconfigure(0, weight=1)
        title_frame.columnconfigure(1, weight=0)
        
        title_label = ttk.Label(title_frame, 
                               text="Interactive Chart Generator v2.0", 
                               style='Title.TLabel')
        title_label.grid(row=0, column=0, sticky='w')
        
        version_label = ttk.Label(title_frame, 
                                 text="Advanced Interactive Features", 
                                 style='Info.TLabel')
        version_label.grid(row=0, column=1, sticky='e')        # Main content frame
        main_frame = ttk.Frame(self.root)
        main_frame.grid(row=1, column=0, sticky='nsew', padx=10, pady=5)
        
        # Get screen width for responsive sizing
        screen_width = self.root.winfo_screenwidth()
        min_panel_width = max(int(screen_width * 0.25), 400)  # 25% of screen or 400px minimum
        
        # Configure main frame grid for responsive 50/50 split
        main_frame.columnconfigure(0, weight=1, minsize=min_panel_width)  # Left panel (controls)
        main_frame.columnconfigure(1, weight=1, minsize=min_panel_width)  # Right panel (chart preview)
        main_frame.rowconfigure(0, weight=1)
        
        # Left panel (controls)
        left_panel = ttk.Frame(main_frame)
        left_panel.grid(row=0, column=0, sticky='nsew', padx=(0, 5))
        
        # Right panel (chart preview)
        right_panel = ttk.Frame(main_frame)
        right_panel.grid(row=0, column=1, sticky='nsew', padx=(5, 0))
        
        # Setup left panel
        self.setup_left_panel(left_panel)
        
        # Setup right panel
        self.setup_right_panel(right_panel)
        
        # Status frame
        self.status_frame = StatusFrame(self.root)
        self.status_frame.frame.grid(row=2, column=0, sticky='ew', padx=10, pady=(5, 10))    
    def setup_left_panel(self, parent):
        """Setup the left control panel"""        # Configure parent grid
        parent.columnconfigure(0, weight=1)
        parent.rowconfigure(0, weight=0)  # File selection
        parent.rowconfigure(1, weight=1)  # Axes selection
        parent.rowconfigure(2, weight=0)  # Chart options
        parent.rowconfigure(3, weight=0)  # Export options
        
        # File selection
        self.file_frame = FileSelectionFrame(parent, self.on_file_loaded)
        self.file_frame.set_preview_callback(self.on_preview_data)
        self.file_frame.set_clear_callback(self.on_clear_data)
        self.file_frame.frame.grid(row=0, column=0, sticky='ew', pady=5)
        
        # Initialize filter window (not shown until button is clicked)
        self.filter_window = FilterWindow(self.root, self.data_processor, self.on_data_filtered)
        
        # Add Filter buttons to the file frame (using pack to match existing structure)
        filter_button_frame = ttk.Frame(self.file_frame.frame)
        filter_button_frame.pack(fill='x', pady=(10, 0))
        
        # Add a separator for visual clarity
        separator = ttk.Separator(filter_button_frame, orient='horizontal')
        separator.pack(fill='x', pady=(0, 5))
        
        # Label for filter section
        filter_label = ttk.Label(filter_button_frame, text="Data Filtering:", font=('TkDefaultFont', 9, 'bold'))
        filter_label.pack(anchor='w', pady=(0, 5))
        
        # Buttons frame
        buttons_frame = ttk.Frame(filter_button_frame)
        buttons_frame.pack(fill='x')
        
        self.filter_button = ttk.Button(buttons_frame, text="🔍 Add Filter", 
                                       command=self.show_filter_window, state='disabled',
                                       width=15)
        self.filter_button.pack(side='left', padx=(0, 5))
        
        self.clear_filters_button = ttk.Button(buttons_frame, text="🗑️ Clear All Filters", 
                                             command=self.clear_all_filters, state='disabled',
                                             width=18)
        self.clear_filters_button.pack(side='left')
        
        # Status label for filters
        self.filter_status_label = ttk.Label(buttons_frame, text="No filters applied", 
                                           foreground="gray", font=('TkDefaultFont', 8))
        self.filter_status_label.pack(side='right', padx=(10, 0))
        
        # Axes selection
        self.axes_frame = AxesSelectionFrame(parent, self.on_axes_changed)
        self.axes_frame.frame.grid(row=1, column=0, sticky='nsew', pady=5)
        
        # Chart options (positioned right under axes selection as requested)
        self.options_frame = ChartOptionsFrame(parent, self.on_options_changed)
        self.options_frame.frame.grid(row=2, column=0, sticky='ew', pady=5)          # Export options frame (compact)
        export_frame = ttk.LabelFrame(parent, text="Export", padding=8)
        export_frame.grid(row=3, column=0, sticky='ew', pady=5)
        # Export buttons (compact)
        button_frame = ttk.Frame(export_frame)
        button_frame.grid(row=0, column=0, sticky='ew')
        
        ttk.Button(button_frame, text="PNG", width=8,
                  command=self.save_as_png).grid(row=0, column=0, padx=3)
        ttk.Button(button_frame, text="PDF", width=8,
                  command=self.save_as_pdf).grid(row=0, column=1, padx=3)
        ttk.Button(button_frame, text="Clipboard", width=10,
                  command=self.copy_to_clipboard).grid(row=0, column=2, padx=3)
    
    def setup_right_panel(self, parent):
        """Setup the right chart preview panel"""
        
        # Configure parent grid
        parent.columnconfigure(0, weight=1)
        parent.rowconfigure(0, weight=1)
          # Chart preview frame - takes up half the application as requested
        self.chart_preview_frame = ttk.LabelFrame(parent, text="Interactive Chart Preview", padding=10)
        self.chart_preview_frame.grid(row=0, column=0, sticky='nsew')
        
        # Configure chart preview frame grid
        self.chart_preview_frame.columnconfigure(0, weight=1)
        self.chart_preview_frame.rowconfigure(0, weight=1)
        
        # Initial message
        initial_frame = ttk.Frame(self.chart_preview_frame)
        initial_frame.grid(row=0, column=0, sticky='nsew')
        
        # Configure initial frame grid
        initial_frame.columnconfigure(0, weight=1)
        initial_frame.rowconfigure(0, weight=1)
        
        ttk.Label(initial_frame, 
                 text="Interactive Chart Preview\\n\\nLoad a CSV file and select axes to see your chart with:\\n" +
                      "• Navigation toolbar (zoom, pan, save)\\n" +
                      "• Interactive toggles (grid, legend, data points)\\n" +
                      "• Data cursor with tooltips\\n" +
                      "• Crosshair for precise inspection\\n" +
                      "• Adjustable line properties\\n" +
                      "• Statistics overlay\\n" +
                      "• Coordinate display",
                 justify='center',
                 font=('Arial', 11)).grid(row=0, column=0)
    def on_file_loaded(self, filepath: str) -> bool:
        """Handle file loading"""
        try:
            success = self.data_processor.load_csv_file(filepath)
            if success:
                # Update UI with new data - use all columns, not just numeric
                columns = self.data_processor.get_all_columns()
                if not columns:
                    self.status_frame.set_status("No columns found in file")
                    tk.messagebox.showerror("Error", "No columns found in the selected CSV file.")
                    return False
                
                self.axes_frame.update_columns(columns)
                
                # TODO: Update filter frame when Excel-style filtering is implemented
                # if hasattr(self.filter_frame, 'update_columns'):
                #     self.filter_frame.update_columns()
                
                # Log column types for user information
                numeric_cols = self.data_processor.get_numeric_columns()
                chartable_cols = self.data_processor.get_chartable_columns()
                logger.info(f"All columns: {columns}")
                logger.info(f"Numeric columns: {numeric_cols}")
                logger.info(f"Chartable columns: {chartable_cols}")
                
                # Update filter window when new data is loaded
                if hasattr(self, 'filter_window') and self.filter_window:
                    self.filter_window.refresh_data()
                
                # Enable filter buttons
                if hasattr(self, 'filter_button'):
                    self.filter_button.config(state='normal')
                if hasattr(self, 'clear_filters_button'):
                    self.clear_filters_button.config(state='normal')
                
                # Update status
                info = self.data_processor.get_data_info() if hasattr(self.data_processor, 'get_data_info') else {'filename': filepath, 'rows': len(self.data_processor.data) if self.data_processor.data is not None else 0, 'columns': len(self.data_processor.columns) if self.data_processor.columns else 0}
                self.status_frame.set_status(f"Loaded: {info['filename']}")
                self.status_frame.set_info(f"{info['rows']} rows, {len(columns)} columns ({len(numeric_cols)} numeric)")
                # Auto-update chart if axes are selected
                self.update_chart_preview()
                return True
            else:
                self.status_frame.set_status("Failed to load file")
                tk.messagebox.showerror("Error", f"Failed to load file: {filepath}\nCheck if the file is a valid CSV and not empty.")
                return False
        except Exception as e:
            logger.error(f"Error in file loading callback: {e}")
            self.status_frame.set_status("Error loading file")
            tk.messagebox.showerror("Error", f"Error loading file:\n{e}")
            return False
      # Filter window methods
    def show_filter_window(self):
        """Show the data filtering window"""
        if self.filter_window:
            self.filter_window.show_window()
    
    def clear_all_filters(self):
        """Clear all filters and restore original data"""
        if self.filter_window:
            self.filter_window.clear_all_filters()
            self.filter_window.apply_filters_to_processor()
            
        # Update filter status label
        if hasattr(self, 'filter_status_label'):
            self.filter_status_label.config(text="No filters applied", foreground="gray")

    # Excel-style filtering callback
    def on_data_filtered(self):
        """Handle data filter changes from Excel-style table"""
        try:
            # Update axes frame with available columns from filtered data
            if self.data_processor.data is not None and not self.data_processor.data.empty:
                columns = list(self.data_processor.data.columns)
                self.axes_frame.update_columns(columns)
            
            # Update chart preview with filtered data
            self.update_chart_preview()
            
            # Update status with filtered data info
            if self.data_processor.data is not None:
                filtered_rows = len(self.data_processor.data)
                total_rows = len(self.data_processor.original_data) if self.data_processor.original_data is not None else 0
                if filtered_rows != total_rows:
                    self.status_frame.set_info(f"Showing {filtered_rows} of {total_rows} rows (filtered)")
                    # Update filter status label
                    if hasattr(self, 'filter_status_label'):
                        active_filters = len(self.filter_window.filters) if self.filter_window else 0
                        self.filter_status_label.config(text=f"{active_filters} filter(s) active", foreground="blue")
                else:
                    self.status_frame.set_info(f"{filtered_rows} rows, {len(self.data_processor.get_all_columns())} columns")
                    # Update filter status label
                    if hasattr(self, 'filter_status_label'):
                        self.filter_status_label.config(text="No filters applied", foreground="gray")
            
            logger.info(f"Data filtered - showing {len(self.data_processor.data) if self.data_processor.data is not None else 0} rows")
        except Exception as e:
            logger.error(f"Error in data filter callback: {e}")
            self.status_frame.set_status("Error applying filters")

    def on_axes_changed(self):
        """Handle axes selection changes"""
        self.update_chart_preview()
    
    def on_options_changed(self):
        """Handle chart options changes"""
        self.update_chart_preview()
    
    def update_chart_preview(self):
        """Update the interactive chart preview"""
        try:
            # Check if we have data
            if self.data_processor.data is None:
                return
            
            # Get selected axes
            axes = self.axes_frame.get_selected_axes()
            if not axes['x_axis'] or not axes['y_axes']:
                return
              # Get chart options
            options = self.options_frame.get_options()
            
            # Get data with automatic conversion for charting
            x_data = self.data_processor.get_column_data_for_charting(axes['x_axis'])
            if x_data is None:
                self.status_frame.set_status("X-axis data cannot be converted for charting")
                return
                
            y_data_list = []
            y_labels = []
            
            for y_axis in axes['y_axes']:
                y_data = self.data_processor.get_column_data_for_charting(y_axis)
                if y_data is not None:
                    y_data_list.append(y_data)
                    y_labels.append(y_axis)
                else:
                    logger.warning(f"Could not convert Y-axis '{y_axis}' for charting")
            
            if not y_data_list:
                self.status_frame.set_status("No Y-axis data could be converted for charting")
                return
              # Create the interactive chart
            self.chart_generator.create_interactive_chart(
                parent_frame=self.chart_preview_frame,
                x_data=x_data,
                y_data_list=y_data_list,
                x_label=axes['x_axis'],
                y_labels=y_labels,
                chart_type=options['chart_type'],
                color_scheme=options['color_scheme'],
                dual_axis=options['dual_axis'],
                log_x=options['log_x'],
                log_y=options['log_y']
            )
            
            # Update status
            self.status_frame.set_status("Chart updated")
            self.status_frame.set_info(f"Showing {len(y_data_list)} series with interactive features")
            
            logger.info(f"Chart preview updated: {len(y_data_list)} series, {options['chart_type']} type")
            
        except Exception as e:
            logger.error(f"Error updating chart preview: {e}")
            self.status_frame.set_status("Error updating chart")
    
    def save_as_png(self):
        """Save chart as PNG"""
        if self.chart_generator.figure is None:
            tk.messagebox.showwarning("Warning", "No chart to save. Please create a chart first.")
            return
        
        from tkinter import filedialog
        filename = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("All files", "*.*")],
            title="Save chart as PNG"
        )
        
        if filename:
            try:
                self.chart_generator.figure.savefig(filename, dpi=300, bbox_inches='tight')
                self.status_frame.set_status(f"Chart saved as PNG: {filename}")
                tk.messagebox.showinfo("Success", f"Chart saved successfully as:\\n{filename}")
            except Exception as e:
                logger.error(f"Error saving PNG: {e}")
                tk.messagebox.showerror("Error", f"Failed to save chart:\\n{e}")
    
    def save_as_pdf(self):
        """Save chart as PDF"""
        if self.chart_generator.figure is None:
            tk.messagebox.showwarning("Warning", "No chart to save. Please create a chart first.")
            return
        
        from tkinter import filedialog
        filename = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")],
            title="Save chart as PDF"
        )
        
        if filename:
            try:
                self.chart_generator.figure.savefig(filename, bbox_inches='tight')
                self.status_frame.set_status(f"Chart saved as PDF: {filename}")
                tk.messagebox.showinfo("Success", f"Chart saved successfully as:\\n{filename}")
            except Exception as e:
                logger.error(f"Error saving PDF: {e}")
                tk.messagebox.showerror("Error", f"Failed to save chart:\\n{e}")
    
    def copy_to_clipboard(self):
        """Copy chart to clipboard"""
        if self.chart_generator.figure is None:
            tk.messagebox.showwarning("Warning", "No chart to copy. Please create a chart first.")
            return
        
        try:
            import io
            from PIL import Image
            
            # Save figure to bytes
            buf = io.BytesIO()
            self.chart_generator.figure.savefig(buf, format='png', dpi=300, bbox_inches='tight')
            buf.seek(0)
            
            # Convert to PIL Image
            img = Image.open(buf)
            
            # Copy to clipboard (Windows)
            import win32clipboard
            from io import BytesIO
            
            output = BytesIO()
            img.save(output, 'BMP')
            data = output.getvalue()[14:]  # Remove BMP header
            output.close()
            
            win32clipboard.OpenClipboard()
            win32clipboard.EmptyClipboard()
            win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
            win32clipboard.CloseClipboard()
            
            self.status_frame.set_status("Chart copied to clipboard")
            tk.messagebox.showinfo("Success", "Chart copied to clipboard successfully!")
        except ImportError:
            tk.messagebox.showwarning("Warning", "Clipboard functionality requires PIL and win32clipboard.\\nPlease install: pip install pillow pywin32")
        except Exception as e:
            logger.error(f"Error copying to clipboard: {e}")
            tk.messagebox.showerror("Error", f"Failed to copy chart to clipboard:\\n{e}")
    
    def on_preview_data(self):
        """Show a preview of the loaded data in a popup window"""
        if self.data_processor.data is None:
            tk.messagebox.showinfo("Preview Data", "No data loaded.")
            return
        from ui.dialogs import show_data_preview_dialog
        show_data_preview_dialog(self.root, self.data_processor.data)

    def on_clear_data(self):
        """Clear loaded data and reset UI"""
        self.data_processor.clear_data()
        self.axes_frame.update_columns([])
        
        # Clear filter window
        if hasattr(self, 'filter_window') and self.filter_window:
            self.filter_window.clear_all_filters()
        
        # Disable filter buttons
        if hasattr(self, 'filter_button'):
            self.filter_button.config(state='disabled')
        if hasattr(self, 'clear_filters_button'):
            self.clear_filters_button.config(state='disabled')
        
        self.status_frame.set_status("Data cleared")
        self.status_frame.set_info("")
        self.file_frame.file_label.config(text="No files selected", foreground="gray")
        self.file_frame.current_files = []  # Clear the files list
        self.update_chart_preview()
    
    def on_window_resize(self, event):
        """Handle window resize events"""
        # Only handle resize events for the root window
        if event.widget == self.root:
            # Update chart size if there's an active chart
            if hasattr(self, 'chart_generator') and self.chart_generator.figure is not None:
                # Debounce resize events - only update after 500ms of no resize
                if hasattr(self, '_resize_timer'):
                    self.root.after_cancel(self._resize_timer)
                self._resize_timer = self.root.after(500, self.update_chart_preview)

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
        self.chart_generator = InteractiveChartGenerator()
        
        # UI Components
        self.file_frame = None
        self.axes_frame = None
        self.options_frame = None
        self.status_frame = None
        self.chart_preview_frame = None
        
        self.setup_ui()
        self.setup_styles()
        
        logger.info("Interactive Chart Application initialized")
    
    def setup_styles(self):
        """Setup UI styles"""
        style = ttk.Style()
        
        # Configure styles
        style.configure('Title.TLabel', font=('Arial', 12, 'bold'))
        style.configure('Header.TLabel', font=('Arial', 10, 'bold'))
        style.configure('Info.TLabel', font=('Arial', 9), foreground='blue')
        
        # Configure the main window
        self.root.configure(bg='#f0f0f0')
    
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
        version_label.grid(row=0, column=1, sticky='e')
          # Main content frame
        main_frame = ttk.Frame(self.root)
        main_frame.grid(row=1, column=0, sticky='nsew', padx=10, pady=5)
        
        # Configure main frame grid for exact 50/50 split
        main_frame.columnconfigure(0, weight=1, minsize=600)  # Left panel (controls) - minimum width
        main_frame.columnconfigure(1, weight=1, minsize=600)  # Right panel (chart preview) - equal weight
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
        """Setup the left control panel"""
        
        # Configure parent grid
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
        
        # Axes selection
        self.axes_frame = AxesSelectionFrame(parent, self.on_axes_changed)
        self.axes_frame.frame.grid(row=1, column=0, sticky='nsew', pady=5)
        
        # Chart options (positioned right under axes selection as requested)
        self.options_frame = ChartOptionsFrame(parent, self.on_options_changed)
        self.options_frame.frame.grid(row=2, column=0, sticky='ew', pady=5)
          # Export options frame (compact)
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
                # Update UI with new data
                columns = self.data_processor.get_numeric_columns()
                if not columns:
                    self.status_frame.set_status("No numeric columns found in file")
                    tk.messagebox.showerror("Error", "No numeric columns found in the selected CSV file.")
                    return False
                self.axes_frame.update_columns(columns)
                # Update status
                info = self.data_processor.get_data_info() if hasattr(self.data_processor, 'get_data_info') else {'filename': filepath, 'rows': len(self.data_processor.data) if self.data_processor.data is not None else 0, 'columns': len(self.data_processor.columns) if self.data_processor.columns else 0}
                self.status_frame.set_status(f"Loaded: {info['filename']}")
                self.status_frame.set_info(f"{info['rows']} rows, {info['columns']} columns")
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
            
            # Get data
            x_data = self.data_processor.get_column_data(axes['x_axis'])
            y_data_list = []
            y_labels = []
            
            for y_axis in axes['y_axes']:
                y_data = self.data_processor.get_column_data(y_axis)
                if y_data is not None:
                    y_data_list.append(y_data)
                    y_labels.append(y_axis)
            
            if not y_data_list:
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
        self.status_frame.set_status("Data cleared")
        self.status_frame.set_info("")
        self.file_frame.file_label.config(text="No files selected", foreground="gray")
        self.file_frame.current_files = []  # Clear the files list
        self.update_chart_preview()

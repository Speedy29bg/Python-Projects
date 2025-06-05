"""
Core application class for the Lab Chart Generator

This module contains the refactored LabChartGenerator class that orchestrates the overall
functionality of the application, delegating to the modular components.

Author: Lab Chart Tools Team
"""

import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import os
import logging
from typing import List, Dict

# Import UI components
from modules.ui.main_window import MainWindow
from modules.ui.file_selection import FileSelectionFrame
from modules.ui.axes_selection import AxesSelectionFrame
from modules.ui.chart_options import ChartOptionsFrame
from modules.ui.preview_frame import PreviewFrame
from modules.ui.output_options import OutputOptionsFrame

# Import data components
from modules.data.file_handler import FileDataHandler

# Import other modules
from modules.chart_generator import create_preview_plot, clear_figure, create_tkinter_canvas
from modules.excel_export import generate_excel_workbook, export_figure
from modules.data_analysis import calculate_statistics, filter_outliers, smooth_data

class LabChartGenerator:
    """
    Main class for the Laboratory Chart Generator application
    
    This class provides a comprehensive GUI for loading, visualizing and exporting
    chart data from CSV files, delegating to specialized component modules.
    """
    
    def __init__(self, root: tk.Tk):
        """
        Constructor initializes the application with modular components
        
        Args:
            root: The tkinter root window instance
        """
        self.root = root
        self.root.title("Lab Chart Generator")
        
        # Initialize main window
        self.main_window = MainWindow(root, self)
        
        # Initialize data handler
        self.data_handler = FileDataHandler(self)
        
        # Create UI components with references to the main app instance
        self.file_selection = FileSelectionFrame(self.main_window.main_frame, self)
        self.axes_selection = AxesSelectionFrame(self.main_window.main_frame, self)
        self.chart_options = ChartOptionsFrame(self.main_window.main_frame, self)
        self.preview = PreviewFrame(self.main_window.main_frame, self)
        self.output_options = OutputOptionsFrame(self.main_window.main_frame, self)
        
        # Store reference to status label
        self.status_label = self.main_window.status_label
        
        logging.info("Application initialized with modular components")
    
    def select_files(self):
        """Handle file selection and load column headers"""
        success = self.data_handler.select_files(filedialog.askopenfilenames, self.status_label)
        if success:
            self.file_selection.update_file_label(len(self.data_handler.files))
    
    def detect_headers_and_populate_listboxes(self):
        """Detect headers from the first file and populate column selection listboxes"""
        if not self.data_handler.files or not self.data_handler.file_data_cache:
            return
        
        try:
            # Get first file from cache
            first_file = self.data_handler.files[0]
            if first_file in self.data_handler.file_data_cache:
                df = self.data_handler.file_data_cache[first_file]
                
                # Clear existing items in axes selection listboxes
                self.axes_selection.clear_listboxes()
                
                # Add headers to all listboxes
                self.data_handler.column_headers = list(df.columns)
                self.axes_selection.populate_listboxes(self.data_handler.column_headers)
                
                self.status_label.config(text=f"Loaded {len(self.data_handler.column_headers)} columns from {os.path.basename(first_file)}")
            else:
                self.status_label.config(text="Selected file is not in cache. Please try again.")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to detect headers: {str(e)}")
            self.status_label.config(text=f"Error detecting headers: {str(e)}")
    
    def preview_data(self):
        """Show a preview of the data in the first selected file"""
        if not self.data_handler.files:
            messagebox.showinfo("Info", "No files selected")
            return
        
        try:
            # Get data from the first file
            file_path = self.data_handler.files[0]
            df = self.data_handler.get_data_from_file(file_path)
            
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
    
    def update_preview(self):
        """Update the chart preview based on current selections"""
        if not self.data_handler.files or not self.data_handler.column_headers:
            return
            
        try:
            # Get selected columns from axes selection component
            x_selected, y_selected, secondary_selected = self.axes_selection.get_selected_items(self.data_handler.column_headers)
            
            if not x_selected:
                # No X-axis selected, can't create chart
                if self.preview.figure:
                    self.preview.figure, self.preview.canvas = clear_figure(self.preview.figure, self.preview.canvas)
                return
                
            # Get chart settings from options component
            chart_settings = self.chart_options.get_chart_settings()
            
            # Get data from first file
            file_path = self.data_handler.files[0]
            df = self.data_handler.get_data_from_file(file_path)
            
            # Clear current chart
            if self.preview.figure:
                self.preview.figure, self.preview.canvas = clear_figure(self.preview.figure, self.preview.canvas)
                
            # Create the figure with the first X column and all selected Y columns
            self.preview.figure, chart_info = create_preview_plot(
                df, 
                x_selected[0], 
                y_selected, 
                secondary_selected, 
                chart_settings,
                df
            )
            
            # Add figure to the preview frame
            if self.preview.figure:
                self.preview.canvas = create_tkinter_canvas(self.preview.figure, self.preview.preview_frame)
                
                # Update status with any chart information
                if 'info' in chart_info:
                    self.status_label.config(text=chart_info['info'])
                else:
                    self.status_label.config(text=f"Chart preview updated")
            else:
                # Error creating chart
                if 'error' in chart_info:
                    self.status_label.config(text=f"Error: {chart_info['error']}")
                else:
                    self.status_label.config(text="Error creating preview chart")
                    
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update preview: {str(e)}")
            self.status_label.config(text=f"Error updating preview: {str(e)}")
    
    def generate_charts(self):
        """Generate chart workbooks for all selected files"""
        if not self.data_handler.files:
            messagebox.showinfo("Info", "No files selected")
            return
            
        try:
            # Get output filename
            output_name = self.output_options.get_output_filename()
            if not output_name:
                output_name = "Lab_Charts"
                
            # Get selected axes
            x_selected, y_selected, secondary_selected = self.axes_selection.get_selected_items(self.data_handler.column_headers)
            
            if not x_selected or not (y_selected or secondary_selected):
                messagebox.showinfo("Info", "Please select X-axis and at least one Y-axis column")
                return
                
            # Get chart settings from options component
            chart_settings = self.chart_options.get_chart_settings()
            
            # Create Excel workbook with charts for each file
            export_format = chart_settings['export_format']
            
            if export_format == 'xlsx':
                # Export to Excel with embedded charts
                result = generate_excel_workbook(
                    self.data_handler.files,
                    self.data_handler.file_data_cache,
                    x_selected[0],
                    y_selected,
                    secondary_selected,
                    chart_settings,
                    output_name
                )
                
                if result['success']:
                    messagebox.showinfo("Success", f"Charts exported to {result['filename']}")
                    self.status_label.config(text=f"Charts exported to {result['filename']}")
                else:
                    messagebox.showerror("Error", f"Failed to export charts: {result['error']}")
                    self.status_label.config(text=f"Error: {result['error']}")
            else:
                # Export individual chart files (PNG, PDF)
                for file_path in self.data_handler.files:
                    df = self.data_handler.get_data_from_file(file_path)
                    basename = os.path.splitext(os.path.basename(file_path))[0]
                    
                    figure, _ = create_preview_plot(
                        df,
                        x_selected[0],
                        y_selected,
                        secondary_selected,
                        chart_settings,
                        df
                    )
                    
                    if figure:
                        filename = f"{output_name}_{basename}.{export_format}"
                        export_figure(figure, filename, export_format)
                        messagebox.showinfo("Success", f"Chart exported to {filename}")
                        self.status_label.config(text=f"Chart exported to {filename}")
                        
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate charts: {str(e)}")
            self.status_label.config(text=f"Error generating charts: {str(e)}")
    
    def export_current_chart(self):
        """Export the current chart preview to a file"""
        if not self.preview.figure:
            messagebox.showinfo("Info", "No chart to export")
            return
            
        try:
            # Get output filename
            output_name = self.output_options.get_output_filename()
            if not output_name:
                output_name = "Lab_Chart"
                
            # Get export format
            export_format = self.chart_options.export_format.get()
            
            # Export the current figure
            filename = f"{output_name}.{export_format}"
            export_figure(self.preview.figure, filename, export_format)
            
            messagebox.showinfo("Success", f"Chart exported to {filename}")
            self.status_label.config(text=f"Chart exported to {filename}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export chart: {str(e)}")
            self.status_label.config(text=f"Error exporting chart: {str(e)}")
    
    def clear_selections(self):
        """Clear all selections and reset UI state"""
        try:
            # Clear axes selections
            self.axes_selection.clear_listboxes()
            
            # Clear preview
            if self.preview.figure:
                self.preview.figure, self.preview.canvas = clear_figure(self.preview.figure, self.preview.canvas)
                
            # Reset file data
            self.data_handler.files = []
            self.data_handler.file_data_cache = {}
            self.data_handler.column_headers = []
            
            # Update file label
            self.file_selection.update_file_label(0)
            
            # Reset status
            self.status_label.config(text="All selections cleared")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to clear selections: {str(e)}")
            self.status_label.config(text=f"Error clearing selections: {str(e)}")
    
    def analyze_data(self):
        """Open data analysis dialog with statistics and visualization options"""
        # This method would be implemented to handle data analysis
        # For brevity, the full implementation is not shown here
        self.status_label.config(text="Data analysis functionality not implemented in this example")
        messagebox.showinfo("Info", "Data analysis functionality would be implemented in a separate module")

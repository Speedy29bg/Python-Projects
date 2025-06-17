"""
Core application class for the Lab Chart Generator

This module contains the refactored LabChartGenerator class that orchestrates the overall
functionality of the application, delegating to the modular components.


Author: Speedy29bg
"""

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pandas as pd
import os
import logging
from typing import List, Dict

# Import UI components
from modules.app_modules.ui.main_window import MainWindow
from modules.app_modules.ui.file_selection import FileSelectionFrame
from modules.app_modules.ui.axes_selection import AxesSelectionFrame
from modules.app_modules.ui.chart_options import ChartOptionsFrame
from modules.app_modules.ui.preview_frame import PreviewFrame
from modules.app_modules.ui.output_options import OutputOptionsFrame

# Import data components
from modules.app_modules.data.file_handler import FileDataHandler

# Import other modules
from modules.chart_generator import create_preview_plot, clear_figure, create_tkinter_canvas
from modules.export_module.excel import generate_excel_workbook
from modules.export_module.figure_export import export_figure
from modules.data_analysis import calculate_statistics, filter_outliers, smooth_data

# Helper function for data analysis
def analyze_correlation(df):
    """
    Analyze correlation between columns in the DataFrame
    
    Args:
        df: Pandas DataFrame with numeric columns
        
    Returns:
        str: Text representation of correlation analysis
    """
    corr_matrix = df.corr()
    result = "Correlation Matrix:\n\n"
    result += str(corr_matrix.round(3)) + "\n\n"
    
    # Find highest correlations
    corr_pairs = []
    for i in range(len(corr_matrix.columns)):
        for j in range(i+1, len(corr_matrix.columns)):
            col1 = corr_matrix.columns[i]
            col2 = corr_matrix.columns[j]
            corr = corr_matrix.iloc[i, j]
            corr_pairs.append((col1, col2, corr))
    
    # Sort by absolute correlation value
    corr_pairs.sort(key=lambda x: abs(x[2]), reverse=True)
    
    # Add sorted results
    result += "Top Correlations:\n"
    for col1, col2, corr in corr_pairs[:5]:  # Show top 5
        result += f"{col1} ↔ {col2}: {corr:.3f}\n"
        
    return result

class LabChartGenerator:
    """
    Main class for the Laboratory Chart Generator application
    
    This class provides a comprehensive GUI for loading, visualizing and exporting
    chart data from CSV files, delegating to specialized component modules.
    """
    
    def __init__(self, root: tk.Tk):
        """Initialize the application interface and components
        
        Args:
            root: The tkinter root window
        """
        # Store references to the window and internal state
        self.root = root
        self.files = []
        self.file_data_cache = {}
        self.column_headers = []
        self.current_figure = None
          # Set up the main application container
        self.main_window = MainWindow(self.root)
        
        # Create status bar at the bottom
        self.status_label = self.main_window.create_status_bar()
        self.status_label = self.main_window.create_status_bar()
        
        # Setup the file selection frame
        self.file_selection_frame = FileSelectionFrame(
            self.main_window.get_top_frame(),
            self
        )
        
        # Setup the axes selection frame
        self.axes_selection_frame = AxesSelectionFrame(
            self.main_window.get_middle_left_frame(),
            self
        )
        
        # Setup the chart options frame
        self.chart_options_frame = ChartOptionsFrame(
            self.main_window.get_middle_right_frame(),
            self
        )
        
        # Setup the preview frame
        self.preview_frame = PreviewFrame(
            self.main_window.get_chart_frame(),
            self
        )
        
        # Setup the output options frame
        self.output_options_frame = OutputOptionsFrame(
            self.main_window.get_bottom_frame(),
            self
        )
        
        # Create file data handler
        self.file_data_handler = FileDataHandler(self)
        
        # Initial UI state update
        self.update_status("Ready")
        
        logging.info("Application initialized with modular components")
        
    def update_status(self, message):
        """
        Update the status bar message
        
        Args:
            message (str): The message to display in the status bar
        """
        if hasattr(self, 'status_label') and self.status_label:
            self.status_label.config(text=message)
            self.root.update_idletasks()
            
    def select_files(self):
        """Handle file selection and load column headers"""
        selected_files = filedialog.askopenfilenames(
            title="Select CSV Data Files",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        
        if selected_files:
            self.file_data_handler.files = selected_files
            self.file_data_handler.load_files_in_background(
                selected_files, 
                self.detect_headers_and_populate_listboxes, 
                self.status_label
            )
            
            # Update instance variables
            self.files = self.file_data_handler.files
            self.file_data_cache = self.file_data_handler.file_data_cache
            self.file_selection_frame.update_file_label(len(selected_files))
            self.update_status(f"Selected {len(selected_files)} files")
        
        self.files = self.file_data_handler.files
        self.file_data_cache = self.file_data_handler.file_data_cache
        self.column_headers = self.file_data_handler.column_headers
        
        if self.files:
            self.detect_headers_and_populate_listboxes()
    
    def detect_headers_and_populate_listboxes(self):
        """Detect headers from the first file and populate column selection listboxes"""
        if not self.files or not self.file_data_cache:
            self.status_label.config(text="No valid headers found in selected files")
            return

        # Get first file from cache
        first_file = self.files[0]
        if first_file in self.file_data_cache:
            df = self.file_data_cache[first_file]
            self.column_headers = list(df.columns)
            self.axes_selection_frame.clear_listboxes()
            self.axes_selection_frame.populate_listboxes(self.column_headers)
            self.status_label.config(text=f"{len(self.files)} file(s) loaded successfully")
        else:
            self.status_label.config(text="Selected file is not in cache. Please try again.")
    
    def preview_data(self):
        """Show a preview of the data in the first selected file"""
        if not self.files:
            self.status_label.config(text="No files selected")
            return
            
        try:
            first_file = self.files[0]
            df = self.file_data_handler.get_data_from_file(first_file)
            
            if df is not None and not df.empty:
                from modules.ui_components import create_data_preview
                preview_window = create_data_preview(self.root, df, f"Data Preview: {os.path.basename(first_file)}")
                self.status_label.config(text=f"Previewing data from {os.path.basename(first_file)}")
            else:
                messagebox.showerror("Error", "Could not load data from the selected file")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to preview data: {str(e)}")
            self.status_label.config(text=f"Error: {str(e)}")
    
    def update_preview(self):
        """Update the chart preview based on current selections"""
        if not self.files:
            self.status_label.config(text="No files selected")
            return
        
        # Get selected columns
        x_axis = self.axes_selection_frame.get_x_column()
        y_axes = self.axes_selection_frame.get_primary_y_columns()
        secondary_axes = self.axes_selection_frame.get_secondary_y_columns()
        
        if not x_axis or not y_axes:
            self.status_label.config(text="Please select X-axis and at least one Y-axis column")
            return
        
        # Get chart options
        chart_settings = self.chart_options_frame.get_settings()
        
        try:
            # Get the data from the first file
            df = self.file_data_handler.get_data_from_file(self.files[0])
            if df is None or df.empty:
                self.status_label.config(text="No valid data in selected file")
                return
                
            # Process the data for scaling
            from modules.data_processor import process_data_for_scaling
            processed_df = process_data_for_scaling(df, x_axis, y_axes, secondary_axes, chart_settings)
            
            # Create the preview plot (matplotlib Figure)
            if self.current_figure and self.canvas:
                self.current_figure, self.canvas = clear_figure(self.current_figure, self.canvas)
            self.current_figure, chart_info = create_preview_plot(
                processed_df,
                x_axis,
                y_axes,
                secondary_axes,
                chart_settings,
                original_df=df
            )
            if self.current_figure:
                self.canvas = create_tkinter_canvas(self.current_figure, self.preview_frame.preview_frame)
                self.status_label.config(text="Chart preview updated")
            else:
                self.status_label.config(text="Failed to update chart preview")
                
        except Exception as e:
            logging.exception("Error updating preview")
            self.status_label.config(text=f"Error: {str(e)}")
            messagebox.showerror("Error", f"Failed to update preview: {str(e)}")
    
    def generate_charts(self):
        """Generate chart workbooks or image exports for all selected files"""
        if not self.files:
            self.status_label.config(text="No files selected")
            return

        x_axis = self.axes_selection_frame.get_x_column()
        y_axes = self.axes_selection_frame.get_primary_y_columns()
        secondary_axes = self.axes_selection_frame.get_secondary_y_columns()

        if not x_axis or not y_axes:
            self.status_label.config(text="Please select X-axis and at least one Y-axis column")
            return

        # Get chart options
        chart_settings = self.chart_options_frame.get_settings()
        export_format = chart_settings.get('export_format', 'xlsx')

        if export_format == 'xlsx':
            # Ask for save location (directory)
            save_dir = filedialog.askdirectory(title="Select directory to save Excel workbook")
            if not save_dir:
                return
            output_name = "Lab_Charts"
            try:
                # Call generate_excel_workbook and handle result dict
                result = generate_excel_workbook(
                    self.files,
                    self.file_data_cache,
                    x_axis,
                    y_axes,
                    secondary_axes,
                    chart_settings,
                    output_name
                )
                if result.get('success'):
                    # Move file to selected directory if needed
                    src = result['filename']
                    dst = os.path.join(save_dir, os.path.basename(src))
                    if os.path.abspath(src) != os.path.abspath(dst):
                        import shutil
                        shutil.move(src, dst)
                    msg = f"Charts exported to {dst}\nFiles processed: {result.get('processed_files', '?')}\nFiles skipped: {result.get('skipped_files', '?')}"
                    self.status_label.config(text=f"Charts exported to {dst}")
                    messagebox.showinfo("Success", msg)
                else:
                    error_msg = result.get('error', 'Unknown error')
                    self.status_label.config(text=f"Error: {error_msg}")
                    messagebox.showerror("Error", f"Failed to export charts: {error_msg}")
            except Exception as e:
                logging.exception("Error generating charts")
                self.status_label.config(text=f"Error: {str(e)}")
                messagebox.showerror("Error", f"Failed to generate charts: {str(e)}")
        elif export_format in ("png", "pdf"):
            # Ask for save location (directory)
            save_dir = filedialog.askdirectory(title=f"Select directory to save {export_format.upper()} files")
            if not save_dir:
                return
            output_name = "Lab_Charts"
            exported = 0
            skipped = 0
            errors = []
            for file_path in self.files:
                try:
                    df = self.file_data_handler.get_data_from_file(file_path)
                    if df is None or df.empty:
                        skipped += 1
                        continue
                    # Process data for scaling
                    from modules.data_processor import process_data_for_scaling
                    processed_df = process_data_for_scaling(df, x_axis, y_axes, secondary_axes, chart_settings)
                    # Generate chart
                    figure, chart_info = create_preview_plot(
                        processed_df,
                        x_axis,
                        y_axes,
                        secondary_axes,
                        chart_settings,
                        original_df=df
                    )
                    if figure is None:
                        skipped += 1
                        continue
                    basename = os.path.splitext(os.path.basename(file_path))[0]
                    filename = f"{output_name}_{basename}.{export_format}"
                    out_path = os.path.join(save_dir, filename)
                    export_figure(figure, out_path, export_format)
                    exported += 1
                except Exception as e:
                    skipped += 1
                    errors.append(f"{os.path.basename(file_path)}: {str(e)}")
            msg = f"Exported {exported} file(s) as {export_format.upper()}\nSkipped {skipped} file(s)"
            if errors:
                msg += "\nErrors:\n" + "\n".join(errors)
            self.status_label.config(text=msg)
            if exported:
                messagebox.showinfo("Success", msg)
            else:
                messagebox.showerror("Error", msg)
        else:
            self.status_label.config(text=f"Unsupported export format: {export_format}")
            messagebox.showerror("Error", f"Unsupported export format: {export_format}")
    
    def export_current_chart(self):
        """Export the current chart preview to a file"""
        if self.current_figure is None:
            self.status_label.config(text="No chart to export")
            return
            
        # Get selected export format
        export_format = self.output_options_frame.get_export_format()
        
        if export_format == "excel":
            filetypes = [("Excel files", "*.xlsx")]
            default_ext = ".xlsx"
        elif export_format == "png":
            filetypes = [("PNG files", "*.png")]
            default_ext = ".png"
        elif export_format == "pdf":
            filetypes = [("PDF files", "*.pdf")]
            default_ext = ".pdf"
        else:
            self.status_label.config(text="Invalid export format")
            return
            
        # Ask for save location
        save_path = filedialog.asksaveasfilename(
            title="Save Chart As",
            filetypes=filetypes,
            defaultextension=default_ext
        )
        
        if not save_path:
            return
            
        try:
            if export_format == "excel":
                # For Excel, we need to recreate the chart in Excel format
                x_axis = self.axes_selection_frame.get_x_column()
                y_axes = self.axes_selection_frame.get_primary_y_columns()
                secondary_axes = self.axes_selection_frame.get_secondary_y_columns()
                chart_settings = self.chart_options_frame.get_settings()
                
                df = self.file_data_handler.get_data_from_file(self.files[0])
                from modules.data_processor import process_data_for_scaling
                processed_df = process_data_for_scaling(df, x_axis, y_axes, secondary_axes, chart_settings)
                
                generate_excel_workbook(
                    save_path,
                    processed_df, 
                    x_axis, 
                    y_axes, 
                    secondary_axes,
                    chart_settings,
                    original_df=df
                )
            else:
                # For image formats, export directly from matplotlib figure
                export_figure(self.current_figure, save_path, export_format)
                
            self.status_label.config(text=f"Chart exported successfully as {export_format.upper()}")
            messagebox.showinfo("Success", f"Chart exported successfully as {export_format.upper()}")
            
        except Exception as e:
            logging.exception("Error exporting chart")
            self.status_label.config(text=f"Error: {str(e)}")
            messagebox.showerror("Error", f"Failed to export chart: {str(e)}")
    
    def clear_selections(self):
        """Clear all selections and reset the application state"""
        # Clear file list and data cache
        self.files = []
        self.file_data_cache = {}
        self.column_headers = []
        self.file_data_handler.files = []
        self.file_data_handler.file_data_cache = {}
        self.file_data_handler.column_headers = []
        
        # Clear UI selections
        self.file_selection_frame.clear_selections()
        self.axes_selection_frame.clear_selections()
        
        # Clear chart
        self.current_figure, self.canvas = self.preview_frame.clear_plot(
            self.current_figure, 
            self.canvas
        )
        
        # Reset status
        self.status_label.config(text="Ready. Please select CSV files to begin.")
    
    def analyze_data(self):
        """Perform statistical analysis on the selected columns"""
        if not self.files:
            self.status_label.config(text="No files selected")
            return
        
        try:
            # Get data from the first file
            df = self.file_data_handler.get_data_from_file(self.files[0])
            if df is None or df.empty:
                self.status_label.config(text="No valid data in selected file")
                return
                
            # Get selected columns for analysis
            all_y_axes = (self.axes_selection_frame.get_primary_y_columns() + 
                         self.axes_selection_frame.get_secondary_y_columns())
            
            if not all_y_axes:
                self.status_label.config(text="Please select at least one column for analysis")
                messagebox.showwarning("Warning", "Please select at least one column for Y-axis")
                return
                
            # Create analysis window
            analysis_window = tk.Toplevel(self.root)
            analysis_window.title("Data Analysis")
            analysis_window.geometry("800x600")
            analysis_window.transient(self.root)
            
            # Create a notebook for different analysis tabs
            notebook = ttk.Notebook(analysis_window)
            notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
            # 1. Statistics tab
            stats_frame = ttk.Frame(notebook)
            notebook.add(stats_frame, text="Statistics")
            
            # Create text widget for statistics
            stats_text = tk.Text(stats_frame, wrap=tk.WORD, height=20, width=80)
            stats_scroll = ttk.Scrollbar(stats_frame, orient=tk.VERTICAL, command=stats_text.yview)
            stats_text.configure(yscrollcommand=stats_scroll.set)
            
            stats_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
            stats_scroll.pack(side=tk.RIGHT, fill=tk.Y)
            
            # Calculate and display statistics
            statistics = calculate_statistics(df, all_y_axes)
            # Format statistics for display
            if statistics:
                stats_text.insert(tk.END, f"Statistical Analysis for Selected Columns\n")
                stats_text.insert(tk.END, f"{'=' * 70}\n\n")
                for column, column_stats in statistics.items():
                    stats_text.insert(tk.END, f"Column: {column}\n")
                    stats_text.insert(tk.END, f"{'-' * 70}\n")
                    for stat_name, stat_value in column_stats.items():
                        stats_text.insert(tk.END, f"{stat_name.capitalize()}: {stat_value}\n")
                    stats_text.insert(tk.END, "\n")
            else:
                stats_text.insert(tk.END, "No statistics available for the selected columns.")
            stats_text.configure(state="disabled")  # Make read-only
            
            # 2. Correlation tab
            corr_frame = ttk.Frame(notebook)
            notebook.add(corr_frame, text="Correlation")
            
            # Only add correlation content if we have numeric columns
            numeric_cols = df[all_y_axes].select_dtypes(include=['number']).columns.tolist()
            if len(numeric_cols) > 1:
                # Calculate correlation
                corr_result = analyze_correlation(df[numeric_cols])
                
                # Display correlation matrix
                corr_text = tk.Text(corr_frame, wrap=tk.WORD, height=20, width=80)
                corr_scroll = ttk.Scrollbar(corr_frame, orient=tk.VERTICAL, command=corr_text.yview)
                corr_text.configure(yscrollcommand=corr_scroll.set)
                
                corr_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
                corr_scroll.pack(side=tk.RIGHT, fill=tk.Y)
                
                corr_text.insert(tk.END, corr_result)
                corr_text.configure(state="disabled")  # Make read-only
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
                outlier_text.configure(state="normal")
                outlier_text.delete(1.0, tk.END)
                
                method = outlier_method.get()
                threshold = threshold_var.get()
                
                for col in numeric_cols:
                    try:
                        outliers, summary = filter_outliers(df[col], method=method, threshold=threshold)
                        outlier_text.insert(tk.END, f"\n-- {col} --\n{summary}\n\n")
                    except Exception as e:
                        outlier_text.insert(tk.END, f"\n-- {col} --\nError: {str(e)}\n\n")
                
                outlier_text.configure(state="disabled")
            
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
            window_var = tk.IntVar(value=5)
            window_entry = ttk.Entry(transform_controls, textvariable=window_var, width=5)
            window_entry.pack(side=tk.LEFT, padx=5)
            
            # Create frame for displaying transformation results
            result_frame = ttk.Frame(transform_frame)
            result_frame.pack(fill=tk.BOTH, expand=True, pady=10)
            
            # Create transformation function
            def apply_transformation():
                # Clear previous results
                for widget in result_frame.winfo_children():
                    widget.destroy()
                
                # Select column from dropdown
                col = column_var.get()
                if not col:
                    return
                
                try:
                    # Apply smoothing
                    method = smooth_method.get()
                    window = window_var.get()
                    
                    smoothed = smooth_data(df[col], method=method, window_size=window)
                    
                    # Create a small preview chart comparing original and smoothed data
                    import matplotlib.pyplot as plt
                    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
                    
                    fig, ax = plt.subplots(figsize=(8, 4))
                    ax.plot(df[col].values, label="Original", alpha=0.7)
                    ax.plot(smoothed.values, label=f"Smoothed ({method})", linewidth=2)
                    ax.set_title(f"Smoothing Preview: {col}")
                    ax.legend()
                    ax.grid(True)
                    
                    # Embed the plot
                    canvas = FigureCanvasTkAgg(fig, master=result_frame)
                    canvas.draw()
                    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
                    
                except Exception as e:
                    error_label = ttk.Label(result_frame, text=f"Error: {str(e)}", foreground="red")
                    error_label.pack(pady=20)
            
            # Add column selector
            ttk.Label(transform_controls, text="Column:").pack(side=tk.LEFT, padx=10)
            column_var = tk.StringVar()
            column_combo = ttk.Combobox(transform_controls, textvariable=column_var, values=numeric_cols)
            column_combo.pack(side=tk.LEFT, padx=5)
            if numeric_cols:
                column_var.set(numeric_cols[0])
            
            # Add apply button
            apply_button = ttk.Button(transform_controls, text="Apply Transformation", command=apply_transformation)
            apply_button.pack(side=tk.LEFT, padx=20)
            
            # Initially apply transformation
            if numeric_cols:
                apply_transformation()
            
        except Exception as e:
            logging.exception("Error in data analysis")
            messagebox.showerror("Error", f"Analysis failed: {str(e)}")
            self.status_label.config(text=f"Error: {str(e)}")

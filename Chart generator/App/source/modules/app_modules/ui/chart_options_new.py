"""
Chart Options UI Component

This module provides UI components for chart options (excluding scaling and colors when needed)
in the Lab Chart Generator application.


Author: Speedy29bg
"""

import tkinter as tk
from tkinter import ttk
import logging

class ChartOptionsFrame:
    """Manages chart options UI components and interactions"""
    
    def __init__(self, parent_frame, app_instance, exclude_scaling_and_colors=False):
        """
        Initialize chart options UI components
        
        Args:
            parent_frame: Parent tkinter frame to place this component in
            app_instance: Reference to the main application instance
            exclude_scaling_and_colors: If True, exclude scaling and color options
        """
        self.parent = parent_frame
        self.app = app_instance
        self.exclude_scaling_and_colors = exclude_scaling_and_colors
        
        # Chart type and export options (always available)
        self.chart_type = tk.StringVar(value="line")
        self.export_format = tk.StringVar(value="xlsx")
        
        self.create_chart_options_ui()
    
    def create_chart_options_ui(self):
        """Create chart options UI components"""
        # Chart type and export options (always shown)
        chart_type_frame = ttk.LabelFrame(self.parent, text="Chart Type & Export")
        chart_type_frame.pack(fill=tk.X, pady=5)
        
        # Chart type selection
        ttk.Label(chart_type_frame, text="Chart Type:").pack(anchor=tk.W, padx=5, pady=(5, 0))
        chart_type_selection = ttk.Frame(chart_type_frame)
        chart_type_selection.pack(anchor=tk.W, padx=5)
        
        ttk.Radiobutton(chart_type_selection, text="Line", variable=self.chart_type, 
                       value="line", command=self.app.update_preview).pack(side=tk.LEFT)
        ttk.Radiobutton(chart_type_selection, text="Scatter", variable=self.chart_type, 
                       value="scatter", command=self.app.update_preview).pack(side=tk.LEFT, padx=(10, 0))
        
        # Export format selection
        ttk.Label(chart_type_frame, text="Export Format:").pack(anchor=tk.W, padx=5, pady=(10, 0))
        export_format_selection = ttk.Frame(chart_type_frame)
        export_format_selection.pack(anchor=tk.W, padx=5, pady=(0, 5))
        
        ttk.Radiobutton(export_format_selection, text="Excel", variable=self.export_format, 
                       value="xlsx").pack(side=tk.LEFT)
        ttk.Radiobutton(export_format_selection, text="PNG", variable=self.export_format, 
                       value="png").pack(side=tk.LEFT, padx=(10, 0))
        ttk.Radiobutton(export_format_selection, text="PDF", variable=self.export_format, 
                       value="pdf").pack(side=tk.LEFT, padx=(10, 0))
    
    def get_chart_settings(self):
        """Get all current chart settings
        
        Returns:
            dict: Dictionary containing all chart settings
        """
        settings = {
            'chart_type': self.chart_type.get(),
            'export_format': self.export_format.get()
        }
        
        return settings

    # Alias for backward compatibility with code expecting get_settings
    get_settings = get_chart_settings

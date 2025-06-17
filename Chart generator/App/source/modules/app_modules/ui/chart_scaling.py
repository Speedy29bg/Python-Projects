"""
Chart Scaling UI Component

This module provides UI components for chart scaling and color scheme options
that are positioned right under the axes selection in the Lab Chart Generator application.


Author: Speedy29bg
"""

import tkinter as tk
from tkinter import ttk
import logging

class ChartScalingFrame:
    """Manages chart scaling and color scheme UI components"""
    
    def __init__(self, parent_frame, app_instance):
        """
        Initialize chart scaling UI components
        
        Args:
            parent_frame: Parent tkinter frame to place this component in
            app_instance: Reference to the main application instance
        """
        self.parent = parent_frame
        self.app = app_instance
        
        # Chart scaling settings
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
        
        # Color scheme for charts
        self.color_schemes = ["default", "viridis", "plasma", "inferno", "magma", "cividis"]
        self.selected_color_scheme = tk.StringVar(value=self.color_schemes[0])
        
        self.create_scaling_ui()
    
    def create_scaling_ui(self):
        """Create chart scaling and color scheme UI components"""
        # Chart scaling options
        self.scaling_frame = ttk.LabelFrame(self.parent, text="Chart Scaling Options")
        self.scaling_frame.pack(fill=tk.X, pady=5)
        
        # Left and right sections for scaling options
        scale_left = ttk.Frame(self.scaling_frame)
        scale_right = ttk.Frame(self.scaling_frame)
        scale_left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        scale_right.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Scale options (left side)
        ttk.Checkbutton(scale_left, text="Auto Scale", variable=self.auto_scale, 
                       command=self.toggle_manual_scaling).pack(anchor=tk.W)
        ttk.Checkbutton(scale_left, text="Log Scale X-Axis", variable=self.log_scale_x,
                       command=self.app.update_preview).pack(anchor=tk.W)
        ttk.Checkbutton(scale_left, text="Log Scale Primary Y-Axis", variable=self.log_scale_y1,
                       command=self.app.update_preview).pack(anchor=tk.W)
        ttk.Checkbutton(scale_left, text="Log Scale Secondary Y-Axis", variable=self.log_scale_y2,
                       command=self.app.update_preview).pack(anchor=tk.W)
        ttk.Checkbutton(scale_left, text="Normalize Data (0-1)", variable=self.normalize_data,
                       command=self.app.update_preview).pack(anchor=tk.W)
        
        # Custom range inputs (right side)
        range_frame = ttk.Frame(scale_right)
        range_frame.pack(fill=tk.X)
        
        # X-Axis range
        ttk.Label(range_frame, text="X-Axis Range:").grid(row=0, column=0, sticky=tk.W, pady=2)
        ttk.Label(range_frame, text="Min:").grid(row=0, column=1, sticky=tk.E, padx=5, pady=2)
        self.x_min_entry = ttk.Entry(range_frame, textvariable=self.x_min, width=8, state='disabled')
        self.x_min_entry.grid(row=0, column=2, pady=2)
        ttk.Label(range_frame, text="Max:").grid(row=0, column=3, sticky=tk.E, padx=5, pady=2)
        self.x_max_entry = ttk.Entry(range_frame, textvariable=self.x_max, width=8, state='disabled')
        self.x_max_entry.grid(row=0, column=4, pady=2)
        
        # Primary Y-Axis range
        ttk.Label(range_frame, text="Primary Y-Axis:").grid(row=1, column=0, sticky=tk.W, pady=2)
        ttk.Label(range_frame, text="Min:").grid(row=1, column=1, sticky=tk.E, padx=5, pady=2)
        self.y1_min_entry = ttk.Entry(range_frame, textvariable=self.y1_min, width=8, state='disabled')
        self.y1_min_entry.grid(row=1, column=2, pady=2)
        ttk.Label(range_frame, text="Max:").grid(row=1, column=3, sticky=tk.E, padx=5, pady=2)
        self.y1_max_entry = ttk.Entry(range_frame, textvariable=self.y1_max, width=8, state='disabled')
        self.y1_max_entry.grid(row=1, column=4, pady=2)
        
        # Secondary Y-Axis range
        ttk.Label(range_frame, text="Secondary Y-Axis:").grid(row=2, column=0, sticky=tk.W, pady=2)
        ttk.Label(range_frame, text="Min:").grid(row=2, column=1, sticky=tk.E, padx=5, pady=2)
        self.y2_min_entry = ttk.Entry(range_frame, textvariable=self.y2_min, width=8, state='disabled')
        self.y2_min_entry.grid(row=2, column=2, pady=2)
        ttk.Label(range_frame, text="Max:").grid(row=2, column=3, sticky=tk.E, padx=5, pady=2)
        self.y2_max_entry = ttk.Entry(range_frame, textvariable=self.y2_max, width=8, state='disabled')
        self.y2_max_entry.grid(row=2, column=4, pady=2)
        
        # Store references to the entry widgets for enabling/disabling
        self.range_entries = [
            self.x_min_entry, self.x_max_entry, 
            self.y1_min_entry, self.y1_max_entry, 
            self.y2_min_entry, self.y2_max_entry
        ]
        
        # Color scheme selection
        color_scheme_frame = ttk.LabelFrame(self.parent, text="Color Scheme")
        color_scheme_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(color_scheme_frame, text="Select Color Scheme:").pack(side=tk.LEFT, padx=5, pady=5)
        color_scheme_menu = ttk.OptionMenu(color_scheme_frame, self.selected_color_scheme, 
                                          self.selected_color_scheme.get(), *self.color_schemes,
                                          command=lambda x: self.app.update_preview())
        color_scheme_menu.pack(side=tk.LEFT, padx=5, pady=5)
    
    def toggle_manual_scaling(self):
        """Enable or disable manual scaling inputs"""
        state = 'disabled' if self.auto_scale.get() else 'normal'
        
        # Update state for all range entry widgets
        for entry in self.range_entries:
            entry.configure(state=state)
        
        self.app.update_preview()
        
    def get_scaling_settings(self):
        """Get all current scaling and color settings
        
        Returns:
            dict: Dictionary containing all scaling and color settings
        """
        return {
            'auto_scale': self.auto_scale.get(),
            'log_scale_x': self.log_scale_x.get(),
            'log_scale_y1': self.log_scale_y1.get(),
            'log_scale_y2': self.log_scale_y2.get(),
            'normalize_data': self.normalize_data.get(),
            'color_scheme': self.selected_color_scheme.get(),
            'x_min': self.x_min.get(),
            'x_max': self.x_max.get(),
            'y1_min': self.y1_min.get(),
            'y1_max': self.y1_max.get(),
            'y2_min': self.y2_min.get(),
            'y2_max': self.y2_max.get()
        }

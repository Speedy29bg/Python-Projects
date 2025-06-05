"""
Canvas Generation Module

This module provides functions for creating interactive matplotlib canvases in Tkinter.


Author: Speedy29bg
"""

import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.pyplot as plt

def create_tkinter_canvas(figure, frame):
    """Create a Tkinter canvas from a matplotlib figure with interactive features
    
    Args:
        figure: The matplotlib figure object
        frame: The Tkinter frame to place the canvas in
        
    Returns:
        FigureCanvasTkAgg: The Tkinter canvas widget
    """
    # Clear frame first to avoid stacking multiple charts
    for widget in frame.winfo_children():
        widget.destroy()
    
    # Create main frame for the chart and controls
    chart_frame = ttk.Frame(frame)
    chart_frame.pack(fill='both', expand=True)
    
    # Create chart area
    canvas = FigureCanvasTkAgg(figure, master=chart_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill='both', expand=True)
    
    # Add matplotlib's built-in navigation toolbar for zoom, pan, etc.
    toolbar_frame = ttk.Frame(chart_frame)
    toolbar_frame.pack(fill='x', pady=2)
    toolbar = NavigationToolbar2Tk(canvas, toolbar_frame)
    toolbar.update()
    
    # Create frame for custom buttons
    button_frame = ttk.Frame(chart_frame)
    button_frame.pack(fill='x', pady=5)
    
    # Grid toggle button
    grid_var = tk.BooleanVar(value=True)  # Default grid on
    
    def toggle_grid():
        for ax in figure.get_axes():
            ax.grid(grid_var.get())
        canvas.draw()
    
    grid_btn = ttk.Checkbutton(button_frame, text="Grid Lines", variable=grid_var, 
                             command=toggle_grid)
    grid_btn.pack(side='left', padx=5)
    
    # Toggle data points
    points_var = tk.BooleanVar(value=True)  # Default points visible
    
    def toggle_points():
        for ax in figure.get_axes():
            for line in ax.get_lines():
                line.set_marker('.' if points_var.get() else '')
        canvas.draw()
    
    points_btn = ttk.Checkbutton(button_frame, text="Show Data Points", variable=points_var, 
                               command=toggle_points)
    points_btn.pack(side='left', padx=5)
    
    # Toggle legend
    legend_var = tk.BooleanVar(value=True)  # Default legend visible
    
    def toggle_legend():
        for ax in figure.get_axes():
            legend = ax.get_legend()
            if legend:
                legend.set_visible(legend_var.get())
        canvas.draw()
    
    legend_btn = ttk.Checkbutton(button_frame, text="Show Legend", variable=legend_var, 
                               command=toggle_legend)
    legend_btn.pack(side='left', padx=5)
    
    # Toggle automatic updates
    autoupdate_var = tk.BooleanVar(value=True)
    autoupdate_btn = ttk.Checkbutton(button_frame, text="Auto-update", variable=autoupdate_var)
    autoupdate_btn.pack(side='left', padx=5)
    
    # Get autoupdate status
    canvas.autoupdate = lambda: autoupdate_var.get()
    
    # Set a reasonable height for the frame
    frame.config(height=450)  # Increased height to accommodate buttons
    
    return canvas

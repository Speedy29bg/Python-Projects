#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Interactive Chart Features Demo

This script demonstrates the enhanced interactive features available in the Chart Generator.
Run this script to see all the interactive functionality in action.

Author: Speedy29bg
Date: June 17, 2025
"""

import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from modules.chart_generator import create_tkinter_canvas, create_preview_plot

def create_demo_data():
    """Create sample data for demonstration"""
    # Generate sample time series data
    time = np.linspace(0, 10, 100)
    
    # Create multiple data series
    data = {
        'Time': time,
        'Signal_A': np.sin(time) + 0.1 * np.random.normal(size=len(time)),
        'Signal_B': np.cos(time * 1.5) + 0.15 * np.random.normal(size=len(time)),
        'Signal_C': np.sin(time * 0.5) * np.exp(-time * 0.1) + 0.1 * np.random.normal(size=len(time)),
        'Trend': time * 0.2 + 0.1 * np.random.normal(size=len(time))
    }
    
    return pd.DataFrame(data)

def main():
    """Main demo function"""
    # Create the main window
    root = tk.Tk()
    root.title("Interactive Chart Features Demo")
    root.geometry("1200x800")
    
    # Create main frame
    main_frame = ttk.Frame(root)
    main_frame.pack(fill='both', expand=True, padx=10, pady=10)
    
    # Create info label
    info_label = ttk.Label(main_frame, 
                          text="Interactive Chart Features Demo - Explore all the interactive controls!",
                          font=('Arial', 12, 'bold'))
    info_label.pack(pady=(0, 10))
    
    # Create frame for the chart
    chart_frame = ttk.Frame(main_frame)
    chart_frame.pack(fill='both', expand=True)
    
    # Generate demo data
    df = create_demo_data()
    
    # Chart settings for demo
    chart_settings = {
        'chart_type': 'line',
        'color_scheme': 'viridis',
        'auto_scale': True,
        'log_scale_x': False,
        'log_scale_y1': False,
        'log_scale_y2': False,
        'normalize_data': False,
        'export_format': 'png'
    }
    
    # Create the interactive chart
    figure, chart_info = create_preview_plot(
        df,
        'Time',  # x-axis
        ['Signal_A', 'Signal_B'],  # primary y-axes
        ['Signal_C', 'Trend'],  # secondary y-axes
        chart_settings
    )
    
    if figure:
        # Create the interactive canvas with all features
        canvas = create_tkinter_canvas(figure, chart_frame)
        
        # Add instructions
        instructions = ttk.Label(main_frame, 
                               text="Try these interactive features:\n"
                                   "• Use the toolbar to zoom, pan, and navigate\n"
                                   "• Toggle grid, points, legend, and other visual elements\n"
                                   "• Enable Data Cursor to hover over points for values\n"
                                   "• Use Crosshair for precise coordinate reading\n"
                                   "• Adjust line width and transparency with sliders\n"
                                   "• Click anywhere on the chart to see coordinates\n"
                                   "• Show statistics to see data summary",
                               justify='left',
                               font=('Arial', 10))
        instructions.pack(pady=10)
    else:
        error_label = ttk.Label(chart_frame, text="Error creating chart", foreground='red')
        error_label.pack(expand=True)
    
    # Start the demo
    root.mainloop()

if __name__ == "__main__":
    main()

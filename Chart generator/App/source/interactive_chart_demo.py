#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Interactive Chart Demo

This script demonstrates the enhanced interactive features of the chart preview.
"""

import tkinter as tk
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from modules.chart_generator import create_tkinter_canvas

def create_demo_chart():
    """Create a demo chart to showcase interactive features"""
    # Generate sample data
    x = np.linspace(0, 10, 100)
    y1 = np.sin(x) + 0.1 * np.random.randn(100)
    y2 = np.cos(x) + 0.1 * np.random.randn(100)
    y3 = np.sin(2*x) * 0.5 + 0.05 * np.random.randn(100)
    
    # Create figure
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Plot lines
    ax.plot(x, y1, label='Sin Wave', linewidth=2, marker='o', markersize=3)
    ax.plot(x, y2, label='Cos Wave', linewidth=2, marker='s', markersize=3)
    ax.plot(x, y3, label='Double Frequency', linewidth=2, marker='^', markersize=3)
    
    # Customize the plot
    ax.set_xlabel('X Values')
    ax.set_ylabel('Y Values')
    ax.set_title('Interactive Chart Demo - Try the Controls Below!')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    return fig

def main():
    """Main function to run the interactive chart demo"""
    # Create main window
    root = tk.Tk()
    root.title("Interactive Chart Features Demo")
    root.geometry("1200x800")
    
    # Create info label
    info_label = tk.Label(root, 
                         text="Interactive Chart Features:\n" +
                              "• Navigation Toolbar: Zoom, Pan, Home, Back/Forward\n" +
                              "• Grid Lines: Toggle grid visibility\n" +
                              "• Show Data Points: Toggle data point markers\n" +
                              "• Show Legend: Toggle legend visibility\n" +
                              "• Data Cursor: Hover over points to see values (if mplcursors is installed)\n" +
                              "• Crosshair: Shows crosshair lines following mouse\n" +
                              "• Line Width: Adjust line thickness\n" +
                              "• Transparency: Adjust line transparency\n" +
                              "• Reset Zoom: Return to original view\n" +
                              "• Show Statistics: Display data statistics\n" +
                              "• Coordinate Display: Click anywhere to see coordinates",
                         justify=tk.LEFT, bg="lightblue", pady=10)
    info_label.pack(fill=tk.X, padx=10, pady=5)
    
    # Create frame for the chart
    chart_frame = tk.Frame(root)
    chart_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
    
    # Create and display the interactive chart
    fig = create_demo_chart()
    canvas = create_tkinter_canvas(fig, chart_frame)
    
    # Add a close button
    close_button = tk.Button(root, text="Close Demo", command=root.quit, 
                           bg="red", fg="white", font=("Arial", 12, "bold"))
    close_button.pack(pady=10)
    
    print("Interactive Chart Demo Started!")
    print("Features to try:")
    print("1. Use the navigation toolbar to zoom and pan")
    print("2. Toggle various visual elements with the checkboxes")
    print("3. Adjust line width and transparency with sliders")
    print("4. Click on the chart to see coordinates")
    print("5. Enable crosshair to see cursor position")
    print("6. Try the data cursor for detailed point information")
    
    # Start the GUI
    root.mainloop()

if __name__ == "__main__":
    main()

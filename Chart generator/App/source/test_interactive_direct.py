#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test if interactive features are properly loaded in the main app
"""

import tkinter as tk
import matplotlib.pyplot as plt
import numpy as np

def test_interactive_features():
    """Test the interactive chart creation directly"""
    
    # Import the interactive function
    try:
        from modules.chart_generator import create_tkinter_canvas
        print("✓ Successfully imported create_tkinter_canvas")
    except ImportError as e:
        print(f"✗ Failed to import create_tkinter_canvas: {e}")
        return
    
    # Create a simple test figure
    fig, ax = plt.subplots(figsize=(10, 6))
    x = np.linspace(0, 10, 100)
    y1 = np.sin(x)
    y2 = np.cos(x)
    
    ax.plot(x, y1, label='sin(x)', linewidth=2)
    ax.plot(x, y2, label='cos(x)', linewidth=2)
    ax.set_xlabel('X axis')
    ax.set_ylabel('Y axis')
    ax.set_title('Test Chart with Interactive Features')
    ax.legend()
    ax.grid(True)
    
    # Create tkinter window
    root = tk.Tk()
    root.title("Interactive Features Test")
    root.geometry("1200x800")
    
    # Create frame for the chart
    main_frame = tk.Frame(root)
    main_frame.pack(fill='both', expand=True, padx=10, pady=10)
    
    # Create the interactive canvas
    print("Creating interactive canvas...")
    try:
        canvas = create_tkinter_canvas(fig, main_frame)
        print("✓ Interactive canvas created successfully")
        print("✓ You should see:")
        print("  - Navigation toolbar (zoom, pan, save, etc.)")
        print("  - Toggle buttons (Grid, Points, Legend, Cursor, Crosshair)")
        print("  - Sliders (Line Width, Transparency)")
        print("  - Additional buttons (Reset Zoom, Statistics)")
        print("  - Coordinate display")
    except Exception as e:
        print(f"✗ Error creating interactive canvas: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # Instructions
    info_label = tk.Label(root, text="Test the interactive features above!", 
                         font=('Arial', 12, 'bold'), fg='blue')
    info_label.pack(pady=5)
    
    root.mainloop()

if __name__ == "__main__":
    test_interactive_features()

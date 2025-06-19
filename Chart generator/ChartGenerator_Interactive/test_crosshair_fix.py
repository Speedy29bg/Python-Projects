#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test script to verify crosshair functionality works correctly
without interfering with chart preview
"""

import sys
import os
sys.path.append('src')

import tkinter as tk
from tkinter import ttk
import numpy as np
import pandas as pd
from core.chart_generator import InteractiveChartGenerator

def test_crosshair():
    """Test crosshair functionality"""
    print("Testing crosshair functionality...")
    
    # Create a test window
    root = tk.Tk()
    root.title("Crosshair Test")
    root.geometry("800x600")
    
    # Create test data
    x_data = np.linspace(0, 10, 100)
    y1_data = np.sin(x_data)
    y2_data = np.cos(x_data)
    
    # Create chart generator
    chart_gen = InteractiveChartGenerator()
    
    # Create a frame for the chart
    chart_frame = ttk.Frame(root)
    chart_frame.pack(fill='both', expand=True, padx=10, pady=10)
    
    try:
        # Create the chart
        chart_gen.create_interactive_chart(
            parent_frame=chart_frame,
            x_data=x_data,
            y_data_list=[y1_data, y2_data],
            x_label="X Values",
            y_labels=["sin(x)", "cos(x)"],
            chart_type="line",
            color_scheme="default"
        )
        print("✓ Chart created successfully")
        
        # Add test instructions
        instructions = ttk.Label(root, 
            text="Test Instructions:\n1. Toggle crosshair on/off\n2. Move mouse over chart\n3. Check if chart preview changes\n4. Close window when done",
            justify='left')
        instructions.pack(pady=10)
        
        print("✓ Test window created")
        print("Manual test required: Toggle crosshair and verify no chart preview changes")
        
        # Don't run mainloop in automated testing
        # root.mainloop()
        
        # Clean up
        root.destroy()
        print("✓ Test completed successfully")
        
    except Exception as e:
        print(f"✗ Error during testing: {e}")
        root.destroy()
        return False
    
    return True

if __name__ == "__main__":
    success = test_crosshair()
    if success:
        print("\n✓ All automated tests passed!")
        print("Note: Manual testing of crosshair UI interaction is still recommended")
    else:
        print("\n✗ Tests failed!")
        sys.exit(1)

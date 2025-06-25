#!/usr/bin/env python
"""
Test the actual Chart Generator app with sample data to see interactive features
"""

import sys
import os
import pandas as pd
import numpy as np

# Add the source directory to path
sys.path.insert(0, os.path.join(os.getcwd(), "Chart generator", "App", "source"))

def create_test_csv():
    """Create a test CSV file for testing"""
    # Generate sample data
    time = np.linspace(0, 10, 100)
    data = {
        'Time': time,
        'Temperature': 20 + 5 * np.sin(time) + np.random.normal(0, 0.5, len(time)),
        'Pressure': 1013 + 50 * np.cos(time * 0.8) + np.random.normal(0, 2, len(time)),
        'Humidity': 50 + 20 * np.sin(time * 1.2) + np.random.normal(0, 1, len(time)),
        'Flow_Rate': 2.5 + 0.5 * np.sin(time * 2) + np.random.normal(0, 0.1, len(time))
    }
    
    df = pd.DataFrame(data)
    csv_path = os.path.join("Chart generator", "App", "source", "test_data.csv")
    df.to_csv(csv_path, index=False)
    print(f"Created test data: {csv_path}")
    return csv_path

def test_app_with_data():
    """Test the actual app with sample data"""
    try:
        # Create test data
        csv_path = create_test_csv()
        
        # Import the main app
        from modules.app_modules.core.app_controller import LabChartGenerator
        import tkinter as tk
        
        print("Starting Chart Generator with test data...")
        
        # Create the app
        root = tk.Tk()
        root.title("Chart Generator - Testing Interactive Features")
        root.geometry("1400x900")  # Larger window to see everything
        
        app = LabChartGenerator(root)
        
        # Programmatically load the test data
        app.files = [csv_path]
        app.file_data_cache = {csv_path: pd.read_csv(csv_path)}
        
        # Populate the column headers
        df = app.file_data_cache[csv_path]
        app.column_headers = list(df.columns)
        app.axes_selection_frame.clear_listboxes()
        app.axes_selection_frame.populate_listboxes(app.column_headers)
        
        # Programmatically select some columns to trigger chart creation
        # Select Time as X-axis
        app.axes_selection_frame.x_listbox.selection_set(0)  # Time
        # Select Temperature and Pressure as Y-axes
        app.axes_selection_frame.y_listbox.selection_set(1)  # Temperature
        app.axes_selection_frame.y_listbox.selection_set(2)  # Pressure
        
        # Update the file selection label
        app.file_selection_frame.update_file_label(1)
        app.update_status("Test data loaded - Interactive features should appear in chart preview")
        
        # Trigger chart creation        app.update_preview()
        
        instructions = """App started! Check the chart preview area for interactive controls.
You should see:
- Navigation toolbar at the top of the chart
- Interactive control buttons below the chart
- Sliders for line width and transparency
- Coordinate display when you click"""
        print(instructions)
        
        # Add a label with instructions
        instruction_text = "Interactive Features Test - Look for controls below the chart!"
        instruction_label = tk.Label(root, text=instruction_text, 
                                   font=('Arial', 14, 'bold'), fg='red')
        instruction_label.pack(side='top', pady=5)
        
        root.mainloop()
        
    except Exception as e:
        print(f"Error testing app: {e}")
        import traceback
        traceback.print_exc()
        input("Press Enter to continue...")

if __name__ == "__main__":
    print("Testing Chart Generator with automatic data loading...")
    test_app_with_data()

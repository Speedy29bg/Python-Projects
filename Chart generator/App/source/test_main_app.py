#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test script to verify the main application with interactive features
"""

import tkinter as tk
import sys
import os

# Add modules directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'modules'))

from modules.logger import setup_logging, handle_exception
from modules.app_modules.core.app_controller import AppController

def main():
    """Main function to test the Chart Generator application"""
    
    # Initialize the main application window
    root = tk.Tk()
    root.title("Lab Chart Generator - Test")
    root.geometry("1200x800")  # Set a good size for testing
    
    # Setup logging
    logger = setup_logging()
    logger.info("Starting Chart Generator test application")
    
    try:
        # Create the application instance
        app = AppController(root)
        
        # Set custom exception handler
        sys.excepthook = lambda exc_type, exc_value, exc_traceback: handle_exception(
            exc_type, exc_value, exc_traceback, app.status_label if hasattr(app, 'status_label') else None
        )
        
        # Print instructions
        print("\n" + "="*60)
        print("CHART GENERATOR TEST APPLICATION")
        print("="*60)
        print("Instructions:")
        print("1. Load a CSV file using the 'Load File' button")
        print("2. Select axes from the dropdown menus")
        print("3. The chart preview should update automatically")
        print("4. Interactive features should be visible in the preview:")
        print("   - Navigation toolbar (zoom, pan, save)")
        print("   - Toggle buttons (grid, points, legend, cursor, crosshair)")
        print("   - Sliders (line width, transparency)")
        print("   - Additional buttons (reset zoom, statistics)")
        print("5. Test the interactive features!")
        print("="*60)
        
        # Start the application
        root.mainloop()
        
    except Exception as e:
        logger.error(f"Error starting application: {e}")
        print(f"Error: {e}")
    finally:
        root.destroy()

if __name__ == "__main__":
    main()

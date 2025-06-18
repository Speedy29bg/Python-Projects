#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Debug version of the main Chart Generator to test interactive features
"""

import tkinter as tk
import sys
from modules.logger import setup_logging, handle_exception
from modules.core import AppController

def main():
    print("Starting Chart Generator (Debug Version)...")
    print("Testing interactive features...")
    
    # Initialize the main application window
    root = tk.Tk()
    root.title("Lab Chart Generator - DEBUG")
    root.geometry("1400x900")  # Larger window
    
    # Setup logging
    logger = setup_logging()
    logger.info("Starting debug version of Chart Generator")
    
    # Test import of interactive features
    try:
        from modules.chart_generator import create_tkinter_canvas
        print("✓ Successfully imported interactive chart function")
        
        # Check if the function has the expected signature
        import inspect
        sig = inspect.signature(create_tkinter_canvas)
        print(f"✓ Function signature: {sig}")
        
    except Exception as e:
        print(f"✗ Error importing interactive features: {e}")
        return
    
    try:
        # Create the application instance
        app = AppController(root)
        print("✓ Successfully created AppController")
        
        # Set custom exception handler
        sys.excepthook = lambda exc_type, exc_value, exc_traceback: handle_exception(
            exc_type, exc_value, exc_traceback, app.status_label if hasattr(app, 'status_label') else None
        )
        
        print("✓ Application ready - interactive features should be available")
        print("\nInstructions:")
        print("1. Load a CSV file")
        print("2. Select axes")
        print("3. Check if interactive controls appear in chart preview")
        print("4. Interactive features should include:")
        print("   - Navigation toolbar")
        print("   - Toggle buttons (Grid, Points, Legend, etc.)")
        print("   - Sliders (Line Width, Transparency)")
        print("   - Additional controls (Reset Zoom, Statistics)")
        
        # Start the application
        root.mainloop()
        
    except Exception as e:
        logger.error(f"Error starting application: {e}")
        print(f"✗ Error: {e}")
    finally:
        root.destroy()

if __name__ == "__main__":
    main()

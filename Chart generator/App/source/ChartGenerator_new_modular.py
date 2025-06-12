#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Laboratory Chart Generator Application

Main entry point for the Chart Generator application that allows users to create,
customize, and export charts from CSV data files. The application provides a GUI
with various options for chart styling, scaling, and export.

This version has been refactored for better modularity and maintainability.


Author: Speedy29bg
Version: 1.2
Date: June 5, 2025
"""

import tkinter as tk
import sys
from modules.logger import setup_logging, handle_exception
from modules.core import AppController
from modules.cleanup import register_cleanup_on_exit

if __name__ == "__main__":
    # Setup logging first
    logger = setup_logging()
    
    # Register cleanup to run when program exits
    register_cleanup_on_exit()
    
    # Initialize the main application window
    root = tk.Tk()
    root.title("Lab Chart Generator")
    
    # Create the application instance
    app = AppController(root)
    
    # Set custom exception handler
    sys.excepthook = lambda exc_type, exc_value, exc_traceback: handle_exception(
        exc_type, exc_value, exc_traceback, app.status_label if hasattr(app, 'status_label') else None
    )
    
    try:
        # Start the application
        root.mainloop()
    finally:
        # Ensure cleanup runs even if there's an error
        root.destroy()


#TODO focus on generating PNG
#TODO if i select more than one file, it should generate a chart for each file
#TODO implement the logic for mode visualization
#TODO check why date time is not working properly while there is an empty row
#TODO make option to rename X and Y on the chart
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

if __name__ == "__main__":
    # Initialize the main application window
    root = tk.Tk()
    root.title("Lab Chart Generator")
    root.geometry("1400x900")  # Larger window to accommodate interactive features
    
    # Setup logging
    logger = setup_logging()
    logger.info("Starting Chart Generator with Interactive Features")
    
    # Create the application instance
    app = AppController(root)
    
    # Set custom exception handler
    sys.excepthook = lambda exc_type, exc_value, exc_traceback: handle_exception(
        exc_type, exc_value, exc_traceback, app.status_label if hasattr(app, 'status_label') else None
    )
    
    # Log that interactive features are enabled
    logger.info("Chart Generator started with interactive preview features")
    
    # Start the application
    root.mainloop()
    root.destroy()


#TODO focus on generating PNG
#TODO if i select more than one file, it should generate a chart for each file
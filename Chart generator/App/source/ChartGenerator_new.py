#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Laboratory Chart Generator Application

Main entry point for the Chart Generator application that allows users to create,
customize, and export charts from CSV data files. The application provides a GUI
with various options for chart styling, scaling, and export.

Author: Lab Chart Tools Team
Version: 1.0
Date: May 30, 2025
"""

import tkinter as tk
import sys
from modules.logger import setup_logging, handle_exception
from modules.app import LabChartGenerator

if __name__ == "__main__":
    # Initialize the main application window
    root = tk.Tk()
    root.title("Lab Chart Generator")
    
    # Setup logging
    logger = setup_logging()
    
    # Create the application instance
    app = LabChartGenerator(root)
    
    # Set custom exception handler
    sys.excepthook = lambda exc_type, exc_value, exc_traceback: handle_exception(
        exc_type, exc_value, exc_traceback, app.status_label if hasattr(app, 'status_label') else None
    )
    
    # Start the application
    root.mainloop()
    root.destroy()

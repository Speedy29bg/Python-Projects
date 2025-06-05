"""
Exception Handler Module

This module provides exception handling functionality for the Chart Generator application.

Author: Lab Chart Tools Team
"""

import logging
import traceback

def handle_exception(exc_type, exc_value, exc_traceback, status_label=None):
    """Handle uncaught exceptions
    
    Args:
        exc_type: The type of exception
        exc_value: The exception instance
        exc_traceback: The traceback object
        status_label: Optional tkinter label to update with error message
    """
    # Log the error with full traceback
    logging.error("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))
    
    # Format a user-friendly error message
    error_msg = f"An unexpected error occurred:\n{exc_value}"
    
    # Show error dialog if tkinter is still functioning
    try:
        import tkinter.messagebox as messagebox
        messagebox.showerror("Application Error", error_msg)
    except:
        # If tkinter is not working, print to console
        print(error_msg)
    
    # Update status label if possible
    if status_label:
        try:
            status_label.config(text=f"Error: {str(exc_value)}")
        except:
            pass

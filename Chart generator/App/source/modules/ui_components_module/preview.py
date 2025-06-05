"""
Data Preview Module

This module provides functions for creating data preview windows.

Author: Lab Chart Tools Team
"""

import tkinter as tk
from tkinter import ttk
import pandas as pd

def create_data_preview(parent, df, title="Data Preview"):
    """Create a window showing a preview of DataFrame contents
    
    Args:
        parent: The parent tkinter window or frame
        df: The pandas DataFrame to display
        title: The title of the preview window
        
    Returns:
        tk.Toplevel: The created preview window
    """
    preview_window = tk.Toplevel(parent)
    preview_window.title(title)
    preview_window.geometry("800x600")
    
    # Create a Text widget to display the data
    text_widget = tk.Text(preview_window, wrap="none")
    
    # Add scrollbars
    y_scrollbar = ttk.Scrollbar(preview_window, orient="vertical", command=text_widget.yview)
    x_scrollbar = ttk.Scrollbar(preview_window, orient="horizontal", command=text_widget.xview)
    text_widget.configure(yscrollcommand=y_scrollbar.set, xscrollcommand=x_scrollbar.set)
    
    # Layout
    text_widget.grid(row=0, column=0, sticky="nsew")
    y_scrollbar.grid(row=0, column=1, sticky="ns")
    x_scrollbar.grid(row=1, column=0, sticky="ew")
    
    # Configure grid weights
    preview_window.grid_rowconfigure(0, weight=1)
    preview_window.grid_columnconfigure(0, weight=1)
    
    # Format DataFrame as string with fixed-width columns
    # Limit to first 100 rows for performance
    preview_text = df.head(100).to_string(index=True)
    text_widget.insert(tk.END, preview_text)
    
    # Make the text widget read-only
    text_widget.configure(state="disabled")
    
    return preview_window

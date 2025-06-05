"""
Loading Indicator Module

This module provides functions for creating loading indicators in the UI.


Author: Speedy29bg
"""

import tkinter as tk
from tkinter import ttk

def create_loading_indicator(parent, message="Loading..."):
    """Create a loading indicator with a progressbar
    
    Args:
        parent: The parent tkinter window or frame
        message: The message to display
        
    Returns:
        tuple: (frame, label, progressbar) - The created UI elements
    """
    frame = ttk.Frame(parent)
    frame.place(relx=0.5, rely=0.5, anchor='center')
    
    label = ttk.Label(frame, text=message, font=('Helvetica', 12, 'bold'))
    label.pack(pady=10)
    
    progress = ttk.Progressbar(frame, orient="horizontal", length=300, mode="indeterminate")
    progress.pack(pady=10)
    progress.start(10)
    
    return frame, label, progress

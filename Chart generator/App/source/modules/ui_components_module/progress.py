"""
Progress Dialog Module

This module provides functions for creating progress dialogs in the UI.

Author: Lab Chart Tools Team
"""

import tkinter as tk
from tkinter import ttk

def create_progress_dialog(parent, title="Processing", max_value=100):
    """Create a progress dialog with a determinate progress bar
    
    Args:
        parent: The parent tkinter window or frame
        title: The title of the progress dialog window
        max_value: The maximum value for the progress bar
        
    Returns:
        tuple: (dialog, label, progressbar, status_label) - The created UI elements
    """
    dialog = tk.Toplevel(parent)
    dialog.title(title)
    dialog.geometry("400x150")
    dialog.transient(parent)
    dialog.grab_set()
    
    label = ttk.Label(dialog, text=title, font=('Helvetica', 10))
    label.pack(pady=10)
    
    progress_bar = ttk.Progressbar(dialog, orient="horizontal", length=300, mode="determinate", maximum=max_value)
    progress_bar.pack(pady=10)
    
    status_label = ttk.Label(dialog, text="")
    status_label.pack(pady=5)
    
    # Center the dialog on parent
    dialog.update_idletasks()
    parent_x = parent.winfo_rootx()
    parent_y = parent.winfo_rooty()
    parent_width = parent.winfo_width()
    parent_height = parent.winfo_height()
    
    dialog_width = dialog.winfo_width()
    dialog_height = dialog.winfo_height()
    
    x = parent_x + (parent_width - dialog_width) // 2
    y = parent_y + (parent_height - dialog_height) // 2
    
    dialog.geometry(f"+{x}+{y}")
    
    return dialog, label, progress_bar, status_label

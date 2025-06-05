"""
User interface component utilities for the Lab Chart Generator

This module contains functions for creating and managing UI components
that are used across the application, such as progress dialogs, loading indicators,
and file previews.

Author: Lab Chart Tools Team
"""

import tkinter as tk
from tkinter import ttk
import pandas as pd
import logging
from typing import Optional, Dict, Any, Callable

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

def populate_listbox(listbox, items, selection_indices=None):
    """Populate a listbox with items and optionally set selections
    
    Args:
        listbox: The tkinter Listbox to populate
        items: List of items to add to the listbox
        selection_indices: Optional list of indices to select
    """
    # Clear existing content
    listbox.delete(0, tk.END)
    
    # Add new items
    for item in items:
        listbox.insert(tk.END, item)
    
    # Set selections if provided
    if selection_indices:
        for idx in selection_indices:
            if 0 <= idx < len(items):
                listbox.selection_set(idx)

def get_listbox_selections(listbox):
    """Get selected items from a listbox
    
    Args:
        listbox: The tkinter Listbox to get selections from
        
    Returns:
        list: Selected items
    """
    selected_indices = listbox.curselection()
    items = [listbox.get(i) for i in selected_indices]
    return items

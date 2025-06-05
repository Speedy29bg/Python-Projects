"""
Listbox Utilities Module

This module provides functions for working with tkinter Listbox widgets.


Author: Speedy29bg
"""

import tkinter as tk
from typing import List, Optional

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

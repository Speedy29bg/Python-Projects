#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Excel-style Data Table with AutoFilter

Provides an Excel-like data table with column header dropdown filters,
checkboxes for value selection, and sorting - exactly like Excel AutoFilter.
"""

import tkinter as tk
from tkinter import ttk
import pandas as pd
from typing import Dict, List, Any, Optional, Callable
import numpy as np
from utils.logger import get_logger

logger = get_logger()

class ExcelFilterDialog:
    """Excel-style filter dialog for a column"""
    
    def __init__(self, parent, column_name: str, unique_values: List, current_filter: List, callback: Callable):
        """
        Initialize Excel-style filter dialog
        
        Args:
            parent: Parent widget
            column_name: Name of the column being filtered
            unique_values: List of unique values in the column
            current_filter: Currently selected values (empty = all selected)
            callback: Function to call when filter is applied
        """
        self.parent = parent
        self.column_name = column_name
        self.unique_values = sorted(unique_values) if unique_values else []
        self.current_filter = current_filter or []
        self.callback = callback
        self.dialog = None
        self.value_vars = {}
        self.select_all_var = tk.BooleanVar()
        
        self.create_dialog()
    
    def create_dialog(self):
        """Create the Excel-style filter dialog"""
        self.dialog = tk.Toplevel(self.parent)
        self.dialog.title(f"AutoFilter - {self.column_name}")
        self.dialog.geometry("300x400")
        self.dialog.resizable(False, True)
        self.dialog.grab_set()  # Make dialog modal
        
        # Main frame
        main_frame = ttk.Frame(self.dialog, padding=10)
        main_frame.pack(fill='both', expand=True)
        
        # Sort options
        sort_frame = ttk.LabelFrame(main_frame, text="Sort", padding=5)
        sort_frame.pack(fill='x', pady=(0, 10))
        
        ttk.Button(sort_frame, text="Sort A to Z", 
                  command=lambda: self.apply_sort(True)).pack(side='left', padx=5)
        ttk.Button(sort_frame, text="Sort Z to A", 
                  command=lambda: self.apply_sort(False)).pack(side='left', padx=5)
        
        # Filter options
        filter_frame = ttk.LabelFrame(main_frame, text="Filter", padding=5)
        filter_frame.pack(fill='both', expand=True)
        
        # Select All checkbox
        select_all_frame = ttk.Frame(filter_frame)
        select_all_frame.pack(fill='x', pady=(0, 5))
        
        ttk.Checkbutton(select_all_frame, text="Select All", 
                       variable=self.select_all_var,
                       command=self.toggle_select_all).pack(side='left')
        
        # Search box
        search_frame = ttk.Frame(filter_frame)
        search_frame.pack(fill='x', pady=(0, 5))
        
        ttk.Label(search_frame, text="Search:").pack(side='left')
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=20)
        search_entry.pack(side='left', padx=(5, 0), fill='x', expand=True)
        self.search_var.trace('w', self.on_search_changed)
        
        # Scrollable frame for checkboxes
        canvas = tk.Canvas(filter_frame, height=250)
        scrollbar = ttk.Scrollbar(filter_frame, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Create checkboxes for each unique value
        self.create_value_checkboxes()
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill='x', pady=(10, 0))
        
        ttk.Button(button_frame, text="OK", 
                  command=self.apply_filter).pack(side='right', padx=(5, 0))
        ttk.Button(button_frame, text="Cancel", 
                  command=self.dialog.destroy).pack(side='right')
        ttk.Button(button_frame, text="Clear Filter", 
                  command=self.clear_filter).pack(side='left')
        
        # Set initial state
        self.update_select_all_state()
    
    def create_value_checkboxes(self):
        """Create checkboxes for each unique value"""
        # Clear existing checkboxes
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        self.value_vars.clear()
        
        # Get filtered values based on search
        search_text = self.search_var.get().lower() if hasattr(self, 'search_var') else ""
        filtered_values = []
        
        for value in self.unique_values:
            str_value = str(value)
            if search_text == "" or search_text in str_value.lower():
                filtered_values.append(value)
        
        # Create checkbox for each value
        for value in filtered_values:
            var = tk.BooleanVar()
            # Set initial state - if no current filter, all are selected
            if not self.current_filter:
                var.set(True)
            else:
                var.set(value in self.current_filter)
            
            self.value_vars[value] = var
            
            # Create checkbox with value
            cb_frame = ttk.Frame(self.scrollable_frame)
            cb_frame.pack(fill='x', padx=2, pady=1)
            
            ttk.Checkbutton(cb_frame, text=str(value)[:50], variable=var,
                           command=self.update_select_all_state).pack(side='left')
    
    def on_search_changed(self, *args):
        """Handle search text changes"""
        self.create_value_checkboxes()
        self.update_select_all_state()
    
    def toggle_select_all(self):
        """Toggle all checkboxes"""
        select_all = self.select_all_var.get()
        for var in self.value_vars.values():
            var.set(select_all)
    
    def update_select_all_state(self):
        """Update the Select All checkbox state"""
        if not self.value_vars:
            self.select_all_var.set(False)
            return
        
        selected_count = sum(var.get() for var in self.value_vars.values())
        total_count = len(self.value_vars)
        
        if selected_count == total_count:
            self.select_all_var.set(True)
        elif selected_count == 0:
            self.select_all_var.set(False)
        else:
            # Partial selection - in Excel this would be a dash, but we'll use False
            self.select_all_var.set(False)
    
    def apply_filter(self):
        """Apply the selected filter"""
        selected_values = [value for value, var in self.value_vars.items() if var.get()]
        self.callback(self.column_name, 'filter', selected_values)
        self.dialog.destroy()
    
    def apply_sort(self, ascending: bool):
        """Apply sorting"""
        self.callback(self.column_name, 'sort', ascending)
        self.dialog.destroy()
    
    def clear_filter(self):
        """Clear the filter for this column"""
        self.callback(self.column_name, 'clear', None)
        self.dialog.destroy()


class ExcelDataTable:
    """Excel-style data table with AutoFilter capabilities"""
    
    def __init__(self, parent, data_processor, on_data_changed: Callable):
        """
        Initialize Excel-style data table
        
        Args:
            parent: Parent widget
            data_processor: DataProcessor instance
            on_data_changed: Callback when data changes
        """
        self.parent = parent
        self.data_processor = data_processor
        self.on_data_changed = on_data_changed
        self.filters = {}  # column -> selected_values
        self.sort_column = None
        self.sort_ascending = True
        
        self.create_ui()
    
    def create_ui(self):
        """Create the Excel-style table UI"""
        # Main frame
        self.frame = ttk.LabelFrame(self.parent, text="Data Table (Excel-style AutoFilter)", padding=5)
        
        # Toolbar
        toolbar = ttk.Frame(self.frame)
        toolbar.pack(fill='x', pady=(0, 5))
        
        ttk.Button(toolbar, text="Enable AutoFilter", 
                  command=self.toggle_autofilter).pack(side='left', padx=(0, 5))
        ttk.Button(toolbar, text="Clear All Filters", 
                  command=self.clear_all_filters).pack(side='left', padx=(0, 5))
        ttk.Button(toolbar, text="Refresh", 
                  command=self.refresh_data).pack(side='left', padx=(0, 5))
        
        # Info label
        self.info_label = ttk.Label(toolbar, text="No data loaded", foreground="gray")
        self.info_label.pack(side='right')
        
        # Table frame with scrollbars
        table_frame = ttk.Frame(self.frame)
        table_frame.pack(fill='both', expand=True)
        
        # Create Treeview for data display
        columns = []  # Will be set when data is loaded
        self.tree = ttk.Treeview(table_frame, columns=columns, show='tree headings', height=15)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        h_scrollbar = ttk.Scrollbar(table_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Pack scrollbars and tree
        self.tree.grid(row=0, column=0, sticky='nsew')
        v_scrollbar.grid(row=0, column=1, sticky='ns')
        h_scrollbar.grid(row=1, column=0, sticky='ew')
        
        # Configure grid weights
        table_frame.columnconfigure(0, weight=1)
        table_frame.rowconfigure(0, weight=1)
        
        self.autofilter_enabled = False
        self.refresh_data()
    
    def toggle_autofilter(self):
        """Toggle AutoFilter on/off"""
        self.autofilter_enabled = not self.autofilter_enabled
        self.refresh_data()
    
    def refresh_data(self):
        """Refresh the data table"""
        if self.data_processor.data is None:
            self.info_label.config(text="No data loaded")
            self.clear_tree()
            return
        
        # Apply current filters and sorting
        filtered_data = self.get_filtered_data()
        
        # Update tree
        self.update_tree(filtered_data)
        
        # Update info
        total_rows = len(self.data_processor.original_data) if self.data_processor.original_data is not None else 0
        filtered_rows = len(filtered_data)
        
        if self.filters:
            self.info_label.config(text=f"Showing {filtered_rows} of {total_rows} rows (filtered)", 
                                 foreground="blue")
        else:
            self.info_label.config(text=f"Showing {filtered_rows} rows", foreground="black")
    
    def get_filtered_data(self) -> pd.DataFrame:
        """Get filtered and sorted data"""
        if self.data_processor.original_data is None:
            return pd.DataFrame()
        
        data = self.data_processor.original_data.copy()
        
        # Apply filters
        for column, selected_values in self.filters.items():
            if column in data.columns and selected_values:
                data = data[data[column].isin(selected_values)]
        
        # Apply sorting
        if self.sort_column and self.sort_column in data.columns:
            data = data.sort_values(by=self.sort_column, ascending=self.sort_ascending, na_position='last')
        
        return data
    
    def update_tree(self, data: pd.DataFrame):
        """Update the treeview with data"""
        self.clear_tree()
        
        if data.empty:
            return
        
        # Configure columns
        columns = list(data.columns)
        self.tree.configure(columns=columns)
        
        # Configure column headings with filter arrows
        self.tree.heading('#0', text='#', anchor='w')
        self.tree.column('#0', width=50, minwidth=50)
        
        for col in columns:
            # Add filter arrow if autofilter is enabled
            display_text = col
            if self.autofilter_enabled:
                if col in self.filters and self.filters[col]:
                    display_text += " 🔽"  # Filtered
                else:
                    display_text += " ▼"   # Available for filtering
                
                if col == self.sort_column:
                    display_text += " ↑" if self.sort_ascending else " ↓"
            
            self.tree.heading(col, text=display_text, anchor='w')
            self.tree.column(col, width=120, minwidth=80)
            
            # Bind click event for filter dialog
            if self.autofilter_enabled:
                self.tree.heading(col, command=lambda c=col: self.show_filter_dialog(c))
        
        # Add data rows
        for idx, row in data.iterrows():
            values = [str(row[col]) if pd.notna(row[col]) else "" for col in columns]
            self.tree.insert('', 'end', text=str(idx), values=values)
    
    def clear_tree(self):
        """Clear all items from the tree"""
        for item in self.tree.get_children():
            self.tree.delete(item)
    
    def show_filter_dialog(self, column: str):
        """Show Excel-style filter dialog for a column"""
        if not self.autofilter_enabled or self.data_processor.original_data is None:
            return
        
        if column not in self.data_processor.original_data.columns:
            return
        
        # Get unique values for the column
        unique_values = self.data_processor.original_data[column].dropna().unique().tolist()
        
        # Get current filter for this column
        current_filter = self.filters.get(column, [])
        
        # Show filter dialog
        ExcelFilterDialog(
            self.parent,
            column,
            unique_values,
            current_filter,
            self.handle_filter_action
        )
    
    def handle_filter_action(self, column: str, action: str, value: Any):
        """Handle filter dialog actions"""
        if action == 'filter':
            if value:  # If specific values selected
                self.filters[column] = value
            else:  # If no values selected, show all
                if column in self.filters:
                    del self.filters[column]
        
        elif action == 'sort':
            self.sort_column = column
            self.sort_ascending = value
        
        elif action == 'clear':
            if column in self.filters:
                del self.filters[column]
            if self.sort_column == column:
                self.sort_column = None
        
        # Apply changes to data processor
        self.apply_filters_to_processor()
        
        # Refresh display
        self.refresh_data()
        
        # Notify parent of data change
        self.on_data_changed()
    
    def apply_filters_to_processor(self):
        """Apply current filters to the data processor"""
        if self.data_processor.original_data is None:
            return
        
        # Start with original data
        filtered_data = self.data_processor.original_data.copy()
        
        # Apply filters
        for column, selected_values in self.filters.items():
            if column in filtered_data.columns and selected_values:
                filtered_data = filtered_data[filtered_data[column].isin(selected_values)]
        
        # Apply sorting
        if self.sort_column and self.sort_column in filtered_data.columns:
            filtered_data = filtered_data.sort_values(
                by=self.sort_column, 
                ascending=self.sort_ascending, 
                na_position='last'
            )
        
        # Update data processor
        self.data_processor.data = filtered_data
    
    def clear_all_filters(self):
        """Clear all filters and sorting"""
        self.filters.clear()
        self.sort_column = None
        self.sort_ascending = True
        
        # Restore original data
        if self.data_processor.original_data is not None:
            self.data_processor.data = self.data_processor.original_data.copy()
        
        self.refresh_data()
        self.on_data_changed()
    
    def update_data(self):
        """Update when new data is loaded"""
        self.filters.clear()
        self.sort_column = None
        self.sort_ascending = True
        self.refresh_data()
    
    def pack(self, **kwargs):
        """Pack the frame"""
        self.frame.pack(**kwargs)
    
    def grid(self, **kwargs):
        """Grid the frame"""
        self.frame.grid(**kwargs)

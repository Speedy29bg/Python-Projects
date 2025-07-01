#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Data Filtering Window

A separate window for managing data filters and sorting with Excel-style interface.
"""

import tkinter as tk
from tkinter import ttk
import pandas as pd
from typing import Dict, List, Any, Optional, Callable
import numpy as np
from utils.logger import get_logger

logger = get_logger()

class FilterWindow:
    """Data filtering and sorting window"""
    
    def __init__(self, parent, data_processor, on_data_changed: Callable):
        """
        Initialize the filtering window
        
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
        self.window = None
        self.tree = None
        self.info_label = None
        
    def show_window(self):
        """Show the filtering window"""
        if self.window and self.window.winfo_exists():
            # Window already exists, just bring it to front
            self.window.lift()
            self.window.focus_set()
            return
            
        # Create new window
        self.window = tk.Toplevel(self.parent)
        self.window.title("Data Filters & Sorting")
        self.window.geometry("800x600")
        self.window.resizable(True, True)
        
        # Make window modal
        self.window.grab_set()
        self.window.focus_set()
        
        # Center the window
        self.center_window()
        
        # Handle window close
        self.window.protocol("WM_DELETE_WINDOW", self.close_window)
        
        self.create_ui()
        self.refresh_data()
        
    def center_window(self):
        """Center the window on the parent"""
        self.window.update_idletasks()
        
        # Get parent window position and size
        parent_x = self.parent.winfo_x()
        parent_y = self.parent.winfo_y()
        parent_width = self.parent.winfo_width()
        parent_height = self.parent.winfo_height()
        
        # Get window size
        window_width = 800
        window_height = 600
        
        # Calculate position to center on parent
        x = parent_x + (parent_width // 2) - (window_width // 2)
        y = parent_y + (parent_height // 2) - (window_height // 2)
        
        # Ensure window is on screen
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        x = max(0, min(x, screen_width - window_width))
        y = max(0, min(y, screen_height - window_height))
        
        self.window.geometry(f"{window_width}x{window_height}+{x}+{y}")
    
    def create_ui(self):
        """Create the filtering window UI"""
        # Main frame
        main_frame = ttk.Frame(self.window, padding=10)
        main_frame.pack(fill='both', expand=True)
        
        # Title
        title_label = ttk.Label(main_frame, text="Data Filters & Sorting", 
                               font=('TkDefaultFont', 12, 'bold'))
        title_label.pack(pady=(0, 10))
        
        # Toolbar
        toolbar = ttk.Frame(main_frame)
        toolbar.pack(fill='x', pady=(0, 10))
        
        ttk.Button(toolbar, text="Add Filter", 
                  command=self.add_filter).pack(side='left', padx=(0, 5))
        ttk.Button(toolbar, text="Clear All Filters", 
                  command=self.clear_all_filters).pack(side='left', padx=(0, 5))
        ttk.Button(toolbar, text="Apply & Close", 
                  command=self.apply_and_close).pack(side='right', padx=(5, 0))
        ttk.Button(toolbar, text="Cancel", 
                  command=self.close_window).pack(side='right')
        
        # Current filters frame
        filters_frame = ttk.LabelFrame(main_frame, text="Active Filters", padding=5)
        filters_frame.pack(fill='x', pady=(0, 10))
        
        # Filters list
        self.filters_listbox = tk.Listbox(filters_frame, height=4)
        self.filters_listbox.pack(fill='x')
        
        # Remove filter button
        remove_frame = ttk.Frame(filters_frame)
        remove_frame.pack(fill='x', pady=(5, 0))
        ttk.Button(remove_frame, text="Remove Selected Filter", 
                  command=self.remove_selected_filter).pack(side='left')
        
        # Sorting frame
        sort_frame = ttk.LabelFrame(main_frame, text="Sorting", padding=5)
        sort_frame.pack(fill='x', pady=(0, 10))
        
        # Sort column selection
        sort_col_frame = ttk.Frame(sort_frame)
        sort_col_frame.pack(fill='x')
        
        ttk.Label(sort_col_frame, text="Sort by:").pack(side='left')
        self.sort_column_var = tk.StringVar()
        self.sort_column_combo = ttk.Combobox(sort_col_frame, textvariable=self.sort_column_var,
                                            state='readonly', width=20)
        self.sort_column_combo.pack(side='left', padx=(5, 10))
        
        # Sort direction
        self.sort_direction_var = tk.StringVar(value="Ascending")
        ttk.Radiobutton(sort_col_frame, text="Ascending", 
                       variable=self.sort_direction_var, value="Ascending").pack(side='left', padx=(0, 5))
        ttk.Radiobutton(sort_col_frame, text="Descending", 
                       variable=self.sort_direction_var, value="Descending").pack(side='left')
        
        # Sort buttons
        sort_buttons_frame = ttk.Frame(sort_col_frame)
        sort_buttons_frame.pack(side='right')
        
        ttk.Button(sort_buttons_frame, text="Apply Sort", 
                  command=self.apply_sort).pack(side='left', padx=(0, 5))
        ttk.Button(sort_buttons_frame, text="Clear Sort", 
                  command=self.clear_sort).pack(side='left')
        
        # Sort status label
        self.sort_status_label = ttk.Label(sort_frame, text="No sorting applied", 
                                         foreground="gray", font=('TkDefaultFont', 8))
        self.sort_status_label.pack(anchor='w', pady=(5, 0))
        
        # Data preview frame
        preview_frame = ttk.LabelFrame(main_frame, text="Data Preview", padding=5)
        preview_frame.pack(fill='both', expand=True)
        
        # Info label
        self.info_label = ttk.Label(preview_frame, text="No data loaded", foreground="gray")
        self.info_label.pack(anchor='w', pady=(0, 5))
        
        # Table frame with scrollbars
        table_frame = ttk.Frame(preview_frame)
        table_frame.pack(fill='both', expand=True)
        
        # Create Treeview for data display
        self.tree = ttk.Treeview(table_frame, show='tree headings', height=12)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        h_scrollbar = ttk.Scrollbar(table_frame, orient="horizontal", command=self.tree.xview)
        
        self.tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Pack scrollbars and tree
        v_scrollbar.pack(side="right", fill="y")
        h_scrollbar.pack(side="bottom", fill="x")
        self.tree.pack(side="left", fill="both", expand=True)
        
    def add_filter(self):
        """Show dialog to add a new filter"""
        if self.data_processor.original_data is None or self.data_processor.original_data.empty:
            tk.messagebox.showwarning("No Data", "Please load data first")
            return
            
        # Get available columns
        columns = list(self.data_processor.original_data.columns)
        
        # Show column selection dialog
        column = self.select_column_dialog(columns)
        if not column:
            return
            
        # Get unique values for the column
        unique_values = self.data_processor.original_data[column].dropna().unique().tolist()
        if not unique_values:
            tk.messagebox.showwarning("No Values", f"No values found in column '{column}'")
            return
            
        # Show filter values dialog
        selected_values = self.select_values_dialog(column, unique_values)
        if selected_values:
            self.filters[column] = selected_values
            self.update_filters_display()
            self.refresh_preview()
    
    def select_column_dialog(self, columns: List[str]) -> Optional[str]:
        """Show dialog to select a column for filtering"""
        dialog = tk.Toplevel(self.window)
        dialog.title("Select Column")
        dialog.geometry("300x200")
        dialog.grab_set()
        dialog.resizable(False, False)
        
        # Center on parent window
        dialog.update_idletasks()
        x = self.window.winfo_x() + (self.window.winfo_width() // 2) - 150
        y = self.window.winfo_y() + (self.window.winfo_height() // 2) - 100
        dialog.geometry(f"300x200+{x}+{y}")
        
        selected_column = None
        
        frame = ttk.Frame(dialog, padding=10)
        frame.pack(fill='both', expand=True)
        
        ttk.Label(frame, text="Select column to filter:").pack(pady=(0, 10))
        
        # Column listbox
        listbox = tk.Listbox(frame)
        listbox.pack(fill='both', expand=True, pady=(0, 10))
        
        for col in columns:
            listbox.insert(tk.END, col)
        
        def on_select():
            nonlocal selected_column
            selection = listbox.curselection()
            if selection:
                selected_column = columns[selection[0]]
                dialog.destroy()
        
        def on_cancel():
            dialog.destroy()
        
        # Buttons
        button_frame = ttk.Frame(frame)
        button_frame.pack(fill='x')
        
        ttk.Button(button_frame, text="OK", command=on_select).pack(side='right', padx=(5, 0))
        ttk.Button(button_frame, text="Cancel", command=on_cancel).pack(side='right')
        
        # Handle double-click
        listbox.bind('<Double-Button-1>', lambda e: on_select())
        
        dialog.wait_window()
        return selected_column
    
    def select_values_dialog(self, column: str, unique_values: List) -> Optional[List]:
        """Show dialog to select values for filtering"""
        dialog = tk.Toplevel(self.window)
        dialog.title(f"Filter Values - {column}")
        dialog.geometry("400x500")
        dialog.grab_set()
        dialog.resizable(True, True)
        
        # Center on parent window
        dialog.update_idletasks()
        x = self.window.winfo_x() + (self.window.winfo_width() // 2) - 200
        y = self.window.winfo_y() + (self.window.winfo_height() // 2) - 250
        dialog.geometry(f"400x500+{x}+{y}")
        
        selected_values = None
        value_vars = {}
        
        main_frame = ttk.Frame(dialog, padding=10)
        main_frame.pack(fill='both', expand=True)
        
        ttk.Label(main_frame, text=f"Select values for '{column}':").pack(pady=(0, 10))
        
        # Select all checkbox
        select_all_var = tk.BooleanVar(value=True)
        select_all_cb = ttk.Checkbutton(main_frame, text="Select All", variable=select_all_var)
        select_all_cb.pack(anchor='w', pady=(0, 5))
        
        # Scrollable frame for checkboxes
        canvas = tk.Canvas(main_frame)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Create checkboxes for each unique value
        sorted_values = sorted(unique_values, key=lambda x: str(x))
        for value in sorted_values:
            var = tk.BooleanVar(value=True)
            value_vars[value] = var
            
            cb_frame = ttk.Frame(scrollable_frame)
            cb_frame.pack(fill='x', padx=2, pady=1)
            
            ttk.Checkbutton(cb_frame, text=str(value), variable=var).pack(anchor='w')
        
        def toggle_select_all():
            state = select_all_var.get()
            for var in value_vars.values():
                var.set(state)
        
        select_all_cb.configure(command=toggle_select_all)
        
        def on_ok():
            nonlocal selected_values
            selected_values = [value for value, var in value_vars.items() if var.get()]
            dialog.destroy()
        
        def on_cancel():
            dialog.destroy()
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill='x', pady=(10, 0))
        
        ttk.Button(button_frame, text="OK", command=on_ok).pack(side='right', padx=(5, 0))
        ttk.Button(button_frame, text="Cancel", command=on_cancel).pack(side='right')
        
        dialog.wait_window()
        return selected_values
    
    def remove_selected_filter(self):
        """Remove the selected filter"""
        selection = self.filters_listbox.curselection()
        if not selection:
            tk.messagebox.showwarning("No Selection", "Please select a filter to remove")
            return
            
        # Get the filter text and extract column name
        filter_text = self.filters_listbox.get(selection[0])
        column = filter_text.split(":")[0]
        
        if column in self.filters:
            del self.filters[column]
            self.update_filters_display()
            self.refresh_preview()
    
    def clear_all_filters(self):
        """Clear all filters and sorting"""
        self.filters.clear()
        self.sort_column = None
        self.sort_ascending = True
        
        try:
            # Only update UI components if they exist
            if hasattr(self, 'sort_column_var') and self.sort_column_var:
                self.sort_column_var.set("")
            if hasattr(self, 'sort_direction_var') and self.sort_direction_var:
                self.sort_direction_var.set("Ascending")
            
            # Update sort status label
            if hasattr(self, 'sort_status_label') and self.sort_status_label:
                self.sort_status_label.config(text="No sorting applied", foreground="gray")
            
            # Only update UI if window exists
            if self.window and self.window.winfo_exists():
                self.update_filters_display()
                self.refresh_preview()
        except tk.TclError:
            # Widget has been destroyed, ignore
            pass
        except Exception as e:
            logger.warning(f"Error clearing filters: {e}")
    
    def apply_sort(self):
        """Apply the selected sorting"""
        try:
            if not hasattr(self, 'sort_column_var') or not self.sort_column_var:
                tk.messagebox.showwarning("No Sort Column", "Please select a column to sort by")
                return
            
            sort_column = self.sort_column_var.get()
            if not sort_column:
                tk.messagebox.showwarning("No Sort Column", "Please select a column to sort by")
                return
            
            # Check if column exists in data
            if (self.data_processor.original_data is not None and 
                sort_column not in self.data_processor.original_data.columns):
                tk.messagebox.showerror("Invalid Column", f"Column '{sort_column}' not found in data")
                return
            
            # Apply sorting and refresh preview
            self.refresh_preview()
            
            # Update sort status label
            direction = self.sort_direction_var.get() if hasattr(self, 'sort_direction_var') else "Ascending"
            if hasattr(self, 'sort_status_label') and self.sort_status_label:
                self.sort_status_label.config(
                    text=f"Sorted by '{sort_column}' ({direction})", 
                    foreground="blue"
                )
            
            # Show confirmation
            tk.messagebox.showinfo("Sort Applied", f"Data sorted by '{sort_column}' ({direction})")
            
        except Exception as e:
            logger.error(f"Error applying sort: {e}")
            tk.messagebox.showerror("Sort Error", f"Failed to apply sort: {e}")

    def clear_sort(self):
        """Clear sorting"""
        self.sort_column = None
        self.sort_ascending = True
        
        try:
            # Only update UI components if they exist
            if hasattr(self, 'sort_column_var') and self.sort_column_var:
                self.sort_column_var.set("")
            if hasattr(self, 'sort_direction_var') and self.sort_direction_var:
                self.sort_direction_var.set("Ascending")
            
            # Update sort status label
            if hasattr(self, 'sort_status_label') and self.sort_status_label:
                self.sort_status_label.config(text="No sorting applied", foreground="gray")
                
            # Only refresh if window exists
            if self.window and self.window.winfo_exists():
                self.refresh_preview()
                
        except tk.TclError:
            # Widget has been destroyed, ignore
            pass
        except Exception as e:
            logger.warning(f"Error clearing sort: {e}")
    
    def update_filters_display(self):
        """Update the filters listbox"""
        try:
            # Only update if listbox exists
            if not (hasattr(self, 'filters_listbox') and self.filters_listbox):
                return
                
            self.filters_listbox.delete(0, tk.END)
            for column, values in self.filters.items():
                if len(values) <= 3:
                    values_text = ", ".join(str(v) for v in values[:3])
                else:
                    values_text = f"{', '.join(str(v) for v in values[:3])} + {len(values)-3} more"
                self.filters_listbox.insert(tk.END, f"{column}: {values_text}")
        except tk.TclError:
            # Widget has been destroyed, ignore
            pass
        except Exception as e:
            logger.warning(f"Error updating filters display: {e}")
    
    def refresh_preview(self):
        """Refresh the data preview"""
        if self.data_processor.original_data is None:
            return
        
        try:
            # Only update if window exists and UI components are created
            if not (self.window and self.window.winfo_exists() and hasattr(self, 'tree') and self.tree):
                return
                
            # Get filtered data
            filtered_data = self.get_filtered_data()
            
            # Update tree
            self.update_tree(filtered_data)
            
            # Update info
            original_rows = len(self.data_processor.original_data)
            filtered_rows = len(filtered_data)
            
            if hasattr(self, 'info_label') and self.info_label:
                if filtered_rows != original_rows:
                    self.info_label.config(text=f"Showing {filtered_rows} of {original_rows} rows (filtered)", 
                                          foreground="blue")
                else:
                    self.info_label.config(text=f"Showing {filtered_rows} rows", foreground="black")
        except tk.TclError:
            # Widget has been destroyed, ignore
            pass
        except Exception as e:
            logger.warning(f"Error refreshing preview: {e}")
    
    def get_filtered_data(self) -> pd.DataFrame:
        """Get filtered and sorted data"""
        if self.data_processor.original_data is None:
            return pd.DataFrame()
        
        data = self.data_processor.original_data.copy()
        
        # Apply filters
        for column, selected_values in self.filters.items():
            if column in data.columns and selected_values:
                data = data[data[column].isin(selected_values)]
        
        # Apply sorting - check if UI components exist
        sort_column = None
        ascending = True
        
        try:
            if hasattr(self, 'sort_column_var') and self.sort_column_var:
                sort_column = self.sort_column_var.get()
            
            if hasattr(self, 'sort_direction_var') and self.sort_direction_var:
                ascending = self.sort_direction_var.get() == "Ascending"
        except tk.TclError:
            # Variable has been destroyed, ignore
            pass
        except Exception as e:
            logger.warning(f"Error getting sort parameters: {e}")
        
        if sort_column and sort_column in data.columns:
            data = data.sort_values(by=sort_column, ascending=ascending, na_position='last')
        
        return data
    
    def update_tree(self, data: pd.DataFrame):
        """Update the treeview with data"""
        try:
            # Only update if tree exists
            if not (hasattr(self, 'tree') and self.tree):
                return
                
            # Clear existing data
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            if data.empty:
                return
            
            # Configure columns
            columns = list(data.columns)
            self.tree.configure(columns=columns)
            
            # Set column headings and widths
            self.tree.heading('#0', text='Row', anchor='w')
            self.tree.column('#0', width=50, minwidth=50)
            
            for col in columns:
                self.tree.heading(col, text=col, anchor='w')
                self.tree.column(col, width=100, minwidth=80)
            
            # Add data rows (limit to first 1000 for performance)
            max_rows = min(1000, len(data))
            for i in range(max_rows):
                row = data.iloc[i]
                values = [str(row[col]) if pd.notna(row[col]) else "" for col in columns]
                self.tree.insert('', 'end', text=str(i+1), values=values)
            
            if len(data) > max_rows:
                self.tree.insert('', 'end', text='...', values=['...'] * len(columns))
        except tk.TclError:
            # Widget has been destroyed, ignore
            pass
        except Exception as e:
            logger.warning(f"Error updating tree: {e}")
    
    def refresh_data(self):
        """Refresh when new data is loaded"""
        try:
            if self.data_processor.original_data is not None and hasattr(self, 'sort_column_combo'):
                # Update sort column options only if the combo exists and window is still valid
                if (self.window and self.window.winfo_exists() and 
                    self.sort_column_combo and self.sort_column_combo.winfo_exists()):
                    columns = list(self.data_processor.original_data.columns)
                    self.sort_column_combo['values'] = [""] + columns
            
            # Only refresh preview if window exists and is visible
            if self.window and self.window.winfo_exists():
                self.refresh_preview()
        except tk.TclError:
            # Widget has been destroyed, ignore
            pass
        except Exception as e:
            logger.warning(f"Error refreshing filter window data: {e}")
    
    def apply_and_close(self):
        """Apply filters to data processor and close window"""
        self.apply_filters_to_processor()
        self.close_window()
    
    def apply_filters_to_processor(self):
        """Apply current filters to the data processor"""
        if self.data_processor.original_data is None:
            return
        
        # Get filtered data
        filtered_data = self.get_filtered_data()
        
        # Update data processor
        self.data_processor.data = filtered_data
        
        # Notify parent of data change
        self.on_data_changed()
        
        logger.info(f"Applied filters - showing {len(filtered_data)} of {len(self.data_processor.original_data)} rows")
    
    def close_window(self):
        """Close the filtering window"""
        if self.window:
            self.window.grab_release()
            self.window.destroy()
            self.window = None

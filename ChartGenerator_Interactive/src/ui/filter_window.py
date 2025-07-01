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
        """Show dialog to add a new filter with type selection and backend integration"""
        if self.data_processor.original_data is None or self.data_processor.original_data.empty:
            tk.messagebox.showwarning("No Data", "Please load data first")
            return
        columns = list(self.data_processor.original_data.columns)
        column = self.select_column_dialog(columns)
        if not column:
            return
        unique_values = self.data_processor.original_data[column].dropna().unique().tolist()
        if not unique_values:
            tk.messagebox.showwarning("No Values", f"No values found in column '{column}'")
            return
        # Get column type
        col_stats = self.data_processor.get_column_stats_for_filter(column)
        is_numeric = col_stats.get('is_numeric', False)
        # Show filter type and value dialog
        filter_type, value, value2 = self.select_filter_type_and_value_dialog(column, unique_values, is_numeric)
        if filter_type is not None:
            # Convert value(s) to correct type if numeric
            if is_numeric:
                try:
                    if filter_type == 'between' and value2 is not None:
                        value = float(value)
                        value2 = float(value2)
                    elif filter_type in ('greater_than', 'less_than', 'greater_equal', 'less_equal', 'equals', 'not_equals'):
                        value = float(value)
                except Exception:
                    tk.messagebox.showerror("Type Error", "Please enter a valid number for the filter value.")
                    return
            # Add filter to backend
            self.data_processor.add_filter(column, filter_type, value, value2)
            self.update_filters_display()
            self.refresh_preview()
    def select_filter_type_and_value_dialog(self, column: str, unique_values: list, is_numeric: bool):
        """Show dialog to select filter type and value(s)"""
        dialog = tk.Toplevel(self.window)
        dialog.title(f"Filter - {column}")
        dialog.geometry("400x300")
        dialog.grab_set()
        dialog.resizable(False, False)

        filter_types = [
            ("Equals", "equals"),
            ("Not Equals", "not_equals"),
            ("In List", "in_list"),
            ("Not In List", "not_in_list"),
            ("Contains", "contains"),
            ("Not Contains", "not_contains"),
            ("Starts With", "starts_with"),
            ("Ends With", "ends_with"),
            ("Is Null", "is_null"),
            ("Is Not Null", "is_not_null")
        ]
        if is_numeric:
            filter_types += [
                ("Greater Than", "greater_than"),
                ("Less Than", "less_than"),
                ("Greater or Equal", "greater_equal"),
                ("Less or Equal", "less_equal"),
                ("Between", "between")
            ]

        selected_type = tk.StringVar(value=filter_types[0][1])
        value_var = tk.StringVar()
        value2_var = tk.StringVar()
        selected_values = []

        main_frame = ttk.Frame(dialog, padding=10)
        main_frame.pack(fill='both', expand=True)

        ttk.Label(main_frame, text=f"Select filter type for '{column}':").pack(anchor='w')
        type_combo = ttk.Combobox(main_frame, values=[ft[0] for ft in filter_types], state='readonly')
        type_combo.current(0)
        type_combo.pack(fill='x', pady=(5, 10))

        value_frame = ttk.Frame(main_frame)
        value_frame.pack(fill='x', pady=(5, 0))

        value_label = ttk.Label(value_frame, text="Value:")
        value_entry = ttk.Entry(value_frame, textvariable=value_var)
        value2_label = ttk.Label(value_frame, text="and")
        value2_entry = ttk.Entry(value_frame, textvariable=value2_var)

        # Listbox for in_list/not_in_list
        listbox = tk.Listbox(main_frame, selectmode=tk.MULTIPLE, height=8)
        if len(unique_values) > 100:
            ttk.Label(main_frame, text="Warning: Too many unique values, showing first 100.", foreground="red").pack()
            unique_values = unique_values[:100]
        for v in unique_values:
            listbox.insert(tk.END, str(v))

        def update_value_widgets(event=None):
            ft = type_combo.get()
            # Hide all
            value_label.pack_forget()
            value_entry.pack_forget()
            value2_label.pack_forget()
            value2_entry.pack_forget()
            listbox.pack_forget()
            if ft in ["Equals", "Not Equals", "Contains", "Not Contains", "Starts With", "Ends With", "Greater Than", "Less Than", "Greater or Equal", "Less or Equal"]:
                value_label.pack(side='left')
                value_entry.pack(side='left', fill='x', expand=True)
            elif ft == "Between":
                value_label.pack(side='left')
                value_entry.pack(side='left', fill='x', expand=True)
                value2_label.pack(side='left', padx=5)
                value2_entry.pack(side='left', fill='x', expand=True)
            elif ft in ["In List", "Not In List"]:
                listbox.pack(fill='both', expand=True)

        type_combo.bind('<<ComboboxSelected>>', update_value_widgets)
        update_value_widgets()

        result = {'filter_type': None, 'value': None, 'value2': None}

        def on_ok():
            ft_label = type_combo.get()
            ft = None
            for label, code in filter_types:
                if label == ft_label:
                    ft = code
                    break
            if ft is None:
                tk.messagebox.showerror("Error", "Please select a filter type.")
                return
            if ft in ["in_list", "not_in_list"]:
                indices = listbox.curselection()
                if not indices:
                    tk.messagebox.showwarning("No Selection", "Please select at least one value.")
                    return
                selected = [unique_values[i] for i in indices]
                result['filter_type'] = ft
                result['value'] = selected
                result['value2'] = None
            elif ft == "between":
                v1 = value_var.get()
                v2 = value2_var.get()
                if not v1 or not v2:
                    tk.messagebox.showwarning("Missing Value", "Please enter both values for 'between' filter.")
                    return
                result['filter_type'] = ft
                result['value'] = v1
                result['value2'] = v2
            elif ft in ["is_null", "is_not_null"]:
                result['filter_type'] = ft
                result['value'] = None
                result['value2'] = None
            else:
                v = value_var.get()
                if not v:
                    tk.messagebox.showwarning("Missing Value", "Please enter a value for the filter.")
                    return
                result['filter_type'] = ft
                result['value'] = v
                result['value2'] = None
            dialog.destroy()

        def on_cancel():
            dialog.destroy()

        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill='x', pady=(10, 0))
        ttk.Button(button_frame, text="OK", command=on_ok).pack(side='right', padx=(5, 0))
        ttk.Button(button_frame, text="Cancel", command=on_cancel).pack(side='right')

        dialog.wait_window()
        return result['filter_type'], result['value'], result['value2']
    
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
        filter_text = self.filters_listbox.get(selection[0])
        column = filter_text.split(":")[0]
        self.data_processor.remove_filter(column)
        self.update_filters_display()
        self.refresh_preview()
    
    def clear_all_filters(self):
        """Clear all filters and sorting"""
        self.data_processor.clear_filters()
        self.sort_column = None
        self.sort_ascending = True
        try:
            if hasattr(self, 'sort_column_var') and self.sort_column_var:
                self.sort_column_var.set("")
            if hasattr(self, 'sort_direction_var') and self.sort_direction_var:
                self.sort_direction_var.set("Ascending")
            if hasattr(self, 'sort_status_label') and self.sort_status_label:
                self.sort_status_label.config(text="No sorting applied", foreground="gray")
            if self.window and self.window.winfo_exists():
                self.update_filters_display()
                self.refresh_preview()
        except tk.TclError:
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
            if not (hasattr(self, 'filters_listbox') and self.filters_listbox):
                return
            self.filters_listbox.delete(0, tk.END)
            filters = getattr(self.data_processor.data_filter, 'filters', {})
            for column, f in filters.items():
                ftype = f.get('type', '')
                val = f.get('value', '')
                val2 = f.get('value2', None)
                if ftype == 'between' and val2 is not None:
                    values_text = f"{ftype}: {val} and {val2}"
                elif isinstance(val, (list, tuple)):
                    if len(val) <= 3:
                        values_text = f"{ftype}: {', '.join(str(v) for v in val[:3])}"
                    else:
                        values_text = f"{ftype}: {', '.join(str(v) for v in val[:3])} + {len(val)-3} more"
                else:
                    values_text = f"{ftype}: {val}"
                self.filters_listbox.insert(tk.END, f"{column}: {values_text}")
        except tk.TclError:
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
        """Get filtered and sorted data (delegates to backend)"""
        if self.data_processor.original_data is None:
            return pd.DataFrame()
        # Apply sorting if set in UI
        sort_column = None
        ascending = True
        try:
            if hasattr(self, 'sort_column_var') and self.sort_column_var:
                sort_column = self.sort_column_var.get()
            if hasattr(self, 'sort_direction_var') and self.sort_direction_var:
                ascending = self.sort_direction_var.get() == "Ascending"
        except tk.TclError:
            pass
        except Exception as e:
            logger.warning(f"Error getting sort parameters: {e}")
        # Set sort in backend
        if sort_column and sort_column in self.data_processor.original_data.columns:
            self.data_processor.data_filter.set_sort(sort_column, ascending)
        else:
            self.data_processor.data_filter.set_sort(None)
        # Apply filters and sorting
        return self.data_processor.data_filter.apply_filters(self.data_processor.original_data)
    
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

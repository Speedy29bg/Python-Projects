"""
File Data Handler Module

This module handles file loading and data management 
for the Lab Chart Generator application.

Author: Lab Chart Tools Team
"""

import pandas as pd
import os
import queue
import threading
import tkinter as tk
from tkinter import ttk, messagebox
import logging
from typing import List, Dict, Callable, Any

from modules.data_processor import detect_header_row, read_csv_file

class FileDataHandler:
    """Handles file loading and data management for the application"""
    
    def __init__(self, app_instance):
        """
        Initialize file data handler
        
        Args:
            app_instance: Reference to the main application instance
        """
        self.app = app_instance
        self.files: List[str] = []
        self.file_data_cache: Dict[str, pd.DataFrame] = {}  # Cache for loaded file data
        self.column_headers: List[str] = []
    
    def select_files(self, file_select_dialog, status_label):
        """Handle file selection and load column headers
        
        Args:
            file_select_dialog: Function to display file selection dialog
            status_label: Status label to update during operations
            
        Returns:
            bool: True if files were selected, False otherwise
        """
        selected_files = file_select_dialog(filetypes=[("CSV files", "*.csv")])
        
        if not selected_files:
            return False
        
        self.files = selected_files
        
        try:
            # Clear cache for files that are no longer selected
            self.file_data_cache = {k: v for k, v in self.file_data_cache.items() if k in self.files}
            
            # Load files in background
            self.load_files_in_background(self.files, self.app.detect_headers_and_populate_listboxes, status_label)
            return True
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load file(s): {str(e)}")
            status_label.config(text="Error loading files")
            return False
    
    def load_files_in_background(self, files, callback, status_label):
        """Load files in background thread to keep UI responsive
        
        Args:
            files: List of file paths to load
            callback: Function to call when loading is complete
            status_label: Status label to update during operations
        """
        status_label.config(text="Loading files...")
        root = status_label.winfo_toplevel()
        
        # Create loading indicator
        loading_frame = ttk.Frame(root)
        loading_frame.place(relx=0.5, rely=0.5, anchor='center')
        
        loading_label = ttk.Label(loading_frame, text="Loading files...", font=('Helvetica', 12, 'bold'))
        loading_label.pack(pady=10)
        
        progress = ttk.Progressbar(loading_frame, orient="horizontal", length=300, mode="indeterminate")
        progress.pack(pady=10)
        progress.start(10)
        
        # Create queue for thread communication
        file_queue = queue.Queue()
        
        # Function to run in background thread
        def load_files_thread():
            loaded_data = {}
            
            for i, file_path in enumerate(files):
                try:
                    header_row_idx = detect_header_row(file_path)
                    df = read_csv_file(file_path, header_row_idx)
                    loaded_data[file_path] = df
                    
                    # Update progress info via queue
                    file_queue.put(("progress", i+1, len(files), os.path.basename(file_path)))
                except Exception as e:
                    file_queue.put(("error", os.path.basename(file_path), str(e)))
            
            # Signal completion
            file_queue.put(("done", loaded_data))
        
        # Function to process queue updates in main thread
        def check_queue():
            try:
                while True:
                    message = file_queue.get_nowait()
                    
                    if message[0] == "progress":
                        _, current, total, filename = message
                        loading_label.config(text=f"Loading {current}/{total}: {filename}")
                    
                    elif message[0] == "error":
                        _, filename, error = message
                        logging.error(f"Error loading {filename}: {error}")
                    
                    elif message[0] == "done":
                        _, loaded_data = message
                        # Update cache with loaded data
                        self.file_data_cache.update(loaded_data)
                        
                        # Remove loading indicator
                        loading_frame.destroy()
                        
                        # Call the callback
                        if callback:
                            callback()
                        
                        return  # Exit the update loop
            
            except queue.Empty:
                # Queue is empty but loading not complete, check again after a delay
                root.after(100, check_queue)
        
        # Start background thread
        threading.Thread(target=load_files_thread, daemon=True).start()
        
        # Start queue checking in main thread
        check_queue()
        
    def get_data_from_file(self, file_path):
        """Get data from a specific file, loading it if not in cache
        
        Args:
            file_path: Path to the file to load
            
        Returns:
            pd.DataFrame: DataFrame containing the file data
        """
        if file_path in self.file_data_cache:
            return self.file_data_cache[file_path]
        else:
            header_row_idx = detect_header_row(file_path)
            df = read_csv_file(file_path, header_row_idx)
            self.file_data_cache[file_path] = df
            return df

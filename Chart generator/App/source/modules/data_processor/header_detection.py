"""
Header Detection Module

This module provides functions for detecting header rows in CSV files.


Author: Speedy29bg
"""

import csv
import itertools
import logging

def detect_header_row(file_path: str) -> int:
    """Analyze a CSV file to determine the row containing column headers
    
    Args:
        file_path: Absolute path to the CSV file
        
    Returns:
        int: Index of the detected header row (0-based)
    """
    try:
        with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
            reader = csv.reader(f)
            rows = list(itertools.islice(reader, 0, 20))  # Read first 20 rows for analysis
            
            # Check if file is empty
            if not rows:
                logging.info("File is empty")
                return 0
            
            # Strategy 1: Look for the first row where most cells contain non-numeric content
            for i, row in enumerate(rows):
                if len(row) >= 4:  # Need at least 2 columns to be useful
                    # Check if this row has mostly text (non-numeric) content
                    non_numeric_count = sum(1 for cell in row if cell.strip() and not cell.replace('.', '', 1).isdigit())
                    if non_numeric_count > len(row) / 2:  # More than half are non-numeric
                        logging.debug(f"Detected header at row {i} (mostly text content)")
                        return i
            
            # Strategy 2: Fall back to first non-empty row
            for i, row in enumerate(rows):
                if any(cell.strip() for cell in row):
                    logging.debug(f"Using first non-empty row at index {i}")
                    return i
        
        # If all strategies fail, use the first row
        logging.debug("Using first row as header by default")
        return 0
    except Exception as e:
        logging.error(f"Error detecting header row: {str(e)}")
        return 0

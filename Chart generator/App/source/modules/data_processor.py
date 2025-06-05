import pandas as pd
import csv
import os
import re
import logging
import itertools
from typing import List, Dict, Tuple, Optional, Any, Union

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

def read_csv_file(file_path: str, header_row_idx: int) -> pd.DataFrame:
    """Read a CSV file with automatic encoding and delimiter detection
    
    Args:
        file_path: Absolute path to the CSV file
        header_row_idx: Index of the header row (0-based)
        
    Returns:
        pd.DataFrame: DataFrame containing the CSV data
        
    Raises:
        Exception: If all reading methods fail
    """
    try:
        logging.info(f"Attempting to read file: {file_path}")
        
        # Try to detect delimiter
        with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
            sample = f.read(4096)  # Read a sample of the file
        
        # Detect delimiter
        delimiter = ','  # Default delimiter
        try:
            sniffer = csv.Sniffer()
            if sample.strip():  # Make sure the sample isn't empty
                detected_delimiter = sniffer.sniff(sample).delimiter
                logging.debug(f"Detected delimiter: '{detected_delimiter}'")
                delimiter = detected_delimiter
        except Exception as e:
            logging.warning(f"Delimiter detection failed: {str(e)}. Using default delimiter: ','")
        
        # First try with pandas - the standard approach
        try:
            logging.debug(f"Reading CSV with pandas, header_row_idx: {header_row_idx}, delimiter: '{delimiter}'")
            df = pd.read_csv(file_path, encoding='utf-8', header=header_row_idx, delimiter=delimiter, 
                           low_memory=False, on_bad_lines='warn')
            
            # Check if we have data
            if not df.empty:
                logging.debug(f"CSV loaded successfully with pandas: {len(df)} rows, {len(df.columns)} columns")
                logging.debug(f"Column headers: {list(df.columns)}")
                return df
            else:
                logging.warning("DataFrame is empty after reading with pandas")
        except Exception as e:
            logging.warning(f"Error reading with pandas: {str(e)}")
        
        # Fall back to manual CSV reading if pandas fails
        try:
            logging.debug("Falling back to manual CSV reading...")
            with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
                csv_reader = csv.reader(f, delimiter=delimiter)
                rows = list(csv_reader)
            
            if not rows:
                logging.warning("File appears to be empty")
                return pd.DataFrame()
            
            if header_row_idx >= len(rows):
                logging.warning(f"Header row index ({header_row_idx}) out of range. Using first row.")
                header_row_idx = 0
            
            # Extract headers and data
            headers = rows[header_row_idx]
            data = rows[header_row_idx+1:] if header_row_idx+1 < len(rows) else []
            
            # Create DataFrame
            df = pd.DataFrame(data, columns=headers)
            
            # Convert numeric columns
            for col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='ignore')
            
            logging.debug(f"Manual CSV reading successful: {len(df)} rows, {len(df.columns)} columns")
            return df
            
        except Exception as e:
            logging.warning(f"Manual CSV reading failed: {str(e)}")
            
        # Try alternative encodings if UTF-8 fails
        for encoding in ['latin1', 'cp1252', 'iso-8859-1']:
            try:
                logging.debug(f"Trying with encoding: {encoding}")
                df = pd.read_csv(file_path, encoding=encoding, header=header_row_idx, 
                                delimiter=delimiter, low_memory=False)
                logging.debug(f"Successful load with {encoding} encoding")
                return df
            except Exception as e:
                logging.debug(f"Failed with {encoding} encoding: {str(e)}")
        
        # As a last resort, try to read without specifying encoding
        try:
            logging.debug("Last attempt: reading without specifying encoding")
            df = pd.read_csv(file_path, header=header_row_idx, delimiter=delimiter, 
                            low_memory=False, encoding_errors='replace')
            return df
        except Exception as e:
            logging.warning(f"Final attempt failed: {str(e)}")
            
        # If all attempts fail
        raise Exception("All methods to read the CSV file failed")
        
    except pd.errors.EmptyDataError:
        logging.warning(f"File {os.path.basename(file_path)} is empty.")
        return pd.DataFrame()
    except Exception as e:
        logging.error(f"Error reading CSV file: {str(e)}")
        raise Exception(f"Failed to read CSV file: {str(e)}")

def process_data_for_scaling(df, x_axis, y_axes, secondary_axes, settings):
    """Process DataFrame to implement scaling and transformation options
    
    Args:
        df: The input pandas DataFrame
        x_axis: Name of the X-axis column
        y_axes: List of primary Y-axis column names
        secondary_axes: List of secondary Y-axis column names
        settings: Dictionary with scaling settings (log_scale_x, log_scale_y1, etc.)
        
    Returns:
        pd.DataFrame: A processed copy of the input DataFrame
    """
    # Make a copy to avoid modifying original
    processed_df = df.copy()
    
    # Convert columns to numeric when possible
    columns_to_process = [x_axis] + y_axes + secondary_axes
    
    for col in columns_to_process:
        if col in processed_df.columns:  # Check if column exists
            # First, try to detect if this is a datetime column
            is_datetime = False
            
            # Check a sample of values for datetime format
            sample = processed_df[col].dropna().head(20).astype(str)
            date_patterns = [
                # Common datetime patterns
                r'\d{1,2}/\d{1,2}/\d{2,4}\s+\d{1,2}:\d{1,2}:\d{1,2}\s*(?:AM|PM)?',  # 1/16/2024 4:44:01 PM
                r'\d{1,2}-\d{1,2}-\d{2,4}\s+\d{1,2}:\d{1,2}:\d{1,2}',  # 16-01-2024 16:44:01
                r'\d{4}-\d{1,2}-\d{1,2}\s+\d{1,2}:\d{1,2}:\d{1,2}',  # 2024-01-16 16:44:01
                r'\d{1,2}/\d{1,2}/\d{2,4}'  # 1/16/2024
            ]
            
            # Check if most values match a datetime pattern
            for pattern in date_patterns:
                matches = sample.str.match(pattern).sum()
                if matches > len(sample) * 0.5:  # If more than 50% match
                    is_datetime = True
                    logging.debug(f"Column '{col}' detected as datetime")
                    break
            
            if is_datetime:
                try:
                    # Convert to datetime and then to timestamp for numeric processing
                    processed_df[col] = pd.to_datetime(processed_df[col], errors='coerce')
                    # Convert datetime to numeric (Unix timestamp in seconds)
                    processed_df[col] = processed_df[col].astype('int64') // 10**9
                    logging.debug(f"Converted datetime column '{col}' to timestamp values")
                except Exception as e:
                    logging.warning(f"Failed to convert datetime column '{col}': {str(e)}")
            else:
                # Try to convert to numeric if not already
                if not pd.api.types.is_numeric_dtype(processed_df[col]):
                    try:
                        processed_df[col] = pd.to_numeric(processed_df[col], errors='coerce')
                        logging.debug(f"Converted column '{col}' to numeric with NaN for non-numeric values")
                    except Exception as e:
                        logging.warning(f"Could not convert column '{col}' to numeric: {str(e)}")
        else:
            logging.warning(f"Column '{col}' does not exist in the dataframe")
    
    # For log scales, replace zeros and negative values with small positive values
    if settings.get('log_scale_x', False) and x_axis in processed_df.columns:
        # Replace negative/zero values for log scale
        min_positive = processed_df[x_axis][processed_df[x_axis] > 0].min() if any(processed_df[x_axis] > 0) else 0.001
        epsilon = min_positive / 10 if min_positive > 0 else 0.001
        processed_df[x_axis] = processed_df[x_axis].apply(lambda x: max(x, epsilon) if pd.notnull(x) else x)
    
    # Handle log scale for primary Y axes
    if settings.get('log_scale_y1', False):
        for y_axis in y_axes:
            if y_axis in processed_df.columns:
                min_positive = processed_df[y_axis][processed_df[y_axis] > 0].min() if any(processed_df[y_axis] > 0) else 0.001
                epsilon = min_positive / 10 if min_positive > 0 else 0.001
                processed_df[y_axis] = processed_df[y_axis].apply(lambda x: max(x, epsilon) if pd.notnull(x) else x)
    
    # Handle log scale for secondary Y axes
    if settings.get('log_scale_y2', False):
        for sec_axis in secondary_axes:
            if sec_axis in processed_df.columns:
                min_positive = processed_df[sec_axis][processed_df[sec_axis] > 0].min() if any(processed_df[sec_axis] > 0) else 0.001
                epsilon = min_positive / 10 if min_positive > 0 else 0.001
                processed_df[sec_axis] = processed_df[sec_axis].apply(lambda x: max(x, epsilon) if pd.notnull(x) else x)
    
    # Normalize data if selected
    if settings.get('normalize_data', False):
        for col in columns_to_process:
            if col in processed_df.columns and pd.api.types.is_numeric_dtype(processed_df[col]):
                col_min = processed_df[col].min()
                col_max = processed_df[col].max()
                if col_max > col_min:  # Prevent division by zero
                    processed_df[col] = (processed_df[col] - col_min) / (col_max - col_min)
    
    return processed_df

def create_safe_sheet_name(base_name: str) -> str:
    """Create a safe sheet name for Excel by removing invalid characters
    
    Args:
        base_name: Original file name to convert to sheet name
        
    Returns:
        str: A sanitized sheet name compatible with Excel requirements
    """
    safe_name = re.sub(r'[\\/*?:"<>|]', '_', base_name)
    return safe_name[:31]  # Excel sheet name limit is 31 characters
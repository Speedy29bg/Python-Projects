"""
CSV Reader Module

This module provides functions for reading CSV files with various encodings and delimiters.


Author: Speedy29bg
"""

import csv
import os
import logging
import pandas as pd

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

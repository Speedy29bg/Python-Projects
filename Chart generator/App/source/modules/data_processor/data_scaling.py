"""
Data Scaling Module

This module provides functions for scaling and transforming data for chart visualization.

Author: Lab Chart Tools Team
"""

import pandas as pd
import logging
from typing import List, Dict

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

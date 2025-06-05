"""
Smoothing Module

This module provides functions for smoothing and filtering time series data.


Author: Speedy29bg
"""

import pandas as pd
import numpy as np
from scipy.signal import savgol_filter
from scipy.ndimage import gaussian_filter1d
from typing import List

def smooth_data(df: pd.DataFrame, columns: List[str], method: str = 'moving_avg', 
                window_size: int = 3, sigma: float = 1.0) -> pd.DataFrame:
    """Apply smoothing to selected columns
    
    Args:
        df: The DataFrame containing the data
        columns: List of column names to smooth
        method: Smoothing method ('moving_avg', 'gaussian', 'savgol')
        window_size: Window size for moving average or Savitzky-Golay filter
        sigma: Standard deviation for Gaussian filter
        
    Returns:
        DataFrame with smoothed data
    """
    smoothed_df = df.copy()
    
    for col in columns:
        if col not in smoothed_df.columns or not pd.api.types.is_numeric_dtype(smoothed_df[col]):
            continue
            
        data = pd.to_numeric(smoothed_df[col], errors='coerce')
        
        # Skip columns with too few valid values
        if len(data.dropna()) <= window_size:
            continue
            
        # Apply selected smoothing method
        if method.lower() == 'moving_avg':
            # Moving average
            smoothed_df[col] = data.rolling(window=window_size, center=True, min_periods=1).mean()
            
        elif method.lower() == 'gaussian':
            # Gaussian filter
            valid_indices = ~data.isna()
            valid_data = data[valid_indices].values
            
            if len(valid_data) > 3:
                smooth_valid = gaussian_filter1d(valid_data, sigma=sigma)
                # Create a new series to preserve NaN values in the original
                result = pd.Series(index=data.index, dtype=float)
                result[valid_indices] = smooth_valid
                result[~valid_indices] = np.nan
                smoothed_df[col] = result
            
        elif method.lower() == 'savgol':
            # Savitzky-Golay filter
            valid_indices = ~data.isna()
            valid_data = data[valid_indices].values
            
            if len(valid_data) > window_size:
                # Make sure window size is odd
                window = window_size if window_size % 2 == 1 else window_size + 1
                # Order of polynomial can't exceed window size
                poly_order = min(3, window_size - 1)
                smooth_valid = savgol_filter(valid_data, window, poly_order)
                
                # Create a new series to preserve NaN values in the original
                result = pd.Series(index=data.index, dtype=float)
                result[valid_indices] = smooth_valid
                result[~valid_indices] = np.nan
                smoothed_df[col] = result
    
    return smoothed_df

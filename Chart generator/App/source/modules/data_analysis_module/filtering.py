"""
Filtering Module

This module provides functions for filtering and cleaning data.

Author: Lab Chart Tools Team
"""

import pandas as pd
import numpy as np
import scipy.stats as stats
from typing import List, Dict, Tuple, Any

def filter_outliers(df: pd.DataFrame, columns: List[str], method: str = 'iqr', threshold: float = 1.5) -> pd.DataFrame:
    """Filter outliers from selected columns
    
    Args:
        df: The DataFrame containing the data
        columns: List of column names to filter
        method: Method for outlier detection ('iqr' or 'zscore')
        threshold: Threshold for outlier detection (1.5 for IQR, 3.0 for z-score)
        
    Returns:
        DataFrame with outliers replaced with NaN
    """
    filtered_df = df.copy()
    
    for col in columns:
        if col not in filtered_df.columns or not pd.api.types.is_numeric_dtype(filtered_df[col]):
            continue
            
        data = pd.to_numeric(filtered_df[col], errors='coerce')
        
        if method.lower() == 'iqr':
            # IQR method
            q1 = np.percentile(data.dropna(), 25)
            q3 = np.percentile(data.dropna(), 75)
            iqr = q3 - q1
            
            lower_bound = q1 - threshold * iqr
            upper_bound = q3 + threshold * iqr
            
            # Replace outliers with NaN
            filtered_df.loc[(filtered_df[col] < lower_bound) | (filtered_df[col] > upper_bound), col] = np.nan
            
        elif method.lower() == 'zscore':
            # Z-score method
            z_scores = np.abs(stats.zscore(data.dropna()))
            # Get original indices that correspond to z_scores
            valid_indices = data.dropna().index
            
            # Create a mask to identify high z-scores
            z_mask = pd.Series(False, index=data.index)
            z_mask.loc[valid_indices] = np.abs(z_scores) > threshold
            
            # Replace outliers with NaN
            filtered_df.loc[z_mask, col] = np.nan
    
    return filtered_df

def detect_anomalies(df: pd.DataFrame, column: str, method: str = 'iqr', threshold: float = 2.0) -> Tuple[List[int], Any, Any]:
    """Detect anomalies in a column and return their indices
    
    Args:
        df: The DataFrame containing the data
        column: Column name to analyze for anomalies
        method: Method for anomaly detection ('iqr' or 'zscore')
        threshold: Threshold for anomaly detection
        
    Returns:
        Tuple containing (list of indices, lower bound, upper bound)
    """
    if column not in df.columns:
        return [], None, None
        
    data = pd.to_numeric(df[column], errors='coerce').dropna()
    anomaly_indices = []
    lower_bound = None
    upper_bound = None
    
    if method.lower() == 'iqr':
        # IQR method
        q1 = np.percentile(data, 25)
        q3 = np.percentile(data, 75)
        iqr = q3 - q1
        
        lower_bound = q1 - threshold * iqr
        upper_bound = q3 + threshold * iqr
        
        # Find indices of anomalies
        anomaly_mask = (data < lower_bound) | (data > upper_bound)
        anomaly_indices = data[anomaly_mask].index.tolist()
        
    elif method.lower() == 'zscore':
        # Z-score method
        z_scores = np.abs(stats.zscore(data))
        # Find indices of anomalies
        anomaly_mask = z_scores > threshold
        anomaly_indices = data[anomaly_mask].index.tolist()
        
        # For consistency with IQR, compute equivalent bounds
        mean = data.mean()
        std = data.std()
        lower_bound = mean - threshold * std
        upper_bound = mean + threshold * std
    
    return anomaly_indices, lower_bound, upper_bound

"""
Statistics Module

This module provides functions for calculating statistical metrics from data.

Author: Lab Chart Tools Team
"""

import pandas as pd
import numpy as np
import scipy.stats as stats
from typing import List, Dict

def calculate_statistics(df: pd.DataFrame, columns: List[str]) -> Dict[str, Dict[str, float]]:
    """Calculate basic statistical metrics for selected columns
    
    Args:
        df: The DataFrame containing the data
        columns: List of column names to analyze
        
    Returns:
        Dictionary with column names as keys and dictionaries of statistics as values
    """
    result = {}
    
    for col in columns:
        if col in df.columns:
            # Skip non-numeric columns
            if not pd.api.types.is_numeric_dtype(df[col]):
                continue
                
            # Get numeric data without NaN values
            data = pd.to_numeric(df[col], errors='coerce').dropna()
            
            if len(data) == 0:
                continue
                
            # Calculate statistics
            stats_dict = {
                'min': float(data.min()),
                'max': float(data.max()),
                'mean': float(data.mean()),
                'median': float(data.median()),
                'std': float(data.std()),
                'count': int(len(data)),
                'missing': int(df[col].isna().sum())
            }
            
            # Calculate additional statistics
            if len(data) >= 2:  # Need at least 2 points for these
                stats_dict['skew'] = float(stats.skew(data))
                stats_dict['kurtosis'] = float(stats.kurtosis(data))
                stats_dict['range'] = float(data.max() - data.min())
                stats_dict['iqr'] = float(np.percentile(data, 75) - np.percentile(data, 25))
                stats_dict['q1'] = float(np.percentile(data, 25))
                stats_dict['q3'] = float(np.percentile(data, 75))
                
            result[col] = stats_dict
    
    return result

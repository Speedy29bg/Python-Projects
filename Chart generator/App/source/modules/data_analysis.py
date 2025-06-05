"""
Data analysis module for the Lab Chart Generator application.

This module provides functions for analyzing and manipulating chart data,
including statistical analysis, data filtering, and transformations
beyond basic scaling provided by the data_processor module.


Author: Speedy29bg
"""

import pandas as pd
import numpy as np
import logging
from typing import List, Dict, Tuple, Optional, Any, Union
import scipy.stats as stats
import scipy.signal as signal
from scipy.ndimage import gaussian_filter1d

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
            
            # Map z-scores back to original indices
            non_na_indices = data.dropna().index
            z_score_map = pd.Series(z_scores, index=non_na_indices)
            
            # Replace outliers with NaN
            for idx, z_score in z_score_map.items():
                if z_score > threshold:
                    filtered_df.loc[idx, col] = np.nan
    
    return filtered_df

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
                smoothed_series = data.copy()
                smoothed_series[valid_indices] = smooth_valid
                smoothed_df[col] = smoothed_series
                
        elif method.lower() == 'savgol':
            # Savitzky-Golay filter
            valid_indices = ~data.isna()
            valid_data = data[valid_indices].values
            
            if len(valid_data) > window_size:
                # Window size must be odd and polyorder must be less than window_size
                poly_order = min(3, window_size - 1)
                if window_size % 2 == 0:
                    window_size += 1
                    
                smooth_valid = signal.savgol_filter(valid_data, window_size, poly_order)
                smoothed_series = data.copy()
                smoothed_series[valid_indices] = smooth_valid
                smoothed_df[col] = smoothed_series
    
    return smoothed_df

def calculate_derived_columns(df: pd.DataFrame, operations: List[Dict[str, Any]]) -> pd.DataFrame:
    """Create new columns by applying operations to existing columns
    
    Args:
        df: The DataFrame containing the data
        operations: List of dictionaries defining operations
                   Each dict should have keys:
                   - 'output_col': Name of the output column
                   - 'operation': Type of operation ('add', 'subtract', 'multiply', 'divide', 'formula')
                   - 'columns': List of input column names or a formula string
                   
    Returns:
        DataFrame with added derived columns
    """
    result_df = df.copy()
    
    for op in operations:
        try:
            output_col = op.get('output_col', 'derived_column')
            operation = op.get('operation', 'add')
            
            if operation == 'formula':
                formula = op.get('formula', '')
                
                if not formula:
                    continue
                    
                # Create a local copy with numeric columns only
                numeric_df = result_df.select_dtypes(include=[np.number])
                
                # Parse the formula and evaluate it
                # Note: This is using eval which can be dangerous if used with user input
                # in a real-world application, we should use a safer approach
                try:
                    result_df[output_col] = numeric_df.eval(formula)
                    logging.debug(f"Created derived column '{output_col}' using formula: {formula}")
                except Exception as e:
                    logging.warning(f"Failed to evaluate formula '{formula}': {str(e)}")
                    
            else:
                columns = op.get('columns', [])
                
                if not columns or len(columns) < 1:
                    continue
                    
                # Ensure all columns exist and are numeric
                valid_columns = [col for col in columns if col in result_df.columns]
                
                if not valid_columns:
                    continue
                    
                # Convert columns to numeric
                for col in valid_columns:
                    result_df[col] = pd.to_numeric(result_df[col], errors='coerce')
                
                # Apply the requested operation
                if operation == 'add':
                    result_df[output_col] = result_df[valid_columns].sum(axis=1)
                elif operation == 'subtract' and len(valid_columns) >= 2:
                    result_df[output_col] = result_df[valid_columns[0]] - result_df[valid_columns[1:]].sum(axis=1)
                elif operation == 'multiply':
                    result_df[output_col] = result_df[valid_columns].prod(axis=1)
                elif operation == 'divide' and len(valid_columns) >= 2:
                    # Avoid division by zero
                    denominator = result_df[valid_columns[1:]]
                    # Replace zeros with NaN to avoid division by zero
                    for col in denominator.columns:
                        denominator[col] = denominator[col].replace(0, np.nan)
                    # Calculate the product of all denominators
                    denom_product = denominator.prod(axis=1)
                    # Perform division
                    result_df[output_col] = result_df[valid_columns[0]] / denom_product
                
                logging.debug(f"Created derived column '{output_col}' using {operation} on {valid_columns}")
                
        except Exception as e:
            logging.error(f"Error creating derived column: {str(e)}")
    
    return result_df

def analyze_correlation(df: pd.DataFrame, columns: List[str], 
                        method: str = 'pearson') -> Tuple[pd.DataFrame, Dict[str, Dict[str, float]]]:
    """Calculate correlation coefficients between selected columns
    
    Args:
        df: The DataFrame containing the data
        columns: List of column names to analyze
        method: Correlation method ('pearson', 'spearman', or 'kendall')
        
    Returns:
        Tuple containing:
        - DataFrame with correlation matrix
        - Dictionary with top correlations for each column
    """
    # Filter to only include requested columns that exist and are numeric
    valid_columns = []
    for col in columns:
        if col in df.columns:
            # Convert to numeric if possible
            df[col] = pd.to_numeric(df[col], errors='coerce')
            if pd.api.types.is_numeric_dtype(df[col]):
                valid_columns.append(col)
    
    if len(valid_columns) < 2:
        return pd.DataFrame(), {}
        
    # Calculate correlation matrix
    corr_matrix = df[valid_columns].corr(method=method)
    
    # Identify top correlations for each column
    top_correlations = {}
    for col in valid_columns:
        # Get correlations for this column, sorted by absolute value
        col_corr = corr_matrix[col].drop(col)  # Drop self-correlation
        top_corrs = col_corr.abs().sort_values(ascending=False).head(3)
        
        # Store the actual correlation values, not the absolute ones
        top_correlations[col] = {
            other_col: round(float(corr_matrix.loc[col, other_col]), 3)
            for other_col in top_corrs.index
        }
    
    return corr_matrix, top_correlations

def detect_anomalies(df: pd.DataFrame, columns: List[str], 
                     methods: List[str] = ['zscore'], threshold: float = 3.0) -> Dict[str, List[int]]:
    """Detect anomalies in the data using statistical methods
    
    Args:
        df: The DataFrame containing the data
        columns: List of column names to analyze
        methods: List of detection methods ('zscore', 'iqr', 'isolation_forest')
        threshold: Threshold for anomaly detection
        
    Returns:
        Dictionary with column names as keys and lists of anomalous row indices as values
    """
    anomalies = {}
    
    for col in columns:
        if col not in df.columns or not pd.api.types.is_numeric_dtype(df[col]):
            continue
            
        # Convert column to numeric
        data = pd.to_numeric(df[col], errors='coerce')
        anomalous_indices = []
        
        for method in methods:
            if method.lower() == 'zscore':
                # Z-score method
                z_scores = np.abs(stats.zscore(data.dropna()))
                # Get indices where z-score exceeds threshold
                non_na_indices = data.dropna().index
                anomalous_indices.extend([idx for i, idx in enumerate(non_na_indices) if z_scores[i] > threshold])
                
            elif method.lower() == 'iqr':
                # IQR method
                q1 = np.percentile(data.dropna(), 25)
                q3 = np.percentile(data.dropna(), 75)
                iqr = q3 - q1
                
                lower_bound = q1 - threshold * iqr
                upper_bound = q3 + threshold * iqr
                
                # Get indices where values are outside the bounds
                anomalous_indices.extend(data[(data < lower_bound) | (data > upper_bound)].index.tolist())
                
            elif method.lower() == 'isolation_forest':
                # Isolation Forest method requires scikit-learn
                try:
                    from sklearn.ensemble import IsolationForest
                    
                    # Reshape data for isolation forest
                    X = data.dropna().values.reshape(-1, 1)
                    
                    if len(X) >= 10:  # Need enough samples
                        # Train isolation forest
                        iso_forest = IsolationForest(contamination=0.1, random_state=42)
                        anomalies_pred = iso_forest.fit_predict(X)
                        
                        # Get indices of anomalies (-1 indicates anomaly)
                        non_na_indices = data.dropna().index
                        anomalous_indices.extend([idx for i, idx in enumerate(non_na_indices) if anomalies_pred[i] == -1])
                except ImportError:
                    logging.warning("scikit-learn not available; skipping isolation forest method")
        
        # Remove duplicates and sort
        anomalies[col] = sorted(list(set(anomalous_indices)))
    
    return anomalies
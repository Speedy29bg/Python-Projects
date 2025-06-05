"""
Correlation Analysis Module

This module provides functions for analyzing correlations between data columns.


Author: Speedy29bg
"""

import pandas as pd
from typing import List, Dict, Tuple

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

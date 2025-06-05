"""
Transformations Module

This module provides functions for creating derived columns and data transformations.

Author: Lab Chart Tools Team
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Any

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
                numeric_df = pd.DataFrame()
                for col in df.columns:
                    numeric_df[col] = pd.to_numeric(df[col], errors='coerce')
                
                # Evaluate the formula using the pandas eval function
                # This allows expressions like 'col1 * 2 + col2'
                result_df[output_col] = pd.eval(formula, local_dict=numeric_df)
                
            else:
                columns = op.get('columns', [])
                
                if not columns or len(columns) < 1:
                    continue
                    
                # Convert columns to numeric
                numeric_values = {}
                for col in columns:
                    if col in df.columns:
                        numeric_values[col] = pd.to_numeric(df[col], errors='coerce')
                    else:
                        # Skip this operation if a column doesn't exist
                        continue
                        
                # Apply the operation
                if operation == 'add':
                    # Start with the first column
                    result = numeric_values[columns[0]].copy()
                    # Add subsequent columns
                    for col in columns[1:]:
                        result += numeric_values[col]
                        
                elif operation == 'subtract':
                    # Start with the first column
                    result = numeric_values[columns[0]].copy()
                    # Subtract subsequent columns
                    for col in columns[1:]:
                        result -= numeric_values[col]
                        
                elif operation == 'multiply':
                    # Start with the first column
                    result = numeric_values[columns[0]].copy()
                    # Multiply by subsequent columns
                    for col in columns[1:]:
                        result *= numeric_values[col]
                        
                elif operation == 'divide':
                    # Start with the first column
                    result = numeric_values[columns[0]].copy()
                    # Divide by subsequent columns
                    for col in columns[1:]:
                        # Avoid division by zero
                        result /= numeric_values[col].replace(0, np.nan)
                
                # Store the result
                result_df[output_col] = result
                
        except Exception as e:
            # Log the error and continue
            import logging
            logging.error(f"Error creating derived column {output_col}: {str(e)}")
    
    return result_df

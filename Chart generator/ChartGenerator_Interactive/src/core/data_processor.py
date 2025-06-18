#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Data processing utilities for the Interactive Chart Generator

Handles CSV file loading, data validation, and preprocessing.
"""

import pandas as pd
import numpy as np
import os
from typing import List, Dict, Optional, Tuple, Any
from utils.logger import get_logger

logger = get_logger()

class DataProcessor:
    """Handles data loading and processing operations"""
    
    def __init__(self):
        """Initialize the data processor"""
        self.data = None
        self.filename = None
        self.columns = []
        
    def load_csv_file(self, filepath: str) -> bool:
        """
        Load a CSV file
        
        Args:
            filepath: Path to the CSV file
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Validate file exists
            if not os.path.exists(filepath):
                logger.error(f"File not found: {filepath}")
                return False
            
            # Validate file extension
            if not filepath.lower().endswith('.csv'):
                logger.error(f"Invalid file type. Expected CSV file: {filepath}")
                return False
            
            # Load the CSV file
            logger.info(f"Loading CSV file: {filepath}")
            self.data = pd.read_csv(filepath)
            self.filename = os.path.basename(filepath)
            
            # Process column names
            self.columns = list(self.data.columns)
            
            # Validate data
            if self.data.empty:
                logger.warning("Loaded CSV file is empty")
                return False
            
            # Clean data
            self._clean_data()
            
            logger.info(f"Successfully loaded {len(self.data)} rows and {len(self.columns)} columns")
            logger.info(f"Columns: {self.columns}")
            
            return True
            
        except Exception as e:
            logger.error(f"Error loading CSV file: {e}")
            return False
    
    def _clean_data(self):
        """Clean and preprocess the loaded data"""
        if self.data is None:
            return
        
        # Convert numeric columns
        for col in self.data.columns:
            if self.data[col].dtype == 'object':
                # Try to convert to numeric
                numeric_data = pd.to_numeric(self.data[col], errors='coerce')
                if not numeric_data.isna().all():
                    self.data[col] = numeric_data
        
        # Log data info
        numeric_cols = self.data.select_dtypes(include=[np.number]).columns.tolist()
        text_cols = self.data.select_dtypes(include=['object']).columns.tolist()
        
        logger.info(f"Numeric columns: {numeric_cols}")
        if text_cols:
            logger.info(f"Text columns: {text_cols}")
    
    def get_columns(self) -> List[str]:
        """
        Get list of column names
        
        Returns:
            List[str]: Column names
        """
        return self.columns.copy() if self.columns else []
    
    def get_numeric_columns(self) -> List[str]:
        """
        Get list of numeric column names
        
        Returns:
            List[str]: Numeric column names
        """
        if self.data is None:
            return []
        
        return self.data.select_dtypes(include=[np.number]).columns.tolist()
    
    def get_column_data(self, column_name: str) -> Optional[pd.Series]:
        """
        Get data for a specific column
        
        Args:
            column_name: Name of the column
            
        Returns:
            pd.Series: Column data or None if not found
        """
        if self.data is None or column_name not in self.columns:
            return None
        
        return self.data[column_name]
    
    def get_data_stats(self, column_name: str) -> Dict[str, Any]:
        """
        Get statistics for a column
        
        Args:
            column_name: Name of the column
            
        Returns:
            Dict: Statistics dictionary
        """
        data = self.get_column_data(column_name)
        if data is None:
            return {}
        
        # Only calculate stats for numeric data
        if not pd.api.types.is_numeric_dtype(data):
            return {'count': len(data), 'type': 'non-numeric'}
        
        # Remove NaN values for calculations
        clean_data = data.dropna()
        
        if len(clean_data) == 0:
            return {'count': 0, 'type': 'numeric', 'all_nan': True}
        
        return {
            'count': len(clean_data),
            'mean': clean_data.mean(),
            'std': clean_data.std(),
            'min': clean_data.min(),
            'max': clean_data.max(),
            'median': clean_data.median(),
            'type': 'numeric'
        }
    
    def get_data_info(self) -> Dict[str, Any]:
        """
        Get general information about the loaded data
        
        Returns:
            Dict: Data information
        """
        if self.data is None:
            return {}
        
        return {
            'filename': self.filename,
            'rows': len(self.data),
            'columns': len(self.columns),
            'column_names': self.columns,
            'numeric_columns': self.get_numeric_columns(),
            'memory_usage': self.data.memory_usage(deep=True).sum()
        }
    
    def clear_data(self):
        """Clear the loaded data"""
        self.data = None
        self.filename = None
        self.columns = []

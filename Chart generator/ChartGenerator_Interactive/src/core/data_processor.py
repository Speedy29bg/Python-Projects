#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Data processing utilities for the Interactive Chart Generator

Handles CSV file loading, data validation, and preprocessing.
"""

import pandas as pd
import numpy as np
import os
import csv
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
        Load a CSV file with smart header detection
        
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
            
            # Smart header detection - look for non-empty cell in column E (index 4)
            logger.info(f"Loading CSV file with smart header detection: {filepath}")
            header_row_idx = self._detect_header_row(filepath)
            
            # Load the CSV file with detected header row
            if header_row_idx is not None:
                logger.info(f"Detected header row at index {header_row_idx} (line {header_row_idx + 1})")
                try:
                    self.data = pd.read_csv(filepath, encoding='utf-8', skiprows=header_row_idx, header=0)
                except UnicodeDecodeError:
                    logger.warning("UTF-8 encoding failed, trying latin1")
                    self.data = pd.read_csv(filepath, encoding='latin1', skiprows=header_row_idx, header=0)
            else:
                logger.warning("No header row detected, loading with default settings")
                try:
                    self.data = pd.read_csv(filepath, encoding='utf-8')
                except UnicodeDecodeError:
                    logger.warning("UTF-8 encoding failed, trying latin1")
                    self.data = pd.read_csv(filepath, encoding='latin1')
            
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
            logger.info(f"Headers: {self.columns}")
            logger.info(f"Data types: {dict(self.data.dtypes)}")
            
            return True
            
        except Exception as e:
            logger.error(f"Error loading CSV file: {e}")
            return False
    
    def _detect_header_row(self, filepath: str) -> Optional[int]:
        """
        Detect the header row by looking for non-empty cell in column E (index 4)
        
        Args:
            filepath: Path to the CSV file
            
        Returns:
            int or None: Index of the header row, or None if not found
        """
        try:
            with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
                reader = csv.reader(f)
                for i, row in enumerate(reader):
                    # Check if row has at least 5 columns and column E (index 4) is not empty
                    if len(row) > 4 and row[4].strip():
                        logger.info(f"Found non-empty cell in column E at row {i}")
                        return i
                        
            logger.warning("No non-empty cell found in column E")
            return None
            
        except Exception as e:
            logger.error(f"Error detecting header row: {e}")
            return None
    
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
    
    def get_chartable_columns(self) -> List[str]:
        """
        Get list of columns that can be used for charting (numeric + date/time)
        
        Returns:
            List[str]: Chartable column names
        """
        if self.data is None:
            return []
        
        chartable_cols = []
        
        for col in self.data.columns:
            # Include numeric columns
            if pd.api.types.is_numeric_dtype(self.data[col]):
                chartable_cols.append(col)
            # Include datetime columns
            elif pd.api.types.is_datetime64_any_dtype(self.data[col]):
                chartable_cols.append(col)
            # Include columns that can be converted to numeric
            elif self.data[col].dtype == 'object':
                # Try to convert a sample to see if it's numeric
                sample = self.data[col].dropna().head(10)
                if len(sample) > 0:
                    try:
                        pd.to_numeric(sample, errors='raise')
                        chartable_cols.append(col)
                    except (ValueError, TypeError):
                        # Check if it could be a date
                        try:
                            pd.to_datetime(sample, errors='raise')
                            chartable_cols.append(col)
                        except (ValueError, TypeError):
                            pass
        
        return chartable_cols
    
    def get_all_columns(self) -> List[str]:
        """
        Get all column names including text columns
        
        Returns:
            List[str]: All column names
        """
        return self.get_columns()
    
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
    
    def get_column_data_for_charting(self, column_name: str) -> Optional[pd.Series]:
        """
        Get data for a specific column, with automatic conversion for charting
        
        Args:
            column_name: Name of the column
            
        Returns:
            pd.Series: Column data converted for charting, or None if not possible
        """
        if self.data is None or column_name not in self.columns:
            return None
        
        column_data = self.data[column_name].copy()
        
        # If already numeric, return as-is
        if pd.api.types.is_numeric_dtype(column_data):
            return column_data
        
        # Try to convert to numeric
        try:
            numeric_data = pd.to_numeric(column_data, errors='coerce')
            if not numeric_data.isna().all():  # If at least some values could be converted
                logger.info(f"Converted column '{column_name}' to numeric for charting")
                return numeric_data
        except Exception:
            pass
        
        # Try to convert to datetime and then to numeric (timestamp)
        try:
            datetime_data = pd.to_datetime(column_data, errors='coerce')
            if not datetime_data.isna().all():
                logger.info(f"Converted column '{column_name}' to datetime for charting")
                return datetime_data
        except Exception:
            pass
        
        # If it's categorical, try to convert to numeric codes
        if column_data.dtype == 'object':
            try:
                # Create categorical codes
                categorical_data = pd.Categorical(column_data)
                logger.info(f"Converted column '{column_name}' to categorical codes for charting")
                return pd.Series(categorical_data.codes, index=column_data.index)
            except Exception:
                pass
        
        logger.warning(f"Could not convert column '{column_name}' to chartable format")
        return None
    
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

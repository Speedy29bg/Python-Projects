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
from typing import List, Dict, Optional, Tuple, Any, Union
from utils.logger import get_logger

logger = get_logger()

class DataFilter:
    """Class to handle data filtering operations"""
    
    def __init__(self):
        """Initialize data filter"""
        self.filters = {}
        self.sort_column = None
        self.sort_ascending = True
    
    def add_filter(self, column: str, filter_type: str, value: Any, value2: Any = None):
        """
        Add a filter for a specific column
        
        Args:
            column: Column name to filter
            filter_type: Type of filter ('equals', 'not_equals', 'contains', 'not_contains', 
                        'starts_with', 'ends_with', 'greater_than', 'less_than', 
                        'between', 'in_list', 'not_in_list', 'is_null', 'is_not_null')
            value: Filter value
            value2: Second value for 'between' filter
        """
        self.filters[column] = {
            'type': filter_type,
            'value': value,
            'value2': value2
        }
    
    def remove_filter(self, column: str):
        """Remove filter for a specific column"""
        if column in self.filters:
            del self.filters[column]
    
    def clear_filters(self):
        """Clear all filters"""
        self.filters.clear()
    
    def set_sort(self, column: str, ascending: bool = True):
        """Set sorting column and direction"""
        self.sort_column = column
        self.sort_ascending = ascending
    
    def apply_filters(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Apply all filters to the data
        
        Args:
            data: Original dataframe
            
        Returns:
            Filtered dataframe
        """
        filtered_data = data.copy()
        
        for column, filter_config in self.filters.items():
            if column not in filtered_data.columns:
                continue
                
            filter_type = filter_config['type']
            value = filter_config['value']
            value2 = filter_config['value2']
            
            try:
                if filter_type == 'equals':
                    filtered_data = filtered_data[filtered_data[column] == value]
                elif filter_type == 'not_equals':
                    filtered_data = filtered_data[filtered_data[column] != value]
                elif filter_type == 'contains':
                    filtered_data = filtered_data[filtered_data[column].astype(str).str.contains(str(value), na=False)]
                elif filter_type == 'not_contains':
                    filtered_data = filtered_data[~filtered_data[column].astype(str).str.contains(str(value), na=False)]
                elif filter_type == 'starts_with':
                    filtered_data = filtered_data[filtered_data[column].astype(str).str.startswith(str(value), na=False)]
                elif filter_type == 'ends_with':
                    filtered_data = filtered_data[filtered_data[column].astype(str).str.endswith(str(value), na=False)]
                elif filter_type == 'greater_than':
                    filtered_data = filtered_data[pd.to_numeric(filtered_data[column], errors='coerce') > float(value)]
                elif filter_type == 'less_than':
                    filtered_data = filtered_data[pd.to_numeric(filtered_data[column], errors='coerce') < float(value)]
                elif filter_type == 'greater_equal':
                    filtered_data = filtered_data[pd.to_numeric(filtered_data[column], errors='coerce') >= float(value)]
                elif filter_type == 'less_equal':
                    filtered_data = filtered_data[pd.to_numeric(filtered_data[column], errors='coerce') <= float(value)]
                elif filter_type == 'between':
                    if value2 is not None:
                        numeric_col = pd.to_numeric(filtered_data[column], errors='coerce')
                        filtered_data = filtered_data[(numeric_col >= float(value)) & (numeric_col <= float(value2))]
                elif filter_type == 'in_list':
                    if isinstance(value, (list, tuple)):
                        filtered_data = filtered_data[filtered_data[column].isin(value)]
                elif filter_type == 'not_in_list':
                    if isinstance(value, (list, tuple)):
                        filtered_data = filtered_data[~filtered_data[column].isin(value)]
                elif filter_type == 'is_null':
                    filtered_data = filtered_data[filtered_data[column].isna()]
                elif filter_type == 'is_not_null':
                    filtered_data = filtered_data[filtered_data[column].notna()]
                    
            except Exception as e:
                logger.warning(f"Error applying filter {filter_type} to column {column}: {e}")
                continue
        
        # Apply sorting
        if self.sort_column and self.sort_column in filtered_data.columns:
            try:
                filtered_data = filtered_data.sort_values(
                    by=self.sort_column, 
                    ascending=self.sort_ascending, 
                    na_position='last'
                )
            except Exception as e:
                logger.warning(f"Error sorting by column {self.sort_column}: {e}")
        
        return filtered_data

class DataProcessor:
    """Handles data loading and processing operations"""
    
    def __init__(self):
        """Initialize the data processor"""
        self.data = None
        self.original_data = None  # Keep original data for filtering
        self.filename = None
        self.columns = []
        self.data_filter = DataFilter()  # Excel-like filtering
        
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
            
            # Store original data for filtering
            self.original_data = self.data.copy()
            
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
    
    # Excel-like filtering methods
    def add_filter(self, column: str, filter_type: str, value: Any, value2: Any = None) -> bool:
        """
        Add a filter for a specific column
        
        Args:
            column: Column name to filter
            filter_type: Type of filter
            value: Filter value
            value2: Second value for 'between' filter
            
        Returns:
            bool: True if filter was added successfully        """
        if self.original_data is None:
            logger.warning("No data loaded, cannot add filter")
            return False
            
        if column not in self.columns:
            logger.warning(f"Column '{column}' not found in data")
            return False
        
        self.data_filter.add_filter(column, filter_type, value, value2)
        self._apply_filters()
        return True
    
    def remove_filter(self, column: str) -> bool:
        """
        Remove filter for a specific column
        
        Args:
            column: Column name
            
        Returns:
            bool: True if filter was removed        """
        if self.original_data is None:
            return False
            
        self.data_filter.remove_filter(column)
        self._apply_filters()
        return True
    
    def clear_filters(self) -> bool:
        """
        Clear all filters and restore original data
        
        Returns:
            bool: True if filters were cleared
        """
        if self.original_data is None:
            return False
            
        self.data_filter.clear_filters()
        self.data = self.original_data.copy()
        logger.info("All filters cleared, data restored to original")
        return True
    
    def set_sort(self, column: str, ascending: bool = True) -> bool:
        """
        Set sorting for data
        
        Args:
            column: Column to sort by
            ascending: Sort direction
            
        Returns:
            bool: True if sort was applied
        """
        if self.original_data is None:
            return False
            
        if column not in self.columns:
            logger.warning(f"Column '{column}' not found in data")
            return False
        
        self.data_filter.set_sort(column, ascending)
        self._apply_filters()
        return True
    
    def get_filter_info(self) -> Dict[str, Any]:
        """
        Get information about current filters
        
        Returns:
            Dict: Filter information
        """
        if self.original_data is None:
            return {}
            
        return {
            'filters': self.data_filter.filters.copy(),
            'sort_column': self.data_filter.sort_column,
            'sort_ascending': self.data_filter.sort_ascending,
            'original_rows': len(self.original_data),
            'filtered_rows': len(self.data) if self.data is not None else 0,
            'filter_applied': len(self.data_filter.filters) > 0 or self.data_filter.sort_column is not None
        }
    
    def get_unique_values(self, column: str, limit: int = 100) -> List[Any]:
        """
        Get unique values for a column (for filter dropdowns)
        
        Args:
            column: Column name
            limit: Maximum number of unique values to return
            
        Returns:
            List of unique values
        """
        if self.original_data is None or column not in self.columns:
            return []
        
        try:
            unique_vals = self.original_data[column].dropna().unique()
            # Sort values if possible
            try:
                unique_vals = sorted(unique_vals)
            except:
                pass  # Can't sort mixed types
                
            return list(unique_vals[:limit])
        except Exception as e:
            logger.warning(f"Error getting unique values for column {column}: {e}")
            return []
    
    def get_column_stats_for_filter(self, column: str) -> Dict[str, Any]:
        """
        Get column statistics for filter UI
        
        Args:
            column: Column name
            
        Returns:
            Dict with column statistics
        """
        if self.original_data is None or column not in self.columns:
            return {}
        
        try:
            col_data = self.original_data[column]
            stats = {
                'name': column,
                'type': str(col_data.dtype),
                'non_null_count': col_data.count(),
                'null_count': col_data.isna().sum(),
                'unique_count': col_data.nunique(),
                'is_numeric': pd.api.types.is_numeric_dtype(col_data)
            }
            
            if stats['is_numeric']:
                numeric_data = pd.to_numeric(col_data, errors='coerce').dropna()
                if len(numeric_data) > 0:
                    stats.update({
                        'min': numeric_data.min(),
                        'max': numeric_data.max(),
                        'mean': numeric_data.mean(),
                        'median': numeric_data.median()
                    })
            
            return stats
        except Exception as e:
            logger.warning(f"Error getting column stats for {column}: {e}")
            return {}
    
    def _apply_filters(self):
        """Apply current filters to the data"""
        if self.original_data is None:
            return
            
        try:
            self.data = self.data_filter.apply_filters(self.original_data)
            logger.info(f"Filters applied: {len(self.original_data)} -> {len(self.data)} rows")
        except Exception as e:
            logger.error(f"Error applying filters: {e}")
            self.data = self.original_data.copy()

    def clear_data(self):
        """Clear the loaded data"""
        self.data = None
        self.original_data = None
        self.filename = None

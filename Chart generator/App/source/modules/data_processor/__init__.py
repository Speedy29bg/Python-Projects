"""
Data Processor Package

This package provides functions for processing CSV data files in the Chart Generator application.
"""

from modules.data_processor.header_detection import detect_header_row
from modules.data_processor.csv_reader import read_csv_file
from modules.data_processor.data_scaling import process_data_for_scaling
from modules.data_processor.utils import create_safe_sheet_name

__all__ = [
    'detect_header_row',
    'read_csv_file',
    'process_data_for_scaling',
    'create_safe_sheet_name'
]

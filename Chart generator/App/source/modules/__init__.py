"""
Package initialization file for the Chart Generator modules package

This file ensures that all modules and subpackages are properly imported
and accessible from the top level of the application.

Author: Lab Chart Tools Team
"""

# Import subpackages
from modules import ui
from modules import core
from modules import data
from modules import utils
from modules import data_processor
from modules import chart_generator_module
from modules import data_analysis_module
from modules import export_module
from modules import logger_module
from modules import ui_components_module

# Import commonly used modules directly
from modules.logger import setup_logging, handle_exception
from modules.chart_generator import create_preview_plot, clear_figure, create_tkinter_canvas
from modules.data_processor import detect_header_row, read_csv_file, process_data_for_scaling, create_safe_sheet_name
from modules.excel_export import generate_excel_workbook, export_figure
from modules.data_analysis import calculate_statistics, filter_outliers, smooth_data, analyze_correlation
from modules.ui_components import create_loading_indicator, create_progress_dialog, create_data_preview

__all__ = [
    # Subpackages
    'ui', 'core', 'data', 'utils', 'data_processor', 'chart_generator_module', 
    'data_analysis_module', 'export_module', 'logger_module', 'ui_components_module',
    
    # Logger functions
    'setup_logging', 'handle_exception',
    
    # Chart generator functions
    'create_preview_plot', 'clear_figure', 'create_tkinter_canvas',
    
    # Data processor functions
    'detect_header_row', 'read_csv_file', 'process_data_for_scaling', 'create_safe_sheet_name',
    
    # Export functions
    'generate_excel_workbook', 'export_figure',
    
    # Data analysis functions
    'calculate_statistics', 'filter_outliers', 'smooth_data', 'analyze_correlation',
    
    # UI components
    'create_loading_indicator', 'create_progress_dialog', 'create_data_preview'
]

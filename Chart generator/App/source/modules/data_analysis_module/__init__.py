"""
Data Analysis Module

This package provides data analysis functionality for the Chart Generator application.
"""

from modules.data_analysis_module.statistics import calculate_statistics
from modules.data_analysis_module.filtering import filter_outliers, detect_anomalies
from modules.data_analysis_module.smoothing import smooth_data
from modules.data_analysis_module.correlation import analyze_correlation
from modules.data_analysis_module.transformations import calculate_derived_columns

__all__ = [
    'calculate_statistics',
    'filter_outliers',
    'detect_anomalies',
    'smooth_data',
    'analyze_correlation',
    'calculate_derived_columns'
]

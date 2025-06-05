"""
Chart generator utility functions for the Lab Chart Generator

This module provides helper functions for chart customization and formatting
that supplement the main chart generation functionality.

Author: Lab Chart Tools Team
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib import cm
import logging
from typing import Dict, List, Tuple, Optional, Any, Union

def apply_color_scheme(ax, color_scheme='default', num_series=1):
    """Apply a color scheme to a plot
    
    Args:
        ax: The matplotlib axis object
        color_scheme: Name of a matplotlib colormap
        num_series: Number of series to generate colors for
        
    Returns:
        list: List of generated colors
    """
    try:
        if color_scheme == 'default' or not hasattr(cm, color_scheme):
            return None
            
        # Get the colormap
        colormap = getattr(cm, color_scheme)
        
        # Generate evenly spaced colors
        colors = [colormap(i) for i in np.linspace(0, 0.9, num_series)]
        
        return colors
    except Exception as e:
        logging.warning(f"Failed to apply color scheme: {str(e)}")
        return None

def format_datetime_axis(ax, datetime_mapping, rotate=True):
    """Format an axis that represents datetime values
    
    Args:
        ax: The matplotlib axis object
        datetime_mapping: Dictionary mapping numeric timestamps to formatted strings
        rotate: Whether to rotate date labels for better readability
    """
    from matplotlib.ticker import FuncFormatter
    
    def format_fn(x, pos):
        try:
            int_x = int(x)
            if int_x in datetime_mapping:
                return datetime_mapping[int_x]
            return str(int_x)
        except:
            return str(x)
            
    formatter = FuncFormatter(format_fn)
    ax.xaxis.set_major_formatter(formatter)
    
    if rotate:
        plt.gcf().autofmt_xdate()  # Rotate date labels

def auto_format_y_axis(ax, values, is_log=False):
    """Automatically format a Y-axis based on data values
    
    Args:
        ax: The matplotlib axis object
        values: Array-like of values to be plotted on this axis
        is_log: Whether the axis is using log scale
    """
    from matplotlib.ticker import ScalarFormatter, LogFormatter
    
    if is_log:
        formatter = LogFormatter(labelOnlyBase=False)
        ax.yaxis.set_major_formatter(formatter)
    else:
        formatter = ScalarFormatter(useOffset=False)
        ax.yaxis.set_major_formatter(formatter)
        
    # Limit precision for very small or large numbers
    max_abs = max(abs(np.nanmin(values)), abs(np.nanmax(values)))
    if max_abs < 0.01 or max_abs > 1000:
        ax.ticklabel_format(style='sci', axis='y', scilimits=(-2, 3))

def add_chart_annotations(fig, chart_info=None):
    """Add annotations to a chart
    
    Args:
        fig: The matplotlib figure object
        chart_info: Dictionary with annotation information
    """
    if not chart_info:
        return
        
    # Add title if provided
    if 'title' in chart_info:
        plt.title(chart_info['title'])
        
    # Add text annotations
    if 'annotations' in chart_info:
        for ann in chart_info['annotations']:
            plt.annotate(
                ann['text'],
                xy=(ann['x'], ann['y']),
                xytext=(ann.get('xt', ann['x']), ann.get('yt', ann['y'])),
                arrowprops=ann.get('arrow_props', None)
            )
            
    # Add figure watermark or footnote
    if 'footnote' in chart_info:
        plt.figtext(
            0.5, 0.01,
            chart_info['footnote'],
            ha='center',
            fontsize=8,
            style='italic'
        )

def detect_series_type(df, column_name):
    """Detect the appropriate chart type for a data series
    
    Args:
        df: Pandas DataFrame containing the data
        column_name: Name of the column to analyze
        
    Returns:
        str: Suggested chart type ('line', 'scatter', or 'bar')
    """
    if column_name not in df.columns:
        return 'line'  # Default
        
    # Get the series
    series = df[column_name]
    
    # Check for categorical data (suggesting bar chart)
    if pd.api.types.is_categorical_dtype(series) or pd.api.types.is_object_dtype(series):
        return 'bar'
        
    # Check for very few unique values (suggesting bar chart)
    if len(series.unique()) < 10:
        return 'bar'
    
    # Check for non-continuous data (suggesting scatter)
    if not pd.api.types.is_numeric_dtype(series):
        return 'scatter'
        
    # Check value spacing
    if len(series) > 1:
        # If data is not uniformly spaced, suggest scatter
        try:
            values = series.dropna().sort_values()
            if len(values) > 1:
                diffs = np.diff(values)
                std_diff = np.std(diffs)
                mean_diff = np.mean(diffs)
                if std_diff > mean_diff * 0.5:  # High variance in differences
                    return 'scatter'
        except:
            pass
            
    # Default to line chart
    return 'line'
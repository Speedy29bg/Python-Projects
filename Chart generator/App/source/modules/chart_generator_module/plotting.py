"""
Plotting Module

This module provides functions for creating and configuring plots.

Author: Lab Chart Tools Team
"""

import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import numpy as np
import pandas as pd
import logging
from typing import List, Dict, Tuple, Optional, Any, Union
import re

def create_preview_plot(df, x_axis, y_axes, secondary_axes, chart_settings, original_df=None):
    """Create and return a preview plot based on the data and settings
    
    Args:
        df: The processed pandas DataFrame containing the data to plot
        x_axis: The name of the X-axis column
        y_axes: List of primary Y-axis column names
        secondary_axes: List of secondary Y-axis column names
        chart_settings: Dictionary containing plot configuration settings
        original_df: Optional original DataFrame for datetime mapping
        
    Returns:
        tuple: (matplotlib.figure.Figure, dict) - The figure object and info/error dictionary
    """
    # Dictionary to store information about the chart or errors
    chart_info = {}
    
    # First, ensure we have data to plot
    if df.empty:
        chart_info['error'] = "No data available for plotting"
        return None, chart_info
    
    # Debug information
    logging.debug(f"DataFrame info for plotting:")
    logging.debug(f"- Shape: {df.shape}")
    logging.debug(f"- Columns: {df.columns.tolist()}")
    logging.debug(f"- Data types: {df.dtypes}")
    logging.debug(f"- X-axis column '{x_axis}' has {df[x_axis].count()} non-null values")
    for y_col in y_axes + secondary_axes:
        logging.debug(f"- Column '{y_col}' has {df[y_col].count()} non-null values")
    
    # Check if X-axis might be a datetime column in the original data
    x_is_datetime = False
    datetime_string_map = None
    
    # If original dataframe is provided, check for datetime
    if original_df is not None and x_axis in original_df.columns:
        # Check a sample of values for datetime format
        sample = original_df[x_axis].dropna().head(20).astype(str)
        date_patterns = [
            r'\d{1,2}/\d{1,2}/\d{2,4}\s+\d{1,2}:\d{1,2}:\d{1,2}\s*(?:AM|PM)?',  # 1/16/2024 4:44:01 PM
            r'\d{1,2}-\d{1,2}-\d{2,4}\s+\d{1,2}:\d{1,2}:\d{1,2}',  # 16-01-2024 16:44:01
            r'\d{4}-\d{1,2}-\d{1,2}\s+\d{1,2}:\d{1,2}:\d{1,2}',  # 2024-01-16 16:44:01
            r'\d{1,2}/\d{1,2}/\d{2,4}'  # 1/16/2024
        ]
        
        for pattern in date_patterns:
            matches = sample.str.match(pattern).sum()
            if matches > len(sample) * 0.5:  # If more than 50% match
                x_is_datetime = True
                logging.debug(f"X-axis '{x_axis}' detected as datetime")
                
                # Convert original values to datetime objects and create string mapping
                try:
                    original_datetime_values = pd.to_datetime(original_df[x_axis], errors='coerce')
                    
                    # Round timestamps to nearest 15 minutes for display
                    rounded_times = original_datetime_values.dt.floor('15min')
                    
                    # Create string formatted dates for x-axis values
                    time_strings = rounded_times.dt.strftime('%m/%d/%Y %H:%M')
                    
                    # Create a mapping from original timestamps to rounded string values
                    unix_timestamps = original_datetime_values.astype('int64') // 10**9
                    datetime_string_map = dict(zip(unix_timestamps, time_strings))
                    
                    logging.debug(f"Created datetime string mapping with {len(datetime_string_map)} entries")
                except Exception as e:
                    logging.warning(f"Error creating datetime mapping: {str(e)}")
                
                break
    
    # Create a copy of the dataframe for plotting
    plot_df = df.copy()
    
    # Ensure data is numeric for plotting
    try:
        # Convert X-axis
        if not pd.api.types.is_numeric_dtype(plot_df[x_axis]):
            plot_df[x_axis] = pd.to_numeric(plot_df[x_axis], errors='coerce')
            
        # Convert Y-axes columns
        for col in y_axes + secondary_axes:
            if not pd.api.types.is_numeric_dtype(plot_df[col]):
                plot_df[col] = pd.to_numeric(plot_df[col], errors='coerce')
    except Exception as e:
        chart_info['error'] = f"Error converting data to numeric: {str(e)}"
        return None, chart_info
    
    # Get settings values
    log_scale_x = chart_settings.get('log_scale_x', False)
    log_scale_y1 = chart_settings.get('log_scale_y1', False)
    log_scale_y2 = chart_settings.get('log_scale_y2', False)
    auto_scale = chart_settings.get('auto_scale', True)
    chart_type = chart_settings.get('chart_type', 'line')
    color_scheme = chart_settings.get('color_scheme', 'default')
    
    # Create a new figure with two subplots sharing x axis
    use_secondary_axis = len(secondary_axes) > 0
    
    # Create the figure with appropriate height based on complexity
    fig_height = 6 if len(y_axes) + len(secondary_axes) < 5 else 8
    fig = plt.figure(figsize=(10, fig_height), dpi=100)
    ax1 = fig.add_subplot(111)
    
    # Initialize second y-axis if needed
    ax2 = None
    if use_secondary_axis:
        ax2 = ax1.twinx()
    
    # Set up colormap based on selected scheme
    if color_scheme != 'default':
        color_map = plt.get_cmap(color_scheme)
        primary_colors = [color_map(i/len(y_axes)) for i in range(len(y_axes))]
        secondary_colors = [color_map(i/len(secondary_axes)) if len(secondary_axes) > 0 else 'red' 
                          for i in range(len(secondary_axes))]
    else:
        # Default color cycle
        primary_colors = [f'C{i}' for i in range(len(y_axes))]
        # Use a different color cycle for secondary axis
        secondary_colors = [f'C{i+len(y_axes)}' for i in range(len(secondary_axes))]
    
    # Plot lines/points on primary y-axis
    for i, y_col in enumerate(y_axes):
        if chart_type == 'line':
            ax1.plot(plot_df[x_axis], plot_df[y_col], marker='.', linestyle='-', label=y_col, 
                    color=primary_colors[i], alpha=0.8)
        else:  # scatter
            ax1.scatter(plot_df[x_axis], plot_df[y_col], marker='o', s=20, label=y_col, 
                       color=primary_colors[i], alpha=0.7)
    
    # Plot lines/points on secondary y-axis if needed
    if use_secondary_axis and ax2 is not None:
        for i, y_col in enumerate(secondary_axes):
            if chart_type == 'line':
                ax2.plot(plot_df[x_axis], plot_df[y_col], marker='.', linestyle='--', label=y_col, 
                        color=secondary_colors[i], alpha=0.8)
            else:  # scatter
                ax2.scatter(plot_df[x_axis], plot_df[y_col], marker='s', s=20, label=y_col, 
                           color=secondary_colors[i], alpha=0.7)
    
    # Set log scale if selected
    if log_scale_x:
        ax1.set_xscale('log')
    if log_scale_y1:
        ax1.set_yscale('log')
    if log_scale_y2 and use_secondary_axis and ax2 is not None:
        ax2.set_yscale('log')
    
    # Set custom limits if auto-scale is disabled
    if not auto_scale:
        # X-axis limits
        if chart_settings.get('x_min') and chart_settings.get('x_max'):
            try:
                x_min = float(chart_settings.get('x_min'))
                x_max = float(chart_settings.get('x_max'))
                if x_min < x_max:
                    ax1.set_xlim(x_min, x_max)
            except (ValueError, TypeError):
                logging.warning("Invalid X-axis range values")
        
        # Primary Y-axis limits
        if chart_settings.get('y1_min') and chart_settings.get('y1_max'):
            try:
                y1_min = float(chart_settings.get('y1_min'))
                y1_max = float(chart_settings.get('y1_max'))
                if y1_min < y1_max:
                    ax1.set_ylim(y1_min, y1_max)
            except (ValueError, TypeError):
                logging.warning("Invalid Primary Y-axis range values")
        
        # Secondary Y-axis limits
        if chart_settings.get('y2_min') and chart_settings.get('y2_max') and use_secondary_axis and ax2 is not None:
            try:
                y2_min = float(chart_settings.get('y2_min'))
                y2_max = float(chart_settings.get('y2_max'))
                if y2_min < y2_max:
                    ax2.set_ylim(y2_min, y2_max)
            except (ValueError, TypeError):
                logging.warning("Invalid Secondary Y-axis range values")
    
    # Set labels
    ax1.set_xlabel(x_axis)
    ax1.set_ylabel(", ".join(y_axes) if y_axes else "")
    if use_secondary_axis and ax2 is not None:
        ax2.set_ylabel(", ".join(secondary_axes))
    
    # Add legends
    ax1.legend(loc='upper left')
    if use_secondary_axis and ax2 is not None:
        ax2.legend(loc='upper right')
    
    # Set grid
    ax1.grid(True, alpha=0.3)
    
    # Custom X-axis formatter for datetime values
    if x_is_datetime and datetime_string_map:
        def format_date(x, pos):
            if x in datetime_string_map:
                return datetime_string_map[x]
            return str(x)
        
        ax1.xaxis.set_major_formatter(FuncFormatter(format_date))
        plt.xticks(rotation=45)
    
    # Adjust layout to prevent clipping of date labels
    plt.tight_layout()
    
    # Return the figure and info
    chart_info['info'] = f"Created chart with {len(y_axes)} primary and {len(secondary_axes)} secondary data series"
    return fig, chart_info

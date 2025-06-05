"""
Worksheet Utilities Module

This module provides functions for manipulating Excel worksheets.

Author: Lab Chart Tools Team
"""

from openpyxl.chart import LineChart, Reference, ScatterChart, Series
from openpyxl.chart.axis import ChartLines
import pandas as pd
import logging
from typing import List

def populate_worksheet(ws, df, x_axis, y_axes, secondary_axes):
    """Populate worksheet with data
    
    Args:
        ws: The openpyxl worksheet object
        df: The pandas DataFrame containing source data
        x_axis: The name of the X-axis column
        y_axes: List of primary Y-axis column names
        secondary_axes: List of secondary Y-axis column names
    """
    all_axes = [x_axis] + y_axes + secondary_axes
    
    # Write headers
    for col_idx, axis in enumerate(all_axes, start=1):
        ws.cell(row=1, column=col_idx, value=axis)
    
    # Write data - use numeric index to avoid issues with DataFrame index
    for idx, (_, row) in enumerate(df.iterrows(), start=0):
        for col_idx, axis in enumerate(all_axes, start=1):
            # Handle NaN values
            value = row[axis]
            if pd.isna(value):
                value = None
            ws.cell(row=idx+2, column=col_idx, value=value)
    
    logging.debug(f"Populated worksheet with {len(df)} rows and {len(all_axes)} columns")

def add_line_chart_to_worksheet(ws, df, x_axis, y_axes, secondary_axes):
    """Add a line chart to the worksheet
    
    Args:
        ws: The openpyxl worksheet object
        df: The pandas DataFrame containing source data
        x_axis: The name of the X-axis column
        y_axes: List of primary Y-axis column names
        secondary_axes: List of secondary Y-axis column names
    """
    chart = LineChart()
    chart.title = f"Line Chart: {', '.join(y_axes)} vs {x_axis}"
    chart.x_axis.title = x_axis
    chart.y_axis.title = "Primary Y-Axes"
    
    # Add primary Y-axis data
    if y_axes:
        x_col = 1  # First column is X-axis
        data_rows = len(df) + 1  # +1 for header row
        
        # X-axis reference
        x_ref = Reference(ws, min_col=x_col, min_row=1, max_row=data_rows)
        
        # Add each Y-axis series
        for i, y_axis in enumerate(y_axes, start=2):
            y_ref = Reference(ws, min_col=i, min_row=1, max_row=data_rows)
            series = Series(y_ref, x_ref, title_from_data=True)
            chart.series.append(series)
            
    # Add secondary Y-axis if needed
    if secondary_axes:
        # Create second Y-axis
        chart.y_axis.majorGridlines = ChartLines()
        chart.y_axis.title = "Primary Y-Axes"
        
        # Add secondary axis
        chart.y_axis.crosses = 'max'
        
        # Start column index after the primary y-axes
        start_col = 2 + len(y_axes)
        
        # Add each secondary Y-axis series
        for i, y_axis in enumerate(secondary_axes, start=start_col):
            y_ref = Reference(ws, min_col=i, min_row=1, max_row=data_rows)
            series = Series(y_ref, x_ref, title_from_data=True)
            chart.series.append(series)
            series.axId = 200  # This assigns the series to the secondary axis
          # Add chart to worksheet
    ws.add_chart(chart, "A10")  # Position the chart below the data
    logging.debug("Added line chart to worksheet")
    
def add_scatter_chart_to_worksheet(ws, df, x_axis, y_axes, secondary_axes):
    """Add a scatter chart to the worksheet
    
    Args:
        ws: The openpyxl worksheet object
        df: The pandas DataFrame containing source data
        x_axis: The name of the X-axis column
        y_axes: List of primary Y-axis column names
        secondary_axes: List of secondary Y-axis column names
    """
    chart = ScatterChart()
    chart.title = f"Scatter Chart: {', '.join(y_axes)} vs {x_axis}"
    chart.x_axis.title = x_axis
    chart.y_axis.title = "Y-Axes"
    
    # Get data row count
    data_rows = len(df) + 1  # +1 for header
    
    # Add primary Y-axis data
    if y_axes:
        x_col = 1  # First column is X-axis
        
        # X-axis reference
        x_ref = Reference(ws, min_col=x_col, min_row=1, max_row=data_rows)
        
        # Add each Y-axis series
        for i, y_axis in enumerate(y_axes, start=2):
            y_ref = Reference(ws, min_col=i, min_row=1, max_row=data_rows)
            series = Series(y_ref, x_ref, title_from_data=True)
            chart.series.append(series)
    
    # Add secondary Y-axis if needed
    if secondary_axes:
        # Create second Y-axis
        chart.y_axis.majorGridlines = ChartLines()
        chart.y_axis.title = "Primary Y-Axes"
        
        # Add secondary axis
        chart.y_axis.crosses = 'max'
        
        # Start column index after the primary y-axes
        start_col = 2 + len(y_axes)
        
        # Add each secondary Y-axis series
        for i, y_axis in enumerate(secondary_axes, start=start_col):
            y_ref = Reference(ws, min_col=i, min_row=1, max_row=data_rows)
            series = Series(y_ref, x_ref, title_from_data=True)
            chart.series.append(series)
            series.axId = 200  # This assigns the series to the secondary axis
    
    # Add chart to worksheet
    ws.add_chart(chart, "A10")  # Position the chart below the data
    logging.debug("Added scatter chart to worksheet")

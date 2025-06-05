import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.ticker import FuncFormatter
import numpy as np
import pandas as pd
import logging
from typing import List, Dict, Tuple, Optional, Any, Union

def clear_figure(figure, canvas):
    """Clear the existing figure and canvas
    
    Args:
        figure: The matplotlib figure object
        canvas: The Tkinter canvas widget
        
    Returns:
        tuple: (None, None) representing cleared figure and canvas
    """
    if canvas:
        canvas.get_tk_widget().pack_forget()
    
    if figure:
        plt.close(figure)
    
    return None, None

def create_tkinter_canvas(figure, frame):
    """Create a Tkinter canvas from a matplotlib figure with interactive features
    
    Args:
        figure: The matplotlib figure object
        frame: The Tkinter frame to place the canvas in
        
    Returns:
        FigureCanvasTkAgg: The Tkinter canvas widget
    """
    import tkinter as tk
    from tkinter import ttk
    from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
    import matplotlib.pyplot as plt
    
    # Clear frame first to avoid stacking multiple charts
    for widget in frame.winfo_children():
        widget.destroy()
    
    # Create main frame for the chart and controls
    chart_frame = ttk.Frame(frame)
    chart_frame.pack(fill='both', expand=True)
    
    # Create chart area
    canvas = FigureCanvasTkAgg(figure, master=chart_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill='both', expand=True)
    
    # Add matplotlib's built-in navigation toolbar for zoom, pan, etc.
    toolbar_frame = ttk.Frame(chart_frame)
    toolbar_frame.pack(fill='x', pady=2)
    toolbar = NavigationToolbar2Tk(canvas, toolbar_frame)
    toolbar.update()
    
    # Create frame for custom buttons
    button_frame = ttk.Frame(chart_frame)
    button_frame.pack(fill='x', pady=5)
    
    # Grid toggle button
    grid_var = tk.BooleanVar(value=True)  # Default grid on
    
    def toggle_grid():
        for ax in figure.get_axes():
            ax.grid(grid_var.get())
        canvas.draw()
    
    grid_btn = ttk.Checkbutton(button_frame, text="Grid Lines", variable=grid_var, 
                             command=toggle_grid)
    grid_btn.pack(side='left', padx=5)
    
    # Toggle data points
    points_var = tk.BooleanVar(value=True)  # Default points visible
    
    def toggle_points():
        for ax in figure.get_axes():
            for line in ax.get_lines():
                line.set_marker('.' if points_var.get() else '')
        canvas.draw()
    
    points_btn = ttk.Checkbutton(button_frame, text="Show Data Points", variable=points_var, 
                               command=toggle_points)
    points_btn.pack(side='left', padx=5)
    
    # Toggle legend
    legend_var = tk.BooleanVar(value=True)  # Default legend visible
    
    def toggle_legend():
        for ax in figure.get_axes():
            legend = ax.get_legend()
            if legend:
                legend.set_visible(legend_var.get())
        canvas.draw()
    
    legend_btn = ttk.Checkbutton(button_frame, text="Show Legend", variable=legend_var, 
                               command=toggle_legend)
    legend_btn.pack(side='left', padx=5)
    
    # Toggle automatic updates
    autoupdate_var = tk.BooleanVar(value=True)
    autoupdate_btn = ttk.Checkbutton(button_frame, text="Auto-update", variable=autoupdate_var)
    autoupdate_btn.pack(side='left', padx=5)
    
    # Get autoupdate status
    canvas.autoupdate = lambda: autoupdate_var.get()
    
    # Set a reasonable height for the frame
    frame.config(height=450)  # Increased height to accommodate buttons
    
    return canvas

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
        logging.warning(f"Error during numeric conversion: {str(e)}")
    
    # Remove rows with NaN in the x-axis
    plot_df = plot_df.dropna(subset=[x_axis])
    if plot_df.empty:
        chart_info['error'] = f"No valid numeric data for X-axis '{x_axis}'"
        return None, chart_info

    # Create figure
    figure, ax = plt.subplots(figsize=(10, 6))
    
    # Set log scales if selected
    if chart_settings.get('log_scale_x', False):
        ax.set_xscale('log')
    if chart_settings.get('log_scale_y1', False):
        ax.set_yscale('log')
    
    # Set manual axis limits if not auto-scaling
    if not chart_settings.get('auto_scale', True):
        try:
            # X-axis limits
            x_min, x_max = chart_settings.get('x_min'), chart_settings.get('x_max')
            if x_min and x_max:
                ax.set_xlim(float(x_min), float(x_max))
            
            # Primary Y-axis limits
            y1_min, y1_max = chart_settings.get('y1_min'), chart_settings.get('y1_max')
            if y1_min and y1_max:
                ax.set_ylim(float(y1_min), float(y1_max))
        except ValueError:
            logging.warning("Invalid numeric values in range fields")
    
    # Plot based on chart type
    is_scatter = chart_settings.get('chart_type') == "scatter"
    has_valid_data = False
    
    # Set color scheme if specified
    color_scheme = chart_settings.get('color_scheme', 'default')
    if color_scheme != 'default':
        try:
            plt.style.use(color_scheme)
        except Exception as e:
            logging.warning(f"Failed to set color scheme {color_scheme}: {str(e)}")
    
    # Plot primary Y-axes
    for y_axis in y_axes:
        # Get valid data points for this series (both x and y must be valid)
        series_df = plot_df[[x_axis, y_axis]].dropna()
        if len(series_df) == 0:
            logging.warning(f"No valid data points for {y_axis} vs {x_axis}")
            continue
            
        logging.debug(f"Plotting {y_axis} vs {x_axis}: {len(series_df)} points")
        has_valid_data = True
        
        if is_scatter:
            ax.scatter(series_df[x_axis], series_df[y_axis], label=y_axis, alpha=0.7)
        else:
            ax.plot(series_df[x_axis], series_df[y_axis], label=y_axis)
    
    # Set labels
    ax.set_xlabel(x_axis)
    y1_label = "Primary Y-Axes" if len(y_axes) > 1 else y_axes[0] if y_axes else ""
    if chart_settings.get('normalize_data', False) and y1_label:
        y1_label += " (Normalized)"
    ax.set_ylabel(y1_label)
    
    # Add grid
    ax.grid(True, linestyle='--', alpha=0.7)
    
    # Plot secondary Y-axes if selected
    if secondary_axes:
        ax2 = ax.twinx()
        
        # Set log scale for secondary Y-axis if selected
        if chart_settings.get('log_scale_y2', False):
            ax2.set_yscale('log')
        
        # Set manual limits for secondary Y-axis if not auto-scaling
        if not chart_settings.get('auto_scale', True):
            try:
                y2_min, y2_max = chart_settings.get('y2_min'), chart_settings.get('y2_max')
                if y2_min and y2_max:
                    ax2.set_ylim(float(y2_min), float(y2_max))
            except ValueError:
                pass  # Already warned above
        
        # Plot secondary axes
        for sec_axis in secondary_axes:
            # Get valid data points for this series
            series_df = plot_df[[x_axis, sec_axis]].dropna()
            if len(series_df) == 0:
                logging.warning(f"No valid data points for {sec_axis} vs {x_axis}")
                continue
                
            logging.debug(f"Plotting {sec_axis} vs {x_axis}: {len(series_df)} points")
            has_valid_data = True
            
            if is_scatter:
                ax2.scatter(series_df[x_axis], series_df[sec_axis], label=sec_axis, marker='x', alpha=0.7)
            else:
                ax2.plot(series_df[x_axis], series_df[sec_axis], label=sec_axis, linestyle="--")
        
        # Set label for secondary Y-axis
        y2_label = "Secondary Y-Axes" if len(secondary_axes) > 1 else secondary_axes[0] if secondary_axes else ""
        if chart_settings.get('normalize_data', False) and y2_label:
            y2_label += " (Normalized)"
        ax2.set_ylabel(y2_label)
        
        # Add legend for secondary Y-axis
        lines2, labels2 = ax2.get_legend_handles_labels()
        if lines2:
            ax2.legend(lines2, labels2, loc="upper right")
    
    # Add legend for primary axes
    lines1, labels1 = ax.get_legend_handles_labels()
    if lines1:
        ax.legend(lines1, labels1, loc="upper left")
    
    # Check if we actually plotted anything
    if not has_valid_data:
        plt.close(figure)
        chart_info['error'] = "No valid data points to plot"
        return None, chart_info
    
    # Format X-axis ticks for datetime if needed
    if x_is_datetime and datetime_string_map:
        try:
            # Create a custom formatter for the x-axis
            def format_timestamp(x, pos=None):
                # Find the nearest mapped timestamp
                if not np.isfinite(x):
                    return ''
                
                # Round to nearest integer as the map uses integers
                x_int = int(round(x))
                
                # Find the closest key in the map
                closest_keys = sorted(datetime_string_map.keys(), key=lambda k: abs(k - x_int))
                
                if closest_keys:
                    # Get the datetime string from the map
                    return datetime_string_map[closest_keys[0]]
                else:
                    return str(x_int)
            
            # Apply the custom formatter
            ax.xaxis.set_major_formatter(FuncFormatter(format_timestamp))
            
            # Set tick positions at regular intervals
            locs = ax.get_xticks()
            if locs.size > 0:
                # Get the min and max of data
                x_min, x_max = plot_df[x_axis].min(), plot_df[x_axis].max()
                
                # Create about 5-10 ticks across the range
                total_range = x_max - x_min
                tick_interval = max(1, total_range // 8)  # At least 1 unit apart
                
                # Generate tick positions
                tick_positions = np.arange(
                    np.floor(x_min / tick_interval) * tick_interval,
                    np.ceil(x_max / tick_interval) * tick_interval + tick_interval,
                    tick_interval
                )
                
                if len(tick_positions) > 1:
                    ax.set_xticks(tick_positions)
            
            # Rotate the tick labels for better readability
            plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')
            
            logging.debug("Successfully formatted datetime axis with string labels")
        except Exception as e:
            logging.warning(f"Error formatting datetime axis: {str(e)}")
    
    # Set title
    plot_type = "Scatter" if is_scatter else "Line"
    scaling_info = " (Normalized)" if chart_settings.get('normalize_data', False) else ""
    ax.set_title(f"{plot_type} Chart: {', '.join(y_axes)} vs {x_axis}{scaling_info}")
    
    # Adjust layout to make room for labels
    plt.tight_layout()
    
    # Store information about the chart
    chart_info['type'] = plot_type
    chart_info['x_axis'] = x_axis
    chart_info['y_axes'] = y_axes
    chart_info['secondary_axes'] = secondary_axes
    chart_info['success'] = True
    
    return figure, chart_info
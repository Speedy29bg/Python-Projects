#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Interactive Chart Generator

Handles chart creation with comprehensive interactive features including:
- Navigation toolbar for zoom, pan, save
- Interactive toggles for grid, legend, data points
- Data cursor with advanced tooltips
- Crosshair cursor for precise inspection
- Adjustable line properties (width, transparency)
- Statistics overlay
- Coordinate display
"""

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.ticker import FuncFormatter
import numpy as np
import pandas as pd
import tkinter as tk
from tkinter import ttk
from typing import List, Dict, Optional, Any, Tuple
from utils.logger import get_logger

logger = get_logger()

class InteractiveChartGenerator:
    """Generates interactive charts with comprehensive controls"""
    
    def __init__(self):
        """Initialize the chart generator"""
        self.figure = None
        self.canvas = None
        self.toolbar = None
        self.current_axes = []
          # Color schemes
        self.color_schemes = {
            'default': plt.cm.tab10,
            'viridis': plt.cm.viridis,
            'plasma': plt.cm.plasma,
            'inferno': plt.cm.inferno,
            'magma': plt.cm.magma,
            'cool': plt.cm.cool,
            'warm': plt.cm.Wistia
        }
    
    def create_interactive_chart(self, parent_frame, x_data, y_data_list, 
                               x_label="X", y_labels=None, chart_type="line",
                               color_scheme="default", dual_axis=False, **kwargs):
        """
        Create an interactive chart with comprehensive controls
        
        Args:
            parent_frame: Tkinter frame to place the chart in
            x_data: X-axis data (pandas Series or array-like)
            y_data_list: List of Y-axis data series
            x_label: X-axis label
            y_labels: List of Y-axis labels
            chart_type: Type of chart ('line' or 'scatter')
            color_scheme: Color scheme name
            dual_axis: Whether to use dual/multiple Y-axes for different scales
            **kwargs: Additional chart options
        """
        
        # Clear any existing content
        for widget in parent_frame.winfo_children():
            widget.destroy()
        
        # Clean up any existing chart elements
        self._cleanup_chart_elements()
        
        # Create main container
        main_container = ttk.Frame(parent_frame)
        main_container.pack(fill='both', expand=True)
        
        # Calculate responsive figure size based on parent frame
        # Get the root window to calculate size
        root = parent_frame.winfo_toplevel()
        try:
            # Get current window dimensions
            window_width = root.winfo_width()
            window_height = root.winfo_height()
            
            # Calculate figure size (approximately 40% of window width, maintain aspect ratio)
            fig_width = max(min(window_width * 0.4 / 100, 12), 6)  # Convert pixels to inches, clamp between 6-12
            fig_height = max(min(window_height * 0.5 / 100, 9), 4)  # Convert pixels to inches, clamp between 4-9
            
        except:
            # Fallback to default size if window size can't be determined
            fig_width, fig_height = 8, 6
        
        # Create the matplotlib figure with responsive size
        self.figure = plt.Figure(figsize=(fig_width, fig_height), dpi=100)
        ax = self.figure.add_subplot(111)
        
        # Prepare data
        if not isinstance(y_data_list, list):
            y_data_list = [y_data_list]
        
        if y_labels is None:
            y_labels = [f"Series {i+1}" for i in range(len(y_data_list))]
        elif not isinstance(y_labels, list):
            y_labels = [y_labels]
        
        # Get colors from scheme
        colors = self._get_colors(color_scheme, len(y_data_list))
        
        # Create the plot with optional dual axis support
        self.current_axes = []
        axes_list = [ax]  # Keep track of all axes
        
        if dual_axis and len(y_data_list) > 1:
            # Create multiple axes for different scales
            for i, (y_data, label) in enumerate(zip(y_data_list, y_labels)):
                if i == 0:
                    # Use the primary axis for the first series
                    current_ax = ax
                else:
                    # Create secondary axes for additional series
                    current_ax = ax.twinx()
                    axes_list.append(current_ax)
                    
                    # Position the additional axes
                    if i > 1:
                        current_ax.spines['right'].set_position(('outward', 60 * (i - 1)))
                        current_ax.spines['right'].set_visible(True)
                
                # Plot the data
                if chart_type == "line":
                    line, = current_ax.plot(x_data, y_data, label=label, color=colors[i], 
                                          linewidth=1.5, marker='o', markersize=3)
                else:  # scatter
                    line = current_ax.scatter(x_data, y_data, label=label, color=colors[i], s=30)
                
                # Set Y-axis label and color
                current_ax.set_ylabel(label, color=colors[i])
                current_ax.tick_params(axis='y', labelcolor=colors[i])
                
                self.current_axes.append((line, current_ax))
        else:
            # Single axis for all series (original behavior)
            for i, (y_data, label) in enumerate(zip(y_data_list, y_labels)):
                if chart_type == "line":
                    line, = ax.plot(x_data, y_data, label=label, color=colors[i], 
                                  linewidth=1.5, marker='o', markersize=3)
                else:  # scatter
                    line = ax.scatter(x_data, y_data, label=label, color=colors[i], s=30)
                
                self.current_axes.append((line, ax))
        
        # Set labels and title
        ax.set_xlabel(x_label)
        if not dual_axis or len(y_data_list) == 1:
            ax.set_ylabel(y_labels[0] if len(y_labels) == 1 else "Value")
        
        ax.set_title("Interactive Chart Preview")
        ax.grid(True, alpha=0.3)
        
        # Handle legend for multiple axes
        if dual_axis and len(y_data_list) > 1:
            # Combine legends from all axes
            lines, labels = [], []
            for axis in axes_list:
                axis_lines, axis_labels = axis.get_legend_handles_labels()
                lines.extend(axis_lines)
                labels.extend(axis_labels)
            ax.legend(lines, labels, loc='upper left')
        else:
            ax.legend()
        
        # Store axes list for later use
        self.axes_list = axes_list
        
        # Adjust layout
        self.figure.tight_layout()
        
        # Create the canvas
        self.canvas = FigureCanvasTkAgg(self.figure, master=main_container)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill='both', expand=True)
        
        # Add interactive controls
        self._add_interactive_controls(main_container, axes_list, chart_type, dual_axis)
        
        logger.info(f"Created interactive {chart_type} chart with {len(y_data_list)} series" + 
                   (f" on {len(axes_list)} axes" if dual_axis else ""))
    def _add_interactive_controls(self, parent, axes_list, chart_type, dual_axis=False):
        """Add comprehensive interactive controls to the chart"""
        
        # Get primary axis for certain operations
        primary_ax = axes_list[0]
        
        # Navigation toolbar
        toolbar_frame = ttk.Frame(parent)
        toolbar_frame.pack(fill='x', pady=2)
        
        self.toolbar = NavigationToolbar2Tk(self.canvas, toolbar_frame)
        self.toolbar.update()
        
        # Custom controls frame 1
        controls_frame1 = ttk.Frame(parent)
        controls_frame1.pack(fill='x', pady=5)
        
        # Grid toggle
        grid_var = tk.BooleanVar(value=True)
        def toggle_grid():
            for ax in axes_list:
                ax.grid(grid_var.get(), alpha=0.3)
            self.canvas.draw()
        
        ttk.Checkbutton(controls_frame1, text="Grid Lines", variable=grid_var, 
                       command=toggle_grid).pack(side='left', padx=5)
          # Data points toggle (for line charts)
        if chart_type == "line":
            points_var = tk.BooleanVar(value=True)
            def toggle_points():
                for ax in axes_list:
                    for line in ax.get_lines():
                        if hasattr(line, 'set_marker'):
                            line.set_marker('o' if points_var.get() else '')
                            line.set_markersize(3 if points_var.get() else 0)
                self.canvas.draw()
            
            ttk.Checkbutton(controls_frame1, text="Show Points", variable=points_var, 
                           command=toggle_points).pack(side='left', padx=5)
        
        # Legend toggle
        legend_var = tk.BooleanVar(value=True)
        def toggle_legend():
            for ax in axes_list:
                legend = ax.get_legend()
                if legend:
                    legend.set_visible(legend_var.get())
            self.canvas.draw()
        
        ttk.Checkbutton(controls_frame1, text="Show Legend", variable=legend_var, 
                       command=toggle_legend).pack(side='left', padx=5)
          # Data cursor toggle
        cursor_var = tk.BooleanVar(value=False)
        def toggle_cursor():
            if cursor_var.get():
                self._enable_data_cursor(primary_ax)
            else:
                self._disable_data_cursor()
        
        ttk.Checkbutton(controls_frame1, text="Data Cursor", variable=cursor_var, 
                       command=toggle_cursor).pack(side='left', padx=5)        # Crosshair toggle
        crosshair_var = tk.BooleanVar(value=False)
        def toggle_crosshair():
            try:
                if crosshair_var.get():
                    self._enable_crosshair(primary_ax)
                    logger.info("Crosshair enabled")
                else:
                    self._disable_crosshair(primary_ax)
                    logger.info("Crosshair disabled")
            except Exception as e:
                logger.error(f"Error toggling crosshair: {e}")
                # Reset checkbox state on error
                crosshair_var.set(False)
        
        ttk.Checkbutton(controls_frame1, text="Crosshair", variable=crosshair_var, 
                       command=toggle_crosshair).pack(side='left', padx=5)
        
        # Custom controls frame 2
        controls_frame2 = ttk.Frame(parent)
        controls_frame2.pack(fill='x', pady=5)
          # Line width control (for line charts)
        if chart_type == "line":
            linewidth_var = tk.DoubleVar(value=1.5)
            def update_linewidth(val):
                width = float(val)
                for ax in axes_list:
                    for line in ax.get_lines():
                        if hasattr(line, 'set_linewidth'):
                            line.set_linewidth(width)
                self.canvas.draw()
            
            ttk.Label(controls_frame2, text="Line Width:").pack(side='left', padx=(5, 2))
            ttk.Scale(controls_frame2, from_=0.5, to=5.0, variable=linewidth_var, 
                     command=update_linewidth, orient='horizontal', length=100).pack(side='left', padx=5)
          # Transparency control
        alpha_var = tk.DoubleVar(value=1.0)
        def update_alpha(val):
            alpha = float(val)
            for ax in axes_list:
                for artist in ax.get_children():
                    if hasattr(artist, 'set_alpha') and hasattr(artist, 'get_label'):
                        if not artist.get_label().startswith('_'):
                            artist.set_alpha(alpha)
            self.canvas.draw()
        
        ttk.Label(controls_frame2, text="Transparency:").pack(side='left', padx=(10, 2))
        ttk.Scale(controls_frame2, from_=0.1, to=1.0, variable=alpha_var, 
                 command=update_alpha, orient='horizontal', length=100).pack(side='left', padx=5)
        
        # Reset zoom button
        def reset_zoom():
            for ax in axes_list:
                ax.relim()
                ax.autoscale()
            self.canvas.draw()
        
        ttk.Button(controls_frame2, text="Reset Zoom", 
                  command=reset_zoom).pack(side='left', padx=10)
          # Statistics toggle
        stats_var = tk.BooleanVar(value=False)
        def toggle_stats():
            if stats_var.get():
                self._show_statistics(primary_ax)
            else:
                self._hide_statistics()
        
        ttk.Checkbutton(controls_frame2, text="Show Stats", variable=stats_var, 
                       command=toggle_stats).pack(side='left', padx=5)
        
        # Coordinate display frame
        coord_frame = ttk.Frame(parent)
        coord_frame.pack(fill='x', pady=2)
        
        self.coord_var = tk.StringVar(value="Click on chart to see coordinates")
        coord_label = ttk.Label(coord_frame, textvariable=self.coord_var, 
                               foreground="blue", font=('Arial', 9))
        coord_label.pack(side='left', padx=5)
        
        # Connect coordinate display
        def on_click(event):
            if event.inaxes:
                self.coord_var.set(f"X: {event.xdata:.4f}, Y: {event.ydata:.4f}")
            else:
                self.coord_var.set("Click on chart to see coordinates")
        
        self.canvas.mpl_connect('button_press_event', on_click)
    
    def _get_colors(self, scheme_name, num_colors):
        """Get colors from the specified color scheme"""
        if scheme_name not in self.color_schemes:
            scheme_name = 'default'
        
        colormap = self.color_schemes[scheme_name]
        
        if scheme_name == 'default':
            # Use tab10 colors for default
            colors = [colormap(i) for i in range(min(num_colors, 10))]
        else:
            # Use colormap for other schemes
            colors = [colormap(i / max(1, num_colors - 1)) for i in range(num_colors)]
        
        return colors
    
    def _enable_data_cursor(self, ax):
        """Enable data cursor with tooltips"""
        try:
            import mplcursors
            
            # Remove existing cursor if any
            if hasattr(self, 'cursor'):
                self.cursor.remove()
            
            # Create new cursor
            self.cursor = mplcursors.cursor(ax, hover=True)
            self.cursor.connect("add", lambda sel: sel.annotation.set_text(
                f"X: {sel.target[0]:.4f}\\nY: {sel.target[1]:.4f}\\nSeries: {sel.artist.get_label()}"
            ))
            self.cursor.connect("add", lambda sel: sel.annotation.set_bbox(
                dict(boxstyle="round,pad=0.3", facecolor="yellow", alpha=0.8)
            ))
            
        except ImportError:
            logger.warning("mplcursors not available, using basic hover")
            self._enable_basic_hover(ax)
    
    def _disable_data_cursor(self):
        """Disable data cursor"""
        if hasattr(self, 'cursor'):
            self.cursor.remove()
            delattr(self, 'cursor')
    
    def _enable_basic_hover(self, ax):
        """Enable basic hover functionality when mplcursors is not available"""
        def on_hover(event):
            if event.inaxes:
                for line in event.inaxes.get_lines():
                    if line.contains(event)[0]:
                        self.coord_var.set(f"Hovering: {line.get_label()} - X: {event.xdata:.4f}, Y: {event.ydata:.4f}")
                        break
        
        self.canvas.mpl_connect('motion_notify_event', on_hover)
    
    def _enable_crosshair(self, ax):
        """Enable crosshair cursor"""
        # Disable any existing crosshair first
        self._disable_crosshair(ax)
        
        # Create crosshair lines if they don't exist
        if not hasattr(self, 'crosshair_h'):
            self.crosshair_h = ax.axhline(color='red', linestyle='--', alpha=0.7, visible=False)
            self.crosshair_v = ax.axvline(color='red', linestyle='--', alpha=0.7, visible=False)
        
        # Keep track of the axis for validation
        self.crosshair_ax = ax
        
        def on_mouse_move(event):
            if (event.inaxes == ax and hasattr(self, 'crosshair_h') and 
                hasattr(self, 'crosshair_ax') and self.crosshair_ax == ax):
                try:
                    # Only update if we have valid data
                    if event.xdata is not None and event.ydata is not None:
                        self.crosshair_h.set_ydata([event.ydata, event.ydata])
                        self.crosshair_v.set_xdata([event.xdata, event.xdata])
                        self.crosshair_h.set_visible(True)
                        self.crosshair_v.set_visible(True)
                        # Use draw_idle for better performance and avoid blocking
                        self.canvas.draw_idle()
                except Exception as e:
                    # Silently ignore errors during crosshair update
                    pass
        
        def on_mouse_leave(event):
            if (hasattr(self, 'crosshair_h') and hasattr(self, 'crosshair_ax') and 
                self.crosshair_ax == ax):
                try:
                    self.crosshair_h.set_visible(False)
                    self.crosshair_v.set_visible(False)
                    self.canvas.draw_idle()
                except Exception as e:
                    # Silently ignore errors during crosshair update
                    pass
        
        # Store event connections for proper cleanup
        self.crosshair_move_cid = self.canvas.mpl_connect('motion_notify_event', on_mouse_move)
        self.crosshair_leave_cid = self.canvas.mpl_connect('axes_leave_event', on_mouse_leave)
    
    def _disable_crosshair(self, ax):
        """Disable crosshair cursor"""
        # Disconnect event handlers
        if hasattr(self, 'crosshair_move_cid'):
            try:
                self.canvas.mpl_disconnect(self.crosshair_move_cid)
                delattr(self, 'crosshair_move_cid')
            except:
                pass
            
        if hasattr(self, 'crosshair_leave_cid'):
            try:
                self.canvas.mpl_disconnect(self.crosshair_leave_cid)
                delattr(self, 'crosshair_leave_cid')
            except:
                pass
        
        # Remove crosshair lines
        if hasattr(self, 'crosshair_h'):
            try:
                self.crosshair_h.remove()
                self.crosshair_v.remove()
            except:
                pass  # Lines might already be removed
            
            # Clean up attributes
            delattr(self, 'crosshair_h')
            delattr(self, 'crosshair_v')
            
        # Clean up axis reference
        if hasattr(self, 'crosshair_ax'):
            delattr(self, 'crosshair_ax')
            
        # Redraw canvas only once to clear crosshairs
        if hasattr(self, 'canvas') and self.canvas:
            try:
                self.canvas.draw_idle()
            except:
                pass
    
    def _show_statistics(self, ax):
        """Show statistics overlay"""
        stats_text = ""
        for line in ax.get_lines():
            if hasattr(line, 'get_ydata'):
                y_data = line.get_ydata()
                if len(y_data) > 0:
                    label = line.get_label()
                    if label and not label.startswith('_'):
                        stats_text += f"{label}:\\n"
                        stats_text += f"  Mean: {np.mean(y_data):.3f}\\n"
                        stats_text += f"  Std: {np.std(y_data):.3f}\\n"
                        stats_text += f"  Min: {np.min(y_data):.3f}\\n"
                        stats_text += f"  Max: {np.max(y_data):.3f}\\n\\n"
        
        # Add text box to the plot
        if stats_text and not hasattr(self.figure, 'stats_text'):
            self.figure.stats_text = self.figure.text(0.02, 0.98, stats_text, 
                                                     transform=self.figure.transFigure,
                                                     verticalalignment='top',
                                                     bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8),
                                                     fontsize=8)
        self.canvas.draw()
    
    def _hide_statistics(self):
        """Hide statistics overlay"""
        if hasattr(self.figure, 'stats_text'):
            self.figure.stats_text.remove()
            delattr(self.figure, 'stats_text')
            self.canvas.draw()
    
    def clear_chart(self, parent_frame):
        """Clear the current chart"""
        for widget in parent_frame.winfo_children():
            widget.destroy()
        
        if self.figure:
            plt.close(self.figure)
            self.figure = None
        
        self.canvas = None
        self.toolbar = None
        self.current_axes = []
    
    def _cleanup_chart_elements(self):
        """Clean up chart elements to prevent conflicts"""
        # Disable crosshair if active (more robust cleanup)
        if hasattr(self, 'crosshair_h') or hasattr(self, 'crosshair_move_cid'):
            try:
                self._disable_crosshair(None)  # ax is not needed for cleanup
            except Exception as e:
                logger.debug(f"Error during crosshair cleanup: {e}")
                # Force cleanup manually
                for attr in ['crosshair_h', 'crosshair_v', 'crosshair_ax', 'crosshair_move_cid', 'crosshair_leave_cid']:
                    if hasattr(self, attr):
                        try:
                            delattr(self, attr)
                        except:
                            pass
                
        # Clean up data cursor
        if hasattr(self, 'cursor'):
            try:
                self._disable_data_cursor()
            except Exception as e:
                logger.debug(f"Error during cursor cleanup: {e}")
                
        # Clean up statistics
        if hasattr(self.figure, 'stats_text'):
            try:
                self._hide_statistics()
            except Exception as e:
                logger.debug(f"Error during statistics cleanup: {e}")
                
        # Close previous figure if exists
        if self.figure:
            try:
                plt.close(self.figure)
            except Exception as e:
                logger.debug(f"Error closing figure: {e}")
            self.figure = None

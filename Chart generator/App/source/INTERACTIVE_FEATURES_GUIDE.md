# Interactive Chart Features Guide

## Overview
The Chart Generator now includes comprehensive interactive functionality that makes chart exploration and analysis much more engaging and powerful.

## How to Access Interactive Features
1. Run `ChartGenerator_new_modular.py`
2. Load your CSV data files
3. Select your axes
4. Configure chart scaling and color options (now positioned right under axes selection)
5. The chart preview (now taking up half the application width) will display with full interactivity

## Interactive Features Available

### 🔧 **Navigation Toolbar** (Top of Chart)
- **Pan**: Drag to move around the chart
- **Zoom**: Rectangle zoom and zoom controls
- **Home**: Reset to original view
- **Back/Forward**: Navigate through zoom history
- **Configure**: Adjust subplot parameters
- **Save**: Save current view

### 🎛️ **Basic Controls** (First Button Row)
- **Grid Lines**: Toggle grid visibility on/off
- **Show Data Points**: Toggle marker visibility on data lines
- **Show Legend**: Toggle legend visibility
- **Auto-update**: Enable/disable automatic chart updates
- **Data Cursor**: Hover over data points to see exact values (requires mplcursors)
- **Crosshair**: Red crosshair lines that follow your mouse for precise reading

### 🎚️ **Customization Sliders**
- **Line Width**: Adjust line thickness from 0.5 to 5.0
- **Transparency**: Adjust line transparency from 0.1 to 1.0

### 📊 **Advanced Features** (Second Button Row)
- **Reset Zoom**: Quickly return to original view
- **Smooth Transitions**: Enable smooth animations (experimental)
- **Show Statistics**: Display mean, std dev, min, max for each data series

### 🖱️ **Mouse Interactions**
- **Click**: Click anywhere on the chart to see exact coordinates
- **Hover**: When data cursor is enabled, hover over lines to see values
- **Crosshair**: When enabled, crosshair follows mouse movement

## Layout Improvements
- **Chart Scaling & Color Options**: Now positioned directly under Axes Selection for better workflow
- **Chart Preview**: Now takes up 50% of the application width for better visibility
- **Organized Controls**: Interactive features are neatly organized in two rows below the chart

## Technical Requirements
- **Required**: matplotlib, tkinter, numpy, pandas
- **Optional**: mplcursors (for enhanced hover tooltips)
  - If not available, basic hover functionality is provided as fallback

## Usage Tips
1. **Start with Data Cursor**: Enable this first to explore your data points
2. **Use Crosshair for Precision**: Great for reading exact coordinates
3. **Adjust Line Width**: Make important data series more prominent
4. **Statistics Toggle**: Quick way to see data overview
5. **Reset Zoom**: Use when you get lost in navigation

## Troubleshooting
- If data cursor doesn't work, install mplcursors: `pip install mplcursors`
- For better performance with large datasets, disable auto-update
- Use Reset Zoom if chart appears corrupted after many operations

## Demo
Run `interactive_demo.py` to see all features in action with sample data.

Enjoy your enhanced interactive chart experience! 🚀

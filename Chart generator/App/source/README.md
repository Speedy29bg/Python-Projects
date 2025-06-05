# Lab Chart Generator

A comprehensive application for generating, customizing, and exporting charts from CSV data files.

## Overview

The Lab Chart Generator provides a graphical user interface for scientists and lab technicians to easily create customized charts from CSV data. It supports various chart types, scaling options, and export formats.

## Features

- **Data Loading**: Automatic detection of CSV format, headers, and data types
- **Chart Customization**: Support for multiple axes, log scaling, and normalization
- **Data Analysis**: Statistical analysis, correlation detection, outlier detection, and data smoothing
- **Export Options**: Export charts to Excel, PNG, PDF, and other formats
- **Preview**: Real-time chart previews as you select columns and adjust settings

## Project Structure

The application follows a modular design pattern with these key components:

- **ChartGenerator_new.py**: Main entry point for the application
- **modules/app.py**: Core application class that manages the UI and workflow
- **modules/chart_generator.py**: Functions related to chart creation
- **modules/chart_export.py**: Functions for exporting charts to various formats
- **modules/data_processor.py**: CSV file handling and basic data processing
- **modules/data_analysis.py**: Advanced data analysis features
- **modules/excel_export.py**: Excel workbook generation with embedded charts
- **modules/chart_generator_utils.py**: Utility functions for chart customization
- **modules/ui_components.py**: Reusable UI components
- **modules/logger.py**: Logging configuration

## Requirements

This application requires the following Python packages:

- Python 3.8+
- pandas
- matplotlib
- numpy
- openpyxl
- scipy
- tkinter (usually included with Python)

See `requirements.txt` for specific version requirements.

## Installation

1. Clone this repository
2. Install required packages:
```
pip install -r requirements.txt
```

## Usage

Run the application by executing the main script:

```
python ChartGenerator_new.py
```

### Basic Workflow

1. Click "Browse" to select one or more CSV files
2. Select columns for X and Y axes
3. Adjust chart options as needed
4. Click "Update Preview" to see your chart
5. Export your chart or generate Excel workbooks with "Export" or "Generate Charts" buttons

### Data Analysis

The application includes advanced data analysis capabilities:

1. Select columns for analysis
2. Click "Analyze Data" button
3. Use the tabbed interface to view statistics, correlations, outliers, and apply transformations

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Author

Lab Chart Tools Team

## Version History

- 1.0: Initial release (May 30, 2025)
  - Modularized codebase with clean separation of concerns
  - Added comprehensive data analysis features
  - Improved error handling and logging

# Module Structure Documentation

## Overview

This document describes the modular structure implemented in the Chart Generator application. The refactoring goal was to improve maintainability, readability, and extensibility by breaking down larger files into smaller, more focused modules organized in logical subfolders.

## Directory Structure

The application is now organized into the following modules:

```
modules/
├── __init__.py                  # Main package initialization
├── app.py                       # Facade to app_controller
├── logger.py                    # Facade to logger_module
├── chart_generator.py           # Facade to chart_generator_module
├── data_processor.py            # Facade to data_processor_module
├── data_analysis.py             # Facade to data_analysis_module
├── excel_export.py              # Facade to export_module
├── ui_components.py             # Facade to ui_components_module
│
├── core/                        # Core application logic
│   ├── __init__.py
│   └── app_controller.py        # Main application controller
│
├── ui/                          # User interface components
│   ├── __init__.py
│   ├── main_window.py           # Main application window
│   ├── file_selection.py        # File selection UI
│   ├── axes_selection.py        # Axes selection UI
│   ├── chart_options.py         # Chart options UI
│   ├── preview_frame.py         # Chart preview UI
│   └── output_options.py        # Output options UI
│
├── data_processor/              # Data processing functionality
│   ├── __init__.py
│   ├── header_detection.py      # Header detection functionality
│   ├── csv_reader.py            # CSV file reading functionality
│   ├── data_scaling.py          # Data scaling functionality
│   └── utils.py                 # Helper utilities
│
├── data/                        # Data management functionality
│   ├── __init__.py
│   └── file_handler.py          # File data handling
│
├── chart_generator_module/      # Chart generation functionality
│   ├── __init__.py
│   ├── figure_management.py     # Figure management
│   ├── plotting.py              # Plotting functionality
│   └── canvas.py                # Canvas creation and management
│
├── data_analysis_module/        # Data analysis functionality
│   ├── __init__.py
│   ├── statistics.py            # Statistical functions
│   ├── filtering.py             # Data filtering functions
│   ├── smoothing.py             # Data smoothing functions
│   ├── correlation.py           # Correlation analysis
│   └── transformations.py       # Data transformation functions
│
├── export_module/               # Export functionality
│   ├── __init__.py
│   ├── worksheet_utils.py       # Excel worksheet utilities
│   ├── excel.py                 # Excel workbook generation
│   └── figure_export.py         # Figure export functionality
│
├── logger_module/               # Logging functionality
│   ├── __init__.py
│   ├── setup.py                 # Logger setup functionality
│   └── exception_handler.py     # Exception handling
│
├── ui_components_module/        # UI component utilities
│   ├── __init__.py
│   ├── loading.py               # Loading indicator components
│   ├── progress.py              # Progress dialog components
│   ├── preview.py               # Data preview components
│   └── listbox.py               # Listbox utility functions
│
└── utils/                       # General utilities
    └── __init__.py
```

## Module Responsibilities

### Core Module

Contains the main application controller that orchestrates the overall functionality.

### UI Module

Handles all user interface components, organized by functional area:
- Main window
- File selection
- Axes selection
- Chart options
- Preview
- Output options

### Data Processor Module

Handles CSV file processing:
- Header detection
- CSV reading
- Data scaling
- Utility functions

### Chart Generator Module

Manages chart creation and visualization:
- Figure management
- Plotting
- Canvas creation and handling

### Data Analysis Module

Provides data analysis capabilities:
- Statistics
- Filtering
- Smoothing
- Correlation analysis
- Data transformations

### Export Module

Handles exporting charts and data:
- Excel workbook generation
- Worksheet utilities
- Figure export

### Logger Module

Manages application logging:
- Logger setup
- Exception handling

### UI Components Module

Provides reusable UI components:
- Loading indicators
- Progress dialogs
- Data previews
- Listbox utilities

## Architectural Approach

1. **Facade Pattern**: Top-level modules provide a simplified interface to the more complex implementation in submodules.
2. **Separation of Concerns**: Each module has a specific responsibility.
3. **Single Responsibility Principle**: Each file handles one aspect of functionality.
4. **Explicit Dependencies**: Dependencies between modules are clearly defined through imports.
5. **Consistent Naming**: Functions and modules follow a consistent naming convention.

## Benefits of the New Structure

1. **Improved Maintainability**: Smaller files are easier to understand and maintain.
2. **Better Testability**: Focused modules with clear responsibilities are easier to test.
3. **Enhanced Collaboration**: Multiple developers can work on different modules simultaneously.
4. **Clearer Organization**: Logical grouping makes it easier to find code.
5. **Reduced Cognitive Load**: Each file does one thing well instead of many things poorly.
6. **Easier Onboarding**: New developers can understand the system more quickly.
7. **Improved Extensibility**: New features can be added with minimal changes to existing code.

## Entry Point

The main entry point is `ChartGenerator_new_modular.py`, which initializes the application, sets up logging, and creates the main application instance from the core module.

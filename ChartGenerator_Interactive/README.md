# Interactive Chart Generator v2.0

A comprehensive, interactive chart generator with advanced visualization features for CSV data analysis.

## 🚀 Features

### Core Functionality
- **CSV Data Loading**: Load and process CSV files with automatic data type detection
- **Multiple Y-Axis Support**: Select multiple columns for comparison
- **Real-time Preview**: Automatic chart updates when settings change
- **Clean, Modern UI**: Intuitive interface with 50/50 split layout

### Interactive Chart Features
- **Navigation Toolbar**: Built-in matplotlib toolbar with zoom, pan, save, and configure options
- **Interactive Toggles**:
  - Grid lines on/off
  - Data points visibility (for line charts)
  - Legend visibility
  - Data cursor with tooltips
  - Crosshair cursor for precise inspection
- **Real-time Adjustments**:
  - Line width slider (0.5-5.0)
  - Transparency slider (0.1-1.0)
  - Statistics overlay toggle
- **Advanced Data Inspection**:
  - Hover tooltips with data values (requires mplcursors)
  - Coordinate display on click
  - Statistical information overlay (mean, std, min, max)
  - Reset zoom functionality

### Chart Types & Styling
- **Chart Types**: Line plots and scatter plots
- **Color Schemes**: Default, Viridis, Plasma, Inferno, Magma, Cool
- **Scaling Options**: Linear and logarithmic scales for both axes
- **Export Options**: PNG, PDF, and clipboard copy

## 📁 Project Structure

```
ChartGenerator_Interactive/
├── main.py                     # Main application entry point
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── src/                        # Source code
│   ├── __init__.py
│   ├── core/                   # Core application logic
│   │   ├── __init__.py
│   │   ├── app_controller.py   # Main application controller
│   │   ├── data_processor.py   # CSV data loading and processing
│   │   └── chart_generator.py  # Interactive chart creation
│   ├── ui/                     # User interface components
│   │   ├── __init__.py
│   │   └── components.py       # UI components (file selection, axes, options)
│   └── utils/                  # Utility modules
│       ├── __init__.py
│       └── logger.py           # Logging configuration
├── data/                       # Data directory (place CSV files here)
├── docs/                       # Documentation
└── logs/                       # Application logs (created automatically)
```

## 🛠️ Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Quick Setup

1. **Clone or download** this project to your local machine

2. **Navigate** to the project directory:
   ```bash
   cd ChartGenerator_Interactive
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**:
   ```bash
   python main.py
   ```

### Dependencies
- **Core**: pandas, numpy, matplotlib
- **Interactive Features**: mplcursors (for advanced tooltips)
- **Optional**: pywin32, pillow (for clipboard support on Windows)

## 📊 Usage Guide

### Getting Started

1. **Launch the Application**:
   ```bash
   python main.py
   ```

2. **Load Data**:
   - Click "Browse & Load CSV" to select a CSV file
   - Or use Quick Load buttons if sample files are available

3. **Select Axes**:
   - Choose X-axis from the dropdown
   - Select one or more Y-axes using checkboxes

4. **Customize Chart**:
   - Choose chart type (Line or Scatter)
   - Select color scheme
   - Enable logarithmic scaling if needed

5. **Interact with Chart**:
   - Use toolbar for zoom, pan, save
   - Toggle visual elements (grid, legend, points)
   - Enable data cursor for detailed inspection
   - Adjust line properties with sliders

### Interactive Features Guide

#### Navigation
- **Zoom**: Use toolbar zoom tool or mouse wheel
- **Pan**: Use toolbar pan tool or click and drag
- **Reset**: Click "Reset Zoom" button to return to original view

#### Data Exploration
- **Data Cursor**: Enable to see tooltips when hovering over data points
- **Crosshair**: Enable for precise coordinate inspection
- **Coordinates**: Click anywhere on chart to see X,Y coordinates
- **Statistics**: Toggle to show statistical information overlay

#### Visual Customization
- **Grid Lines**: Toggle grid visibility
- **Data Points**: Show/hide individual data points on lines
- **Legend**: Toggle legend visibility
- **Line Width**: Adjust thickness of lines (0.5 to 5.0)
- **Transparency**: Adjust line transparency (0.1 to 1.0)

### Exporting Charts

- **PNG**: High-resolution PNG export (300 DPI)
- **PDF**: Vector PDF export for publications
- **Clipboard**: Copy chart directly to clipboard (Windows)

## 🔧 Technical Details

### Key Components

1. **DataProcessor**: Handles CSV loading, data validation, and preprocessing
2. **InteractiveChartGenerator**: Creates matplotlib charts with interactive features
3. **UI Components**: Modular UI components for file selection, axes, and options
4. **AppController**: Coordinates all components and handles application logic

### Interactive Features Implementation

- **Matplotlib Integration**: Uses FigureCanvasTkAgg for Tkinter integration
- **Navigation Toolbar**: Built-in NavigationToolbar2Tk for standard operations
- **Event Handling**: Mouse events for coordinate display and data inspection
- **Real-time Updates**: Automatic chart refresh on parameter changes
- **Advanced Tooltips**: mplcursors library for enhanced data cursor functionality

### Performance Considerations

- **Efficient Data Handling**: Uses pandas for fast data processing
- **Smart Updates**: Only redraws chart when necessary
- **Memory Management**: Proper cleanup of matplotlib figures
- **Responsive UI**: Non-blocking operations for smooth user experience

## 🐛 Troubleshooting

### Common Issues

1. **Import Errors**:
   - Ensure all dependencies are installed: `pip install -r requirements.txt`
   - Check Python version (3.8+ required)

2. **CSV Loading Issues**:
   - Verify file format (comma-separated values)
   - Check for special characters in column names
   - Ensure file is not locked by another application

3. **Interactive Features Not Working**:
   - Install mplcursors for advanced tooltips: `pip install mplcursors`
   - Check matplotlib backend compatibility

4. **Clipboard Copy Issues**:
   - Install Windows dependencies: `pip install pywin32 pillow`
   - Alternative: Use PNG export instead

### Getting Help

- Check the logs directory for detailed error information
- Ensure all requirements are properly installed
- Verify CSV file format and content

## 🎯 Key Improvements Over Previous Versions

1. **Layout Restructuring**: Chart scaling/color options positioned under axes selection
2. **50/50 Layout**: Chart preview takes exactly half the application width
3. **Comprehensive Interactivity**: Full navigation toolbar plus custom controls
4. **Automatic Updates**: No manual "Update Preview" button needed
5. **Enhanced UI**: Professional appearance with clear visual hierarchy
6. **Advanced Features**: Statistics overlay, coordinate display, crosshair cursor
7. **Export Options**: Multiple export formats with high quality output

## 📝 Version History

- **v2.0**: Complete rewrite with interactive features
- **v1.0**: Basic chart generation functionality

## 🤝 Contributing

This project is designed for data analysis and visualization. Feel free to extend or modify according to your needs.

## 📄 License

Open source - feel free to use and modify as needed.

---

**Enjoy creating interactive charts!** 📊✨

"""
UI Components for the Chart Generator Application

This package contains UI-related components for the Chart Generator application.
"""

from modules.app_modules.ui.main_window import MainWindow
from modules.app_modules.ui.file_selection import FileSelectionFrame
from modules.app_modules.ui.axes_selection import AxesSelectionFrame
from modules.app_modules.ui.chart_options import ChartOptionsFrame
from modules.app_modules.ui.preview_frame import PreviewFrame
from modules.app_modules.ui.output_options import OutputOptionsFrame

__all__ = [
    'MainWindow',
    'FileSelectionFrame',
    'AxesSelectionFrame',
    'ChartOptionsFrame',
    'PreviewFrame',
    'OutputOptionsFrame'
]

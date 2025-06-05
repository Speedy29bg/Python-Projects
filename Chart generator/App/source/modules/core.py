"""
Core Module Facade

This module re-exports core components from the app_modules.core package.
"""

from modules.app_modules.core.app_controller import LabChartGenerator as AppController

__all__ = ['AppController']

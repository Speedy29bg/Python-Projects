"""
Logger Module

This package provides logging functionality for the Chart Generator application.
"""

from modules.logger_module.setup import setup_logging
from modules.logger_module.exception_handler import handle_exception

__all__ = [
    'setup_logging',
    'handle_exception'
]

"""
Logger Module

This module provides logging functionality for the Chart Generator application.
It's a facade over the more detailed logger_module.


Author: Speedy29bg
"""

from modules.logger_module import setup_logging, handle_exception

__all__ = [
    'setup_logging',
    'handle_exception'
]
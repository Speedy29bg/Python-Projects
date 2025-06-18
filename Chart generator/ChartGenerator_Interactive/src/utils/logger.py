#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Logging utilities for the Interactive Chart Generator

Provides centralized logging configuration and utilities.
"""

import logging
import os
from datetime import datetime

def setup_logging(log_level=logging.INFO):
    """
    Setup logging configuration
    
    Args:
        log_level: Logging level (default: INFO)
        
    Returns:
        logging.Logger: Configured logger instance
    """
      # Create logs directory if it doesn't exist
    logs_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'logs')
    os.makedirs(logs_dir, exist_ok=True)
    
    # Create log filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_filename = os.path.join(logs_dir, f"chart_generator_{timestamp}.log")
    
    # Configure logging
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_filename, encoding='utf-8'),
            logging.StreamHandler()
        ]
    )
    
    # Create and return logger
    logger = logging.getLogger('InteractiveChartGenerator')
    logger.info(f"Logging initialized. Log file: {log_filename}")
    
    return logger

def get_logger(name=None):
    """
    Get a logger instance
    
    Args:
        name: Logger name (default: InteractiveChartGenerator)
        
    Returns:
        logging.Logger: Logger instance
    """
    return logging.getLogger(name or 'InteractiveChartGenerator')

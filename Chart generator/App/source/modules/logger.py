import logging
import os
from datetime import datetime
import tkinter as tk
import traceback

def setup_logging():
    """Configure application logging
    
    Returns:
        logging.Logger: Configured logger instance
    """
    # Create logs directory if it doesn't exist
    logs_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "logs")
    os.makedirs(logs_dir, exist_ok=True)
    
    # Configure root logger
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)  # Capture all levels
    
    # Clear existing handlers to avoid duplicates
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
    
    # Create formatters
    file_formatter = logging.Formatter(
        '%(asctime)s [%(levelname)s] %(filename)s:%(lineno)d - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_formatter = logging.Formatter('%(levelname)s: %(message)s')
    
    # File handler - detailed logs
    log_filename = f"chart_generator_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    file_handler = logging.FileHandler(os.path.join(logs_dir, log_filename))
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)
    
    # Console handler - less detailed for console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)  # Less verbose for console
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)
    
    logging.info("Logging system initialized")
    logging.info(f"Log file: {os.path.join(logs_dir, log_filename)}")
    
    return logger

def handle_exception(exc_type, exc_value, exc_traceback, status_label=None):
    """Handle uncaught exceptions
    
    Args:
        exc_type: The type of exception
        exc_value: The exception instance
        exc_traceback: The traceback object
        status_label: Optional tkinter label to update with error message
    """
    # Log the error with full traceback
    logging.error("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))
    
    # Format a user-friendly error message
    error_msg = f"An unexpected error occurred:\n{exc_value}"
    
    # Show error dialog if tkinter is still functioning
    try:
        import tkinter.messagebox as messagebox
        messagebox.showerror("Application Error", error_msg)
    except:
        # If tkinter is not working, print to console
        print(error_msg)
    
    # Update status label if possible
    if status_label:
        try:
            status_label.config(text=f"Error: {str(exc_value)}")
        except:
            pass
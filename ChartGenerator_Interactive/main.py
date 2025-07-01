#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Interactive Chart Generator Application

A comprehensive chart generator with advanced interactive features including:
- Real-time chart preview with navigation toolbar
- Interactive controls (zoom, pan, grid, legend toggles)
- Data cursor with tooltips
- Crosshair cursor for precise data inspection
- Adjustable line width and transparency
- Statistics overlay
- Automatic chart updates

Author: Speedy29bg
Version: 2.0 Interactive
Date: June 17, 2025
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os
import logging
import platform
from pathlib import Path
from typing import Optional, Tuple

# Application constants
APP_NAME = "Interactive Chart Generator"
APP_VERSION = "2.0"
MIN_WINDOW_WIDTH = 1000
MIN_WINDOW_HEIGHT = 700
DEFAULT_WIDTH_RATIO = 0.85
DEFAULT_HEIGHT_RATIO = 0.80
MIN_WIDTH_RATIO = 0.60
MIN_HEIGHT_RATIO = 0.60

# Add src directory to path
SRC_DIR = Path(__file__).parent / 'src'
sys.path.insert(0, str(SRC_DIR))

try:
    from core.app_controller import InteractiveChartApp
    from utils.logger import setup_logging
except ImportError as e:
    error_message = f"""Error importing required modules: {e}
Please ensure all required files are present in the src directory"""
    print(error_message)
    sys.exit(1)


def calculate_window_dimensions(screen_width: int, screen_height: int) -> Tuple[int, int, int, int]:
    """
    Calculate optimal window dimensions based on screen size
    
    Returns:
        Tuple of (window_width, window_height, min_width, min_height)
    """
    # Calculate window size as percentage of screen
    window_width = int(screen_width * DEFAULT_WIDTH_RATIO)
    window_height = int(screen_height * DEFAULT_HEIGHT_RATIO)
    
    # Set minimum size (percentage of screen or absolute minimum)
    min_width = max(int(screen_width * MIN_WIDTH_RATIO), MIN_WINDOW_WIDTH)
    min_height = max(int(screen_height * MIN_HEIGHT_RATIO), MIN_WINDOW_HEIGHT)
    
    return window_width, window_height, min_width, min_height


def center_window(root: tk.Tk, window_width: int, window_height: int) -> None:
    """Center window on screen"""
    root.update_idletasks()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)
    
    # Ensure window is not positioned off-screen
    x = max(0, min(x, screen_width - window_width))
    y = max(0, min(y, screen_height - window_height))
    
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")


def should_maximize_window(screen_width: int, screen_height: int) -> bool:
    """Determine if window should start maximized based on screen size"""
    return screen_width <= 1366 or screen_height <= 768


def maximize_window(root: tk.Tk) -> None:
    """Maximize window based on platform"""
    try:
        system = platform.system().lower()
        if system == "windows":
            root.state('zoomed')
        elif system == "darwin":  # macOS
            root.state('zoomed')
        else:  # Linux and others
            root.attributes('-zoomed', True)
    except Exception as e:
        # Fallback to normal state if maximizing fails
        logging.warning(f"Could not maximize window: {e}")
        root.state('normal')


def setup_window_icon(root: tk.Tk) -> None:
    """Setup application icon if available"""
    icon_paths = [
        Path("assets/icon.ico"),
        Path("icon.ico"),
        Path("assets/chart_icon.png"),
        Path("chart_icon.png")
    ]
    
    for icon_path in icon_paths:
        if icon_path.exists():
            try:
                if icon_path.suffix.lower() == '.ico':
                    root.iconbitmap(str(icon_path))
                else:
                    # For PNG files, would need PIL/Pillow
                    pass
                logging.info(f"Application icon loaded: {icon_path}")
                return
            except Exception as e:
                logging.debug(f"Could not load icon {icon_path}: {e}")
    
    logging.debug("No application icon found")


def setup_exception_handling(logger: logging.Logger) -> None:
    """Setup global exception handling"""
    def handle_exception(exc_type, exc_value, exc_traceback):
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return
        
        logger.error("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))
        
        # Show user-friendly error message
        error_msg = f"An unexpected error occurred:\n\n{exc_type.__name__}: {exc_value}"
        if len(error_msg) > 200:
            error_msg = error_msg[:200] + "..."
        
        try:
            messagebox.showerror("Application Error", error_msg)
        except:
            # If messagebox fails, print to console
            print(f"Critical error: {error_msg}")
    
    sys.excepthook = handle_exception


def print_welcome_message() -> None:
    """Print application welcome message"""
    welcome_text = f"""{"=" * 60}
{APP_NAME.upper()} v{APP_VERSION}
{"=" * 60}
Features:
• Real-time interactive chart preview
• Navigation toolbar (zoom, pan, save)
• Interactive controls (grid, legend, data points)
• Advanced tooltips and crosshair cursor
• Adjustable line properties
• Statistics overlay
• Automatic chart updates
• Responsive design and multiple file support
{"=" * 60}"""
    
    print(welcome_text)


def cleanup_resources(root: Optional[tk.Tk] = None, logger: Optional[logging.Logger] = None) -> None:
    """Clean up application resources"""
    if logger:
        logger.info("Cleaning up application resources")
    
    if root:
        try:
            root.quit()
            root.destroy()
        except Exception as e:
            if logger:
                logger.warning(f"Error during cleanup: {e}")


def main():
    """Main application entry point"""
    logger = None
    root = None
    
    try:
        # Setup logging
        logger = setup_logging()
        logger.info(f"Starting {APP_NAME} v{APP_VERSION}")
        
        # Verify Python version
        if sys.version_info < (3, 7):
            raise RuntimeError("Python 3.7 or higher is required")
        
        # Create main window
        root = tk.Tk()
        root.title(f"{APP_NAME} v{APP_VERSION}")
        
        # Get screen dimensions
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        
        # Calculate optimal window dimensions
        window_width, window_height, min_width, min_height = calculate_window_dimensions(
            screen_width, screen_height
        )
        
        # Configure window
        root.geometry(f"{window_width}x{window_height}")
        root.minsize(min_width, min_height)
        root.resizable(True, True)
        
        # Setup window icon
        setup_window_icon(root)
        
        # Setup exception handling
        setup_exception_handling(logger)
        
        # Create application instance
        logger.info("Initializing application controller")
        app = InteractiveChartApp(root)
        
        # Center and optionally maximize window
        center_window(root, window_width, window_height)
        
        if should_maximize_window(screen_width, screen_height):
            maximize_window(root)
        
        # Log configuration
        logger.info(f"Screen size: {screen_width}x{screen_height}")
        logger.info(f"Window size: {window_width}x{window_height}")
        logger.info(f"Minimum size: {min_width}x{min_height}")
        logger.info(f"Platform: {platform.system()} {platform.release()}")
        
        # Print welcome message
        print_welcome_message()
        logger.info("Application started successfully")
        
        # Start the application main loop
        root.mainloop()
        
    except ImportError as e:
        error_msg = f"Missing required dependencies: {e}"
        print(f"Error: {error_msg}")
        if logger:
            logger.error(error_msg)
        messagebox.showerror("Import Error", error_msg)
        return 1
        
    except Exception as e:
        error_msg = f"Failed to start application: {e}"
        print(f"Error: {error_msg}")
        if logger:
            logger.error(error_msg, exc_info=True)
        messagebox.showerror("Startup Error", error_msg)
        return 1
        
    finally:
        cleanup_resources(root, logger)
    
    return 0


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)

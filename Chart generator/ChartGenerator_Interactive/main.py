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
from tkinter import ttk, messagebox, filedialog
import sys
import os
import logging

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from core.app_controller import InteractiveChartApp
from utils.logger import setup_logging

def main():
    """Main application entry point"""
    
    # Setup logging
    logger = setup_logging()
    logger.info("Starting Interactive Chart Generator v2.0")
    
    try:
        # Create main window
        root = tk.Tk()
        root.title("Interactive Chart Generator v2.0")
        root.geometry("1400x900")
        root.minsize(1200, 800)
        
        # Set application icon (if available)
        try:
            root.iconbitmap(default="assets/icon.ico")
        except:
            pass  # Icon file not found, continue without it
        
        # Create application
        app = InteractiveChartApp(root)
        
        # Center window on screen
        root.update_idletasks()
        x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
        y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
        root.geometry(f"+{x}+{y}")
        
        # Set up exception handling
        def handle_exception(exc_type, exc_value, exc_traceback):
            if issubclass(exc_type, KeyboardInterrupt):
                sys.__excepthook__(exc_type, exc_value, exc_traceback)
                return
            
            logger.error("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))
            messagebox.showerror("Error", f"An unexpected error occurred:\\n{exc_value}")
        
        sys.excepthook = handle_exception
        
        # Welcome message
        logger.info("Application started successfully")
        print("="*60)
        print("INTERACTIVE CHART GENERATOR v2.0")
        print("="*60)
        print("Features:")
        print("• Real-time interactive chart preview")
        print("• Navigation toolbar (zoom, pan, save)")
        print("• Interactive controls (grid, legend, data points)")
        print("• Advanced tooltips and crosshair cursor")
        print("• Adjustable line properties")
        print("• Statistics overlay")
        print("• Automatic chart updates")
        print("="*60)
        
        # Start the application
        root.mainloop()
        
    except Exception as e:
        logger.error(f"Failed to start application: {e}")
        messagebox.showerror("Startup Error", f"Failed to start the application:\\n{e}")
    finally:
        try:
            root.destroy()
        except:
            pass

if __name__ == "__main__":
    main()

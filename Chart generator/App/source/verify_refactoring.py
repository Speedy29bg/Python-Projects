#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Chart Generator Refactoring Verification

This script verifies that the Chart Generator application has been
successfully refactored into a modular structure.


Author: Speedy29bg
Version: 1.1
Date: June 5, 2025
"""

import os
import sys
import importlib
import inspect
import tkinter as tk
from pathlib import Path

def print_section(title):
    """Print a section header"""
    print()
    print("=" * 80)
    print(f" {title.upper()} ".center(80, "="))
    print("=" * 80)
    print()

def check_import(module_name):
    """Try to import a module and return success status"""
    try:
        importlib.import_module(module_name)
        return True
    except ImportError as e:
        print(f"  Import Error: {e}")
        return False

def check_directory(path):
    """Check if a directory exists and has the required structure"""
    path = Path(path)
    
    if not path.exists():
        print(f"  ❌ Directory does not exist: {path}")
        return False
    
    init_file = path / "__init__.py"
    if not init_file.exists():
        print(f"  ❌ Missing __init__.py in {path}")
        return False
    
    print(f"  ✅ Directory structure verified: {path}")
    return True

def list_module_contents(module_name):
    """List the contents of a module"""
    try:
        module = importlib.import_module(module_name)
        
        # Get all attributes that don't start with underscore
        attributes = [attr for attr in dir(module) if not attr.startswith('_')]
        
        # Check for __all__ attribute
        if hasattr(module, "__all__"):
            print(f"  Module exports ({len(module.__all__)}): {', '.join(module.__all__)}")
        else:
            print(f"  Module does not define __all__")
        
        # Print public functions
        functions = [attr for attr in attributes 
                     if inspect.isfunction(getattr(module, attr))]
        if functions:
            print(f"  Functions ({len(functions)}): {', '.join(functions)}")
        
        # Print classes
        classes = [attr for attr in attributes 
                   if inspect.isclass(getattr(module, attr))]
        if classes:
            print(f"  Classes ({len(classes)}): {', '.join(classes)}")
        
        return True
    except ImportError as e:
        print(f"  Import Error: {e}")
        return False

def verify_app_controller():
    """Verify that the AppController can be instantiated"""
    print_section("VERIFYING APP CONTROLLER")
    
    try:
        from modules.core import AppController
        print("  ✅ Successfully imported AppController from modules.core")
        
        # Create a root window for testing
        root = tk.Tk()
        root.withdraw()  # Hide the window
        
        # Create the controller
        try:
            app = AppController(root)
            print("  ✅ Successfully created AppController instance")
            
            # Check that UI components are accessible
            ui_components = [
                ("Main window", app.main_window),
                ("File selection frame", app.file_selection_frame),
                ("Axes selection frame", app.axes_selection_frame),
                ("Chart options frame", app.chart_options_frame),
                ("Preview frame", app.preview_frame),
                ("Output options frame", app.output_options_frame)
            ]
            
            print("\n  Verifying UI components:")
            for name, component in ui_components:
                if component:
                    print(f"    ✅ {name} initialized successfully")
                else:
                    print(f"    ❌ {name} not initialized")
            
            root.destroy()
            return True
            
        except Exception as e:
            print(f"  ❌ Error creating AppController: {str(e)}")
            return False
            
    except ImportError as e:
        print(f"  ❌ Failed to import AppController: {str(e)}")
        return False

def main():
    """Main function"""
    # Add the current directory to the path
    sys.path.insert(0, os.path.abspath('.'))
    
    # Check main files
    print_section("Main Files")
    main_files = [
        "ChartGenerator_new_modular.py",
        "MODULE_STRUCTURE.md",
        "REFACTORING.md"
    ]
    for file in main_files:
        if os.path.exists(file):
            print(f"✅ Found: {file}")
        else:
            print(f"❌ Missing: {file}")
    
    # Check module directories
    print_section("Module Directories")
    module_dirs = [
        "modules/core",
        "modules/ui",
        "modules/data",
        "modules/data_processor",
        "modules/chart_generator_module",
        "modules/data_analysis_module",
        "modules/export_module",
        "modules/logger_module",
        "modules/ui_components_module",
        "modules/utils"
    ]
    for dir_path in module_dirs:
        check_directory(dir_path)
    
    # Check main module facades
    print_section("Module Facades")
    facade_modules = [
        "modules.app",
        "modules.chart_generator",
        "modules.data_processor",
        "modules.data_analysis",
        "modules.excel_export",
        "modules.logger",
        "modules.ui_components"
    ]
    for module_name in facade_modules:
        if check_import(module_name):
            print(f"✅ Successfully imported: {module_name}")
            list_module_contents(module_name)
            print()
        else:
            print(f"❌ Failed to import: {module_name}")
            print()
    
    # Check submodule packages
    print_section("Submodule Packages")
    submodule_packages = [
        "modules.core",
        "modules.ui",
        "modules.data",
        "modules.data_processor",
        "modules.chart_generator_module",
        "modules.data_analysis_module",
        "modules.export_module",
        "modules.logger_module",
        "modules.ui_components_module",
        "modules.utils"
    ]
    for package_name in submodule_packages:
        if check_import(package_name):
            print(f"✅ Successfully imported: {package_name}")
            list_module_contents(package_name)
            print()
        else:
            print(f"❌ Failed to import: {package_name}")
            print()
    
    # Check app_modules structure
    print_section("App Modules Structure")
    app_modules_packages = [
        "modules.app_modules.core",
        "modules.app_modules.ui",
        "modules.app_modules.data",
        "modules.app_modules.utils"
    ]
    for package_name in app_modules_packages:
        if check_import(package_name):
            print(f"✅ Successfully imported: {package_name}")
            list_module_contents(package_name)
            print()
        else:
            print(f"❌ Failed to import: {package_name}")
            print()
    
    # Verify AppController
    controller_ok = verify_app_controller()
    
    print_section("Verification Complete")
    if controller_ok:
        print("✅ Application controller initialized successfully!")
    else:
        print("❌ Application controller verification failed!")

if __name__ == "__main__":
    main()

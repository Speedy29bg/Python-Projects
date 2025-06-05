#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Chart Generator Project Structure Verification Script

This script verifies the structure and module functionality 
of the Chart Generator project after restructuring.

Author: Lab Chart Tools Team
Date: May 30, 2025
"""

import os
import sys
import importlib
import inspect
from typing import Dict, List, Set

def print_header(text: str) -> None:
    """Print a header with the specified text"""
    print("\n" + "=" * 80)
    print(text.center(80))
    print("=" * 80 + "\n")

def check_module_exists(module_name: str) -> bool:
    """Check if a module exists and can be imported"""
    try:
        importlib.import_module(module_name)
        return True
    except ImportError:
        return False

def check_function_exists(module_name: str, function_name: str) -> bool:
    """Check if a function exists in a module"""
    try:
        module = importlib.import_module(module_name)
        return hasattr(module, function_name)
    except ImportError:
        return False

def verify_project_structure() -> None:
    """Verify that all required project files exist"""
    print_header("VERIFYING PROJECT STRUCTURE")
    
    # Required files
    required_files = [
        "ChartGenerator_new.py",
        "modules/app.py",
        "modules/chart_generator.py",
        "modules/chart_export.py",
        "modules/data_processor.py",
        "modules/data_analysis.py",
        "modules/excel_export.py",
        "modules/chart_generator_utils.py",
        "modules/ui_components.py",
        "modules/logger.py",
        "requirements.txt",
        "README.md"
    ]
    
    # Check each file
    all_files_exist = True
    for file_path in required_files:
        file_path = os.path.abspath(file_path)
        exists = os.path.exists(file_path)
        status = "✅ Found" if exists else "❌ Missing"
        print(f"{status}: {file_path}")
        
        if not exists:
            all_files_exist = False
    
    # Summary
    if all_files_exist:
        print("\n✅ All required files exist")
    else:
        print("\n❌ Some required files are missing")

def verify_module_imports() -> None:
    """Verify that all necessary modules can be imported"""
    print_header("VERIFYING MODULE IMPORTS")
    
    # Required modules
    required_modules = [
        "modules.app",
        "modules.chart_generator",
        "modules.chart_export",
        "modules.data_processor",
        "modules.data_analysis",
        "modules.excel_export",
        "modules.chart_generator_utils",
        "modules.ui_components",
        "modules.logger"
    ]
    
    # Check each module
    all_modules_importable = True
    for module_name in required_modules:
        can_import = check_module_exists(module_name)
        status = "✅ Importable" if can_import else "❌ Import Failed"
        print(f"{status}: {module_name}")
        
        if not can_import:
            all_modules_importable = False
    
    # Summary
    if all_modules_importable:
        print("\n✅ All modules can be imported")
    else:
        print("\n❌ Some modules cannot be imported")

def verify_key_functions() -> None:
    """Verify that key functions exist in their respective modules"""
    print_header("VERIFYING KEY FUNCTIONS")
    
    # Required functions by module
    required_functions = {
        "modules.chart_generator": ["create_preview_plot", "clear_figure"],
        "modules.chart_export": ["export_chart"],
        "modules.data_processor": ["read_csv_file", "process_data_for_scaling"],
        "modules.data_analysis": ["calculate_statistics", "analyze_correlation", "filter_outliers"],
        "modules.excel_export": ["generate_excel_workbook"],
        "modules.chart_generator_utils": ["apply_color_scheme"],
        "modules.logger": ["setup_logging", "handle_exception"]
    }
    
    # Check each function
    all_functions_exist = True
    for module_name, functions in required_functions.items():
        print(f"\nModule: {module_name}")
        
        for function_name in functions:
            exists = check_function_exists(module_name, function_name)
            status = "✅ Found" if exists else "❌ Missing"
            print(f"  {status}: {function_name}()")
            
            if not exists:
                all_functions_exist = False
    
    # Summary
    if all_functions_exist:
        print("\n✅ All key functions exist in their respective modules")
    else:
        print("\n❌ Some key functions are missing")

def verify_requirements() -> None:
    """Verify that all required packages are listed in requirements.txt"""
    print_header("VERIFYING REQUIREMENTS.TXT")
    
    # Essential packages
    essential_packages = [
        "numpy",
        "pandas", 
        "matplotlib",
        "openpyxl",
        "scipy"
    ]
    
    # Read requirements.txt
    try:
        with open("requirements.txt", "r") as f:
            requirements_content = f.read().lower()
        
        # Check for each package
        for package in essential_packages:
            found = package.lower() in requirements_content
            status = "✅ Listed" if found else "❌ Missing"
            print(f"{status}: {package}")
        
    except FileNotFoundError:
        print("❌ requirements.txt file not found")

def verify_main_script() -> None:
    """Verify that the main script has minimal code that imports from modules"""
    print_header("VERIFYING MAIN SCRIPT")
    
    try:
        with open("ChartGenerator_new.py", "r") as f:
            main_content = f.read()
        
        # Check length - a clean main file should be relatively short
        lines = [line for line in main_content.split("\n") if line.strip() and not line.strip().startswith("#")]
        is_short = len(lines) < 50
        
        if is_short:
            print("✅ Main script is concise (<50 lines of code)")
        else:
            print("❌ Main script is too long, might need more modularization")
        
        # Check imports
        required_imports = ["modules.app", "modules.logger"]
        for module_import in required_imports:
            import_found = f"from {module_import}" in main_content or f"import {module_import}" in main_content
            status = "✅ Found" if import_found else "❌ Missing"
            print(f"{status}: Import for {module_import}")
        
    except FileNotFoundError:
        print("❌ ChartGenerator_new.py file not found")

if __name__ == "__main__":
    # Add source directory to path to make imports work
    source_dir = os.path.abspath(".")
    if source_dir not in sys.path:
        sys.path.append(source_dir)
    
    # Run verification functions
    verify_project_structure()
    verify_module_imports()
    verify_key_functions()
    verify_requirements()
    verify_main_script()
    
    print_header("VERIFICATION COMPLETE")

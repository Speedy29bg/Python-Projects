#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test script for the Interactive Chart Generator v2.0

This script tests the basic functionality of the new interactive chart generator.
"""

import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_imports():
    """Test all imports"""
    print("Testing imports...")
    
    try:
        from core.app_controller import InteractiveChartApp
        print("✓ App controller import successful")
        
        from core.data_processor import DataProcessor
        print("✓ Data processor import successful")
        
        from core.chart_generator import InteractiveChartGenerator
        print("✓ Chart generator import successful")
        
        from ui.components import FileSelectionFrame, AxesSelectionFrame, ChartOptionsFrame, StatusFrame
        print("✓ UI components import successful")
        
        from utils.logger import setup_logging
        print("✓ Logger import successful")
        
        return True
        
    except Exception as e:
        print(f"✗ Import error: {e}")
        return False

def test_dependencies():
    """Test required dependencies"""
    print("\\nTesting dependencies...")
    
    deps = ['pandas', 'numpy', 'matplotlib', 'tkinter']
    optional_deps = ['mplcursors']
    
    all_good = True
    
    for dep in deps:
        try:
            __import__(dep)
            print(f"✓ {dep}")
        except ImportError:
            print(f"✗ {dep} - MISSING!")
            all_good = False
    
    for dep in optional_deps:
        try:
            __import__(dep)
            print(f"✓ {dep} (optional)")
        except ImportError:
            print(f"⚠ {dep} (optional) - will use basic functionality")
    
    return all_good

def test_data_files():
    """Test sample data files"""
    print("\\nTesting sample data files...")
    
    data_dir = "data"
    if os.path.exists(data_dir):
        csv_files = [f for f in os.listdir(data_dir) if f.endswith('.csv')]
        print(f"✓ Found {len(csv_files)} sample CSV files")
        for file in csv_files:
            print(f"  - {file}")
        return True
    else:
        print("⚠ No data directory found")
        return False

def main():
    """Main test function"""
    print("="*60)
    print("INTERACTIVE CHART GENERATOR v2.0 - TEST SCRIPT")
    print("="*60)
    
    # Test imports
    imports_ok = test_imports()
    
    # Test dependencies  
    deps_ok = test_dependencies()
    
    # Test data files
    data_ok = test_data_files()
    
    print("\\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    if imports_ok and deps_ok:
        print("✓ All core components are working!")
        print("✓ Ready to run the Interactive Chart Generator")
        print("\\nTo start the application, run:")
        print("  python main.py")
        
        if data_ok:
            print("\\nSample data files are available for testing.")
    else:
        print("✗ Some issues found. Please check the requirements.")
        
    print("="*60)

if __name__ == "__main__":
    main()

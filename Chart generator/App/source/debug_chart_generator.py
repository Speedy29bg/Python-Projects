#!/usr/bin/env python
"""
Debug script to trace the chart generator import and function calls
"""

def trace_imports():
    print("=== DEBUGGING CHART GENERATOR IMPORTS ===")
    
    # Test direct import
    try:
        from modules.chart_generator import create_tkinter_canvas
        print("✓ Direct import successful")
        
        # Check if the function has our debug prints
        import inspect
        source = inspect.getsource(create_tkinter_canvas)
        if "DEBUG: create_tkinter_canvas called" in source:
            print("✓ Function contains our interactive features")
        else:
            print("✗ Function does NOT contain our interactive features")
            
        print("Function location:", inspect.getfile(create_tkinter_canvas))
        
    except Exception as e:
        print(f"✗ Import failed: {e}")
        return False
    
    # Test app controller import path
    try:
        from modules.app_modules.core.app_controller import LabChartGenerator
        print("✓ App controller import successful")
        
        # Check what chart_generator the app controller imports
        import modules.app_modules.core.app_controller as app_module
        source = inspect.getsource(app_module)
        
        if "from modules.chart_generator import" in source:
            print("✓ App controller imports from modules.chart_generator")
        else:
            print("✗ App controller imports from different location")
            
    except Exception as e:
        print(f"✗ App controller import failed: {e}")
        return False
    
    return True

def test_function_execution():
    print("\n=== TESTING FUNCTION EXECUTION ===")
    
    try:
        import tkinter as tk
        from modules.chart_generator import create_tkinter_canvas
        import matplotlib.pyplot as plt
        import numpy as np
        
        # Create simple test
        fig, ax = plt.subplots()
        x = [1, 2, 3, 4, 5]
        y = [1, 4, 2, 3, 5]
        ax.plot(x, y)
        
        # Create minimal tkinter setup
        root = tk.Tk()
        root.withdraw()  # Hide window
        
        frame = tk.Frame(root)
        
        print("Calling create_tkinter_canvas...")
        canvas = create_tkinter_canvas(fig, frame)
        print("Function returned:", type(canvas))
        
        # Check if canvas has our features
        if hasattr(canvas, 'autoupdate'):
            print("✓ Canvas has autoupdate attribute (our feature)")
        else:
            print("✗ Canvas missing autoupdate attribute")
        
        root.destroy()
        plt.close(fig)
        
        return True
        
    except Exception as e:
        print(f"✗ Function execution failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = trace_imports()
    if success:
        test_function_execution()
    else:
        print("Cannot proceed with function test due to import failures")

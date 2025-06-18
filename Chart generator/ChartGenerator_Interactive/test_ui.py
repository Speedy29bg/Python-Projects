#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Simple test to check if the Interactive Chart Generator works
"""

import sys
import os
import tkinter as tk

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_basic_ui():
    """Test basic UI creation"""
    print("Testing basic UI creation...")
    
    try:
        root = tk.Tk()
        root.title("Test UI")
        root.geometry("800x600")
        
        # Test imports
        from core.app_controller import InteractiveChartApp
        
        # Try creating the app
        app = InteractiveChartApp(root)
        
        print("✓ UI created successfully!")
        print("Application window should be visible now.")
        print("Close the window to continue...")
        
        # Start the GUI (this will block until window is closed)
        root.mainloop()
        
        return True
        
    except Exception as e:
        print(f"✗ Error creating UI: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("="*50)
    print("INTERACTIVE CHART GENERATOR - UI TEST")
    print("="*50)
    
    success = test_basic_ui()
    
    if success:
        print("\\n✓ Test completed successfully!")
        print("The Interactive Chart Generator UI is working.")
    else:
        print("\\n✗ Test failed!")
        print("There are still issues to fix.")
    
    print("="*50)

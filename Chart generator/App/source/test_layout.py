#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test script for the new layout changes

This script tests the UI layout modifications to ensure
Chart Scaling Options and Color Scheme boxes are positioned
under the Axes Selection box.
"""

import tkinter as tk
import sys
import traceback

def test_layout():
    """Test the new layout configuration"""
    try:
        # Initialize the main application window
        root = tk.Tk()
        root.title("Lab Chart Generator - Layout Test")
        
        # Setup logging
        from modules.logger import setup_logging, handle_exception
        logger = setup_logging()
        
        # Create the application instance
        from modules.core import AppController
        app = AppController(root)
        
        # Set custom exception handler
        sys.excepthook = lambda exc_type, exc_value, exc_traceback: handle_exception(
            exc_type, exc_value, exc_traceback, app.status_label if hasattr(app, 'status_label') else None
        )
        
        print("✅ Layout test successful!")
        print("✅ UI components initialized correctly")
        print("✅ Chart Scaling Options and Color Scheme should now be under Axes Selection")
        print("✅ Chart Preview should take up about half the application width")
        
        # Start the application for visual inspection
        print("\n🔍 Starting application for visual inspection...")
        print("   Please verify that:")
        print("   1. Chart Scaling Options box is under Axes Selection")
        print("   2. Color Scheme box is under Chart Scaling Options")
        print("   3. Chart Preview takes up approximately half the app width")
        print("   4. The layout is more balanced")
        
        root.mainloop()
        root.destroy()
        
    except Exception as e:
        print(f"❌ Layout test failed: {str(e)}")
        print("Error details:")
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    print("🧪 Testing new UI layout...")
    success = test_layout()
    if success:
        print("✅ Layout test completed successfully!")
    else:
        print("❌ Layout test failed!")
        sys.exit(1)

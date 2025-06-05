"""
Simple Test Script for Chart Generator Application

This script tests creating an instance of the AppController class.
"""

import tkinter as tk
from modules.core import AppController

def run_test():
    print("Creating a Tkinter root window...")
    root = tk.Tk()
    root.title("Chart Generator Test")
    
    print("Creating an instance of AppController...")
    try:
        app = AppController(root)
        print("✓ Successfully created an instance of AppController")
        
        # Destroy the root window after 500ms (avoid opening GUI)
        root.after(500, root.destroy)
        root.mainloop()
        
    except Exception as e:
        print(f"✗ Failed to create an instance of AppController: {str(e)}")

if __name__ == "__main__":
    run_test()
    print("\nTest complete.")

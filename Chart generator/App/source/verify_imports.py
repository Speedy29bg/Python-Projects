"""
Verification Script for Chart Generator Refactored Module Structure

This script tests importing components from the refactored app_modules structure.
"""

def test_imports():
    print("Testing imports from the refactored module structure...")
    
    # Test core module
    try:
        from modules.core import AppController
        print("✓ Successfully imported AppController from modules.core")
    except Exception as e:
        print(f"✗ Failed to import AppController from modules.core: {str(e)}")
    
    # Test UI module
    try:
        from modules.app_modules.ui.main_window import MainWindow
        from modules.app_modules.ui.file_selection import FileSelectionFrame
        from modules.app_modules.ui.axes_selection import AxesSelectionFrame
        from modules.app_modules.ui.chart_options import ChartOptionsFrame
        from modules.app_modules.ui.preview_frame import PreviewFrame
        from modules.app_modules.ui.output_options import OutputOptionsFrame
        print("✓ Successfully imported UI components from modules.app_modules.ui")
    except Exception as e:
        print(f"✗ Failed to import UI components from modules.app_modules.ui: {str(e)}")
    
    # Test data module
    try:
        from modules.data import FileDataHandler
        print("✓ Successfully imported FileDataHandler from modules.data")
    except Exception as e:
        print(f"✗ Failed to import FileDataHandler from modules.data: {str(e)}")
    
    # Test utils module
    try:
        import modules.utils
        print("✓ Successfully imported modules.utils module")
    except Exception as e:
        print(f"✗ Failed to import modules.utils: {str(e)}")

if __name__ == "__main__":
    test_imports()
    print("\nVerification complete.")

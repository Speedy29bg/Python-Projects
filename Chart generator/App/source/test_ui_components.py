"""
Diagnostic script to test UI component initialization for the Chart Generator application
"""

import tkinter as tk
from modules.app_modules.ui import MainWindow, FileSelectionFrame, AxesSelectionFrame, ChartOptionsFrame, PreviewFrame, OutputOptionsFrame

def create_mock_app():
    """Create a mock application instance with the required methods"""
    
    class MockApp:
        def select_files(self):
            print("select_files called")
        
        def preview_data(self):
            print("preview_data called")
            
        def analyze_data(self):
            print("analyze_data called")
            
        def update_preview(self):
            print("update_preview called")
            
        def generate_charts(self):
            print("generate_charts called")
            
        def export_current_chart(self):
            print("export_current_chart called")
            
        def clear_selections(self):
            print("clear_selections called")
    
    return MockApp()

def test_ui_components():
    """Test initializing all UI components with a mock app instance"""
    print("Testing UI components initialization...")
    
    root = tk.Tk()
    root.title("UI Components Test")
    mock_app = create_mock_app()
    
    # Test MainWindow
    try:
        main_window = MainWindow(root)
        print("✓ Successfully created MainWindow")
        
        # Create frames for other components
        top_frame = tk.Frame(root)
        middle_frame = tk.Frame(root)
        chart_frame = tk.Frame(root)
        bottom_frame = tk.Frame(root)
        
        # Test FileSelectionFrame
        try:
            file_frame = FileSelectionFrame(top_frame, mock_app)
            print("✓ Successfully created FileSelectionFrame")
        except Exception as e:
            print(f"✗ Failed to create FileSelectionFrame: {str(e)}")
        
        # Test AxesSelectionFrame
        try:
            axes_frame = AxesSelectionFrame(middle_frame, mock_app)
            print("✓ Successfully created AxesSelectionFrame")
        except Exception as e:
            print(f"✗ Failed to create AxesSelectionFrame: {str(e)}")
        
        # Test ChartOptionsFrame
        try:
            chart_options = ChartOptionsFrame(middle_frame, mock_app)
            print("✓ Successfully created ChartOptionsFrame")
        except Exception as e:
            print(f"✗ Failed to create ChartOptionsFrame: {str(e)}")
        
        # Test PreviewFrame
        try:
            preview_frame = PreviewFrame(chart_frame, mock_app)
            print("✓ Successfully created PreviewFrame")
        except Exception as e:
            print(f"✗ Failed to create PreviewFrame: {str(e)}")
        
        # Test OutputOptionsFrame
        try:
            output_frame = OutputOptionsFrame(bottom_frame, mock_app)
            print("✓ Successfully created OutputOptionsFrame")
        except Exception as e:
            print(f"✗ Failed to create OutputOptionsFrame: {str(e)}")
        
    except Exception as e:
        print(f"✗ Failed to create MainWindow: {str(e)}")
    
    # Destroy the root window after a short delay
    root.after(500, root.destroy)
    root.mainloop()

if __name__ == "__main__":
    test_ui_components()
    print("\nUI component test complete.")

#!/usr/bin/env python
"""
Minimal test to show interactive chart features working
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.getcwd())

try:
    print("Starting test...")
    
    import matplotlib
    matplotlib.use('TkAgg')  # Ensure we use TkAgg backend
    
    import tkinter as tk
    from tkinter import ttk
    import matplotlib.pyplot as plt
    import numpy as np
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
    
    print("Basic imports successful")
    
    # Test the enhanced function directly
    def create_interactive_canvas(figure, frame):
        """Test version of create_tkinter_canvas with interactive features"""
        
        # Clear frame first
        for widget in frame.winfo_children():
            widget.destroy()
        
        # Create main frame for chart and controls
        chart_frame = ttk.Frame(frame)
        chart_frame.pack(fill='both', expand=True)
        
        # Create chart area
        canvas = FigureCanvasTkAgg(figure, master=chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)
        
        # Add navigation toolbar
        toolbar_frame = ttk.Frame(chart_frame)
        toolbar_frame.pack(fill='x', pady=2)
        toolbar = NavigationToolbar2Tk(canvas, toolbar_frame)
        toolbar.update()
        
        # Create interactive controls
        button_frame = ttk.Frame(chart_frame)
        button_frame.pack(fill='x', pady=5)
        
        # Grid toggle
        grid_var = tk.BooleanVar(value=True)
        def toggle_grid():
            for ax in figure.get_axes():
                ax.grid(grid_var.get())
            canvas.draw()
        
        ttk.Checkbutton(button_frame, text="Grid", variable=grid_var, 
                       command=toggle_grid).pack(side='left', padx=5)
        
        # Points toggle
        points_var = tk.BooleanVar(value=True)
        def toggle_points():
            for ax in figure.get_axes():
                for line in ax.get_lines():
                    line.set_marker('.' if points_var.get() else '')
            canvas.draw()
        
        ttk.Checkbutton(button_frame, text="Points", variable=points_var, 
                       command=toggle_points).pack(side='left', padx=5)
        
        # Legend toggle
        legend_var = tk.BooleanVar(value=True)
        def toggle_legend():
            for ax in figure.get_axes():
                legend = ax.get_legend()
                if legend:
                    legend.set_visible(legend_var.get())
            canvas.draw()
        
        ttk.Checkbutton(button_frame, text="Legend", variable=legend_var, 
                       command=toggle_legend).pack(side='left', padx=5)
        
        # Coordinate display
        coord_var = tk.StringVar(value="Click for coordinates")
        coord_label = ttk.Label(button_frame, textvariable=coord_var, foreground="blue")
        coord_label.pack(side='left', padx=10)
        
        def on_click(event):
            if event.inaxes:
                coord_var.set(f"X: {event.xdata:.3f}, Y: {event.ydata:.3f}")
        
        canvas.mpl_connect('button_press_event', on_click)
        
        return canvas
    
    # Create test window
    print("Creating test window...")
    root = tk.Tk()
    root.title("Interactive Chart Test - Should show controls below chart")
    root.geometry("800x600")
    
    # Create test data
    fig, ax = plt.subplots(figsize=(8, 4))
    x = np.linspace(0, 10, 100)
    y1 = np.sin(x)
    y2 = np.cos(x)
    ax.plot(x, y1, label='Sine', marker='o', markersize=3)
    ax.plot(x, y2, label='Cosine', marker='s', markersize=3)
    ax.set_xlabel('X axis')
    ax.set_ylabel('Y axis')
    ax.legend()
    ax.grid(True)
    ax.set_title('Interactive Chart Test\nYou should see navigation toolbar and control buttons below')
    
    # Create frame
    main_frame = ttk.Frame(root)
    main_frame.pack(fill='both', expand=True, padx=10, pady=10)
    
    info_label = ttk.Label(main_frame, text="Interactive features should appear below the chart:", 
                          font=('Arial', 12, 'bold'))
    info_label.pack(pady=5)
    
    chart_frame = ttk.Frame(main_frame)
    chart_frame.pack(fill='both', expand=True)
    
    # Create interactive canvas
    print("Creating interactive canvas...")
    canvas = create_interactive_canvas(fig, chart_frame)
    print("Canvas created! Interactive controls should be visible.")
    
    # Add instructions
    instructions = ttk.Label(main_frame, 
                           text="Test: Toggle grid/points/legend buttons, use toolbar to zoom/pan, click chart for coordinates",
                           wraplength=600)
    instructions.pack(pady=5)
    
    root.mainloop()

except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
    input("Press Enter to exit...")

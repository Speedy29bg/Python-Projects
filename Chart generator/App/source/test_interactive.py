#!/usr/bin/env python
"""Quick test to see if interactive features are working"""

import tkinter as tk
from modules.chart_generator import create_tkinter_canvas
import matplotlib.pyplot as plt
import numpy as np

def test_interactive_features():
    # Create test data and figure
    fig, ax = plt.subplots(figsize=(10, 6))
    x = np.linspace(0, 10, 50)
    y1 = np.sin(x)
    y2 = np.cos(x)
    ax.plot(x, y1, label='Sine', marker='o')
    ax.plot(x, y2, label='Cosine', marker='s')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.legend()
    ax.grid(True)

    # Create tkinter window
    root = tk.Tk()
    root.title('Interactive Features Test')
    root.geometry('800x700')
    
    frame = tk.Frame(root)
    frame.pack(fill='both', expand=True, padx=10, pady=10)

    # Test the canvas creation
    print("Creating interactive canvas...")
    canvas = create_tkinter_canvas(fig, frame)
    print("Canvas created! Check for interactive controls in the window.")

    root.mainloop()

if __name__ == "__main__":
    test_interactive_features()

"""
Figure Management Module

This module provides functions for managing matplotlib figures.


Author: Speedy29bg
"""

import matplotlib.pyplot as plt

def clear_figure(figure, canvas):
    """Clear the existing figure and canvas
    
    Args:
        figure: The matplotlib figure object
        canvas: The Tkinter canvas widget
        
    Returns:
        tuple: (None, None) representing cleared figure and canvas
    """
    if canvas:
        canvas.get_tk_widget().pack_forget()
    
    if figure:
        plt.close(figure)
    
    return None, None

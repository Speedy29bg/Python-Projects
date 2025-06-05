"""
Figure Export Module

This module provides functions for exporting matplotlib figures to various file formats.

Author: Lab Chart Tools Team
"""

import logging
from typing import Any

def export_figure(figure: Any, filename: str, format_type: str = 'png') -> bool:
    """Export a matplotlib figure to a file
    
    Args:
        figure: Matplotlib figure object
        filename: Output filename
        format_type: File format ('png', 'pdf', etc.)
        
    Returns:
        bool: True if export was successful, False otherwise
    """
    try:
        # Make sure filename has the correct extension
        if not filename.lower().endswith(f'.{format_type.lower()}'):
            filename = f"{filename}.{format_type.lower()}"
            
        # Save the figure
        figure.savefig(
            filename, 
            format=format_type.lower(),
            dpi=300,  # High resolution
            bbox_inches='tight'  # Trim whitespace
        )
        
        logging.info(f"Exported figure to {filename}")
        return True
        
    except Exception as e:
        logging.error(f"Error exporting figure to {filename}: {str(e)}")
        return False

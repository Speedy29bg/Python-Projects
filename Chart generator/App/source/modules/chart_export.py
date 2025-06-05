"""
Chart export utilities for the Lab Chart Generator

This module contains functions for exporting charts to different formats
such as images (PNG), PDF documents, and Excel files with embedded charts.

Author: Lab Chart Tools Team
"""

import matplotlib.pyplot as plt
import os
import logging
from typing import List, Dict, Optional, Any, Union

def export_chart_to_image(figure, output_path, format_type='png', dpi=300):
    """Export a matplotlib chart to an image file
    
    Args:
        figure: The matplotlib figure object
        output_path: Path where to save the image
        format_type: Image format (png, jpg, etc.)
        dpi: Resolution in dots per inch
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Ensure output directory exists
        output_dir = os.path.dirname(output_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        # Save with high quality
        figure.savefig(
            output_path,
            format=format_type,
            dpi=dpi,
            bbox_inches='tight'
        )
        logging.info(f"Chart exported as image to {output_path}")
        return True
    except Exception as e:
        logging.error(f"Error exporting chart to image: {str(e)}")
        return False

def export_chart_to_pdf(figure, output_path, dpi=300):
    """Export a matplotlib chart to a PDF document
    
    Args:
        figure: The matplotlib figure object
        output_path: Path where to save the PDF
        dpi: Resolution in dots per inch
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Ensure output directory exists
        output_dir = os.path.dirname(output_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        # Save with high quality
        figure.savefig(
            output_path,
            format='pdf',
            dpi=dpi,
            bbox_inches='tight'
        )
        logging.info(f"Chart exported as PDF to {output_path}")
        return True
    except Exception as e:
        logging.error(f"Error exporting chart to PDF: {str(e)}")
        return False

def export_multiple_charts_to_pdf(figures, output_path, dpi=300):
    """Export multiple matplotlib charts to a single PDF document
    
    Args:
        figures: List of matplotlib figure objects
        output_path: Path where to save the PDF
        dpi: Resolution in dots per inch
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Ensure output directory exists
        output_dir = os.path.dirname(output_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        # Save all figures to a single PDF
        from matplotlib.backends.backend_pdf import PdfPages
        with PdfPages(output_path) as pdf:
            for figure in figures:
                pdf.savefig(figure, dpi=dpi, bbox_inches='tight')
                
        logging.info(f"Multiple charts exported to PDF {output_path}")
        return True
    except Exception as e:
        logging.error(f"Error exporting multiple charts to PDF: {str(e)}")
        return False
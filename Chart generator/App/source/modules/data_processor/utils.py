"""
Data Processor Utility Functions

This module provides utility functions for data processing tasks.


Author: Speedy29bg
"""

import re

def create_safe_sheet_name(base_name: str) -> str:
    """Create a safe sheet name for Excel by removing invalid characters
    
    Args:
        base_name: Original file name to convert to sheet name
        
    Returns:
        str: A sanitized sheet name compatible with Excel requirements
    """
    safe_name = re.sub(r'[\\/*?:"<>|]', '_', base_name)
    return safe_name[:31]  # Excel sheet name limit is 31 characters

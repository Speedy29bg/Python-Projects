"""
User interface component utilities for the Lab Chart Generator

This module is a facade over the more detailed ui_components_module.

Author: Lab Chart Tools Team
"""

from modules.ui_components_module import (
    create_loading_indicator,
    create_progress_dialog,
    create_data_preview,
    populate_listbox,
    get_listbox_selections
)

__all__ = [
    'create_loading_indicator',
    'create_progress_dialog',
    'create_data_preview',
    'populate_listbox',
    'get_listbox_selections'
]

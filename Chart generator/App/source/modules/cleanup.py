"""
Cleanup Module

This module provides functionality to clean up temporary files and caches
when the application closes.

Author: Speedy29bg
"""

import os
import shutil
import logging
from pathlib import Path
from typing import List, Optional


def find_pycache_directories(root_path: str) -> List[str]:
    """
    Find all __pycache__ directories in the given root path and its subdirectories.
    
    Args:
        root_path: The root directory to search from
        
    Returns:
        List of paths to __pycache__ directories
    """
    pycache_dirs = []
    
    try:
        for root, dirs, files in os.walk(root_path):
            if '__pycache__' in dirs:
                pycache_path = os.path.join(root, '__pycache__')
                pycache_dirs.append(pycache_path)
                
    except Exception as e:
        logging.warning(f"Error searching for __pycache__ directories: {e}")
        
    return pycache_dirs


def remove_pycache_directory(pycache_path: str) -> bool:
    """
    Remove a single __pycache__ directory and all its contents.
    
    Args:
        pycache_path: Path to the __pycache__ directory to remove
        
    Returns:
        True if successfully removed, False otherwise
    """
    try:
        if os.path.exists(pycache_path) and os.path.isdir(pycache_path):
            shutil.rmtree(pycache_path)
            logging.info(f"Removed __pycache__ directory: {pycache_path}")
            return True
    except Exception as e:
        logging.warning(f"Failed to remove __pycache__ directory {pycache_path}: {e}")
        
    return False


def cleanup_pycache_files(root_path: Optional[str] = None) -> int:
    """
    Clean up all __pycache__ directories from the application directory and subdirectories.
    
    Args:
        root_path: The root directory to clean from. If None, uses the current script's directory.
        
    Returns:
        Number of __pycache__ directories successfully removed
    """
    if root_path is None:
        # Get the directory where the current script is located
        root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    logging.info(f"Starting cleanup of __pycache__ files from: {root_path}")
    
    # Find all __pycache__ directories
    pycache_dirs = find_pycache_directories(root_path)
    
    if not pycache_dirs:
        logging.info("No __pycache__ directories found")
        return 0
    
    # Remove each __pycache__ directory
    removed_count = 0
    for pycache_dir in pycache_dirs:
        if remove_pycache_directory(pycache_dir):
            removed_count += 1
    
    logging.info(f"Cleanup complete: {removed_count}/{len(pycache_dirs)} __pycache__ directories removed")
    return removed_count


def cleanup_temp_files(root_path: Optional[str] = None) -> int:
    """
    Clean up other temporary files like .pyc files that might be outside __pycache__.
    
    Args:
        root_path: The root directory to clean from. If None, uses the current script's directory.
        
    Returns:
        Number of temporary files successfully removed
    """
    if root_path is None:
        root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    removed_count = 0
    
    try:
        for root, dirs, files in os.walk(root_path):
            for file in files:
                if file.endswith('.pyc') or file.endswith('.pyo'):
                    file_path = os.path.join(root, file)
                    try:
                        os.remove(file_path)
                        logging.info(f"Removed temporary file: {file_path}")
                        removed_count += 1
                    except Exception as e:
                        logging.warning(f"Failed to remove temporary file {file_path}: {e}")
                        
    except Exception as e:
        logging.warning(f"Error searching for temporary files: {e}")
    
    return removed_count


def full_cleanup(root_path: Optional[str] = None) -> dict:
    """
    Perform a full cleanup of all temporary files and caches.
    
    Args:
        root_path: The root directory to clean from. If None, uses the current script's directory.
        
    Returns:
        Dictionary with cleanup results
    """
    results = {
        'pycache_dirs_removed': 0,
        'temp_files_removed': 0,
        'total_items_removed': 0
    }
    
    try:
        # Clean up __pycache__ directories
        results['pycache_dirs_removed'] = cleanup_pycache_files(root_path)
        
        # Clean up other temporary files
        results['temp_files_removed'] = cleanup_temp_files(root_path)
        
        # Calculate total
        results['total_items_removed'] = results['pycache_dirs_removed'] + results['temp_files_removed']
        
        logging.info(f"Full cleanup completed: {results}")
        
    except Exception as e:
        logging.error(f"Error during full cleanup: {e}")
    
    return results


def register_cleanup_on_exit():
    """
    Register cleanup functions to run when the program exits.
    """
    import atexit
    
    def cleanup_handler():
        """Handler function to run cleanup on exit"""
        logging.info("Running cleanup on program exit...")
        try:
            results = full_cleanup()
            if results['total_items_removed'] > 0:
                print(f"Cleanup completed: Removed {results['pycache_dirs_removed']} __pycache__ directories and {results['temp_files_removed']} temporary files")
        except Exception as e:
            logging.error(f"Error during exit cleanup: {e}")
    
    # Register the cleanup handler
    atexit.register(cleanup_handler)
    logging.info("Cleanup handler registered for program exit")

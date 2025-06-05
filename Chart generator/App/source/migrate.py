#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Chart Generator Migration Script

This script handles the migration from the original monolithic ChartGenerator.py
to the new modular implementation.

Author: Lab Chart Tools Team
Date: May 30, 2025
"""

import os
import sys
import shutil
import argparse
import datetime

def backup_file(file_path):
    """Create a backup of the specified file"""
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = f"{file_path}.bak_{timestamp}"
    
    if os.path.exists(file_path):
        shutil.copy2(file_path, backup_path)
        print(f"✅ Created backup: {backup_path}")
        return True
    else:
        print(f"❌ Source file not found: {file_path}")
        return False

def replace_implementation(source_path, target_path, create_backup=True):
    """Replace target file with source file"""
    # Check if source exists
    if not os.path.exists(source_path):
        print(f"❌ Source file not found: {source_path}")
        return False
    
    # Create backup if requested
    if create_backup and os.path.exists(target_path):
        if not backup_file(target_path):
            return False
    
    # Replace file
    shutil.copy2(source_path, target_path)
    print(f"✅ Replaced: {target_path} with {source_path}")
    return True

def main():
    """Main migration function"""
    parser = argparse.ArgumentParser(description="Migrate from monolithic to modular implementation")
    parser.add_argument("--no-backup", action="store_true", help="Skip backup creation")
    parser.add_argument("--migration-method", choices=["replace", "rename"], default="replace", 
                      help="Method for migration (replace or rename)")
    args = parser.parse_args()
    
    # Define file paths
    current_dir = os.path.dirname(os.path.abspath(__file__))
    source_path = os.path.join(current_dir, "ChartGenerator_new.py")
    target_path = os.path.join(current_dir, "ChartGenerator.py")
    
    print("=" * 80)
    print("CHART GENERATOR MIGRATION SCRIPT".center(80))
    print("=" * 80)
    print(f"Source: {source_path}")
    print(f"Target: {target_path}")
    print(f"Backup: {'Disabled' if args.no_backup else 'Enabled'}")
    print(f"Method: {args.migration_method}")
    print("=" * 80)
    
    # Confirm action
    if not args.no_backup:
        confirm = input("This will create a backup and replace the original implementation. Continue? (y/n): ")
        if confirm.lower() != 'y':
            print("Migration cancelled.")
            return
    else:
        confirm = input("⚠️ WARNING: No backup will be created. Continue? (y/n): ")
        if confirm.lower() != 'y':
            print("Migration cancelled.")
            return
    
    # Perform migration
    if args.migration_method == "replace":
        # Copy new implementation over old one
        if replace_implementation(source_path, target_path, not args.no_backup):
            print("✅ Migration completed successfully")
    else:  # rename method
        # Rename files
        if os.path.exists(target_path) and not args.no_backup:
            backup_file(target_path)
        
        try:
            os.rename(source_path, target_path)
            print(f"✅ Renamed {source_path} to {target_path}")
            print("✅ Migration completed successfully")
        except Exception as e:
            print(f"❌ Error during file rename: {str(e)}")
    
    print("\nReminder: Verify the application functionality after migration.")

if __name__ == "__main__":
    main()

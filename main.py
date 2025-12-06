#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Soplos Welcome 2.0 - The world's most advanced welcome application for Linux

Main entry point for the application.
"""

import sys
import os
import warnings
from pathlib import Path
import atexit
import shutil

# Add project root to Python path
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

# Suppress accessibility warnings for cleaner output
warnings.filterwarnings('ignore', '.*Couldn\'t connect to accessibility bus.*', Warning)
warnings.filterwarnings('ignore', '.*Failed to connect to socket.*', Warning)

# Disable accessibility bridge if not explicitly enabled
if not os.environ.get('ENABLE_ACCESSIBILITY'):
    os.environ['NO_AT_BRIDGE'] = '1'
    os.environ['AT_SPI_BUS'] = '0'


def cleanup_pycache():
    """Remove all __pycache__ directories on exit."""
    try:
        for root, dirs, files in os.walk(PROJECT_ROOT):
            if '__pycache__' in dirs:
                pycache_path = os.path.join(root, '__pycache__')
                shutil.rmtree(pycache_path, ignore_errors=True)
    except Exception:
        pass  # Silent cleanup, don't interrupt exit


# Register cleanup function to run on exit
atexit.register(cleanup_pycache)


def main():
    """Main entry point for Soplos Welcome."""
    try:
        # Import and run the application
        from core import run_application
        return run_application()
        
    except ImportError as e:
        print(f"Import error: {e}")
        print("Please ensure all dependencies are installed:")
        print("  sudo apt install python3-gi python3-gi-cairo gir1.2-gtk-3.0")
        return 1
        
    except Exception as e:
        print(f"Application error: {e}")
        return 1


if __name__ == '__main__':
    sys.exit(main())
    
#!/usr/bin/env python3
"""
Test runner for Soplos Welcome development.
Run this to test the application during development.
"""

import sys
import os
from pathlib import Path

# Add project root to Python path
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

print("🚀 Starting Soplos Welcome 2.0 - Development Mode")
print(f"📁 Project root: {PROJECT_ROOT}")

# Check dependencies
try:
    import gi
    gi.require_version('Gtk', '3.0')
    from gi.repository import Gtk
    print("✅ GTK dependencies available")
except ImportError as e:
    print(f"❌ Missing GTK dependencies: {e}")
    print("Install with: sudo apt install python3-gi python3-gi-cairo gir1.2-gtk-3.0")
    sys.exit(1)

# Set debug mode
os.environ['SOPLOS_DEBUG'] = '1'

# Run the application
if __name__ == '__main__':
    try:
        from main import main
        print("🎯 Launching application...")
        sys.exit(main())
    except Exception as e:
        print(f"💥 Error running application: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

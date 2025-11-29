# Soplos Welcome 2.0 - Project Structure

## 📁 Directory Structure

```
soplos-welcome/
├── main.py                          # 🚀 Application entry point
├── run_dev.py                       # 🧪 Development test runner  
├── CHANGELOG.md                     # 📝 Version history
├── README.md                        # 📚 Main documentation
├── core/                           # 🏗️ Core application logic
│   ├── __init__.py                 # Core module exports
│   ├── application.py              # Main GTK application class
│   ├── environment.py              # Desktop environment detection
│   ├── theme_manager.py            # CSS theme management system
│   └── i18n_manager.py             # GNU Gettext internationalization
├── ui/                             # 🎨 User Interface Components
│   ├── __init__.py                 # UI constants and CSS classes
│   ├── main_window.py              # Main application window
│   ├── tabs/                       # Application tabs
│   │   ├── __init__.py
│   │   ├── welcome_tab.py          # Welcome/system info tab
│   │   ├── software_tab.py         # Smart software management router
│   │   ├── software_gnome_tab.py   # GNOME-optimized software tab
│   │   ├── software_plasma_tab.py  # KDE Plasma-optimized software tab
│   │   ├── software_xfce_tab.py    # XFCE-optimized software tab
│   │   ├── drivers_tab.py          # Hardware drivers management
│   │   ├── kernels_tab.py          # Kernel management
│   │   ├── customization_tab.py    # Desktop customization
│   │   └── recommended_tab.py      # Curated app recommendations
│   ├── widgets/                    # 🧩 Reusable UI components
│   │   └── __init__.py             # Widget exports (placeholder)
│   └── dialogs/                    # 💬 Dialog windows
│       └── __init__.py             # Dialog exports (placeholder)
├── assets/                         # 🎭 Static resources
│   ├── themes/                     # CSS styling system
│   │   ├── base.css                # Base elegant theme styles
│   │   ├── light.css               # Light theme with imports
│   │   └── dark.css                # Dark theme with overrides
│   └── icons/                      # Application icons library
│       ├── com.soplos.welcome.png  # Main app icon
│       ├── slide1.png              # Welcome slide
│       ├── soplos-logo.png         # Soplos Linux logo
│       ├── README.md               # Icon documentation
│       ├── 48x48/                  # Icon size variants
│       ├── 64x64/
│       ├── 128x128/
│       ├── browsers/               # Browser application icons
│       ├── comunications/          # Communication app icons  
│       ├── developer/              # Development tool icons
│       ├── gaming/                 # Gaming application icons
│       ├── graphics/               # Graphics software icons
│       ├── hardware/               # Hardware component icons
│       ├── multimedia/             # Media application icons
│       ├── office/                 # Office suite icons
│       ├── software/               # Software manager icons
│       └── soplos/                 # Soplos-specific tool icons
├── locale/                         # 🌍 Internationalization
│   ├── template.pot                # Translation template
│   ├── es/LC_MESSAGES/            # Spanish translations (.po/.mo)
│   ├── en/LC_MESSAGES/            # English translations
│   ├── fr/LC_MESSAGES/            # French translations
│   ├── de/LC_MESSAGES/            # German translations
│   ├── pt/LC_MESSAGES/            # Portuguese translations
│   ├── it/LC_MESSAGES/            # Italian translations
│   ├── ro/LC_MESSAGES/            # Romanian translations
│   └── ru/LC_MESSAGES/            # Russian translations
├── config/                         # ⚙️ Configuration management
│   ├── __init__.py                 # Config module exports
│   ├── paths.py                    # Application path configuration
│   └── software.py                 # Software package definitions
├── utils/                          # 🔧 Utility functions
│   ├── __init__.py                 # Utility exports
│   └── command_runner.py           # System command execution
├── services/                       # 🔌 Business logic services
│   └── __init__.py                 # Service layer (placeholder)
├── tests/                          # 🧪 Test suite
│   └── __init__.py                 # Test framework (placeholder)
├── docs/                           # � Documentation
│   └── (empty - documentation TBD)
└── debian/                         # 📦 Debian packaging
    └── com.soplos.welcome.metainfo.xml  # AppStream metadata
```

## 🎯 Architecture Overview

### Core Layer (🏗️)
- **application.py**: Main GTK Application lifecycle management
- **environment.py**: Smart desktop environment detection (GNOME/KDE/XFCE)
- **theme_manager.py**: CSS-based theming with automatic dark/light detection
- **i18n_manager.py**: GNU Gettext internationalization with 8 language support

### UI Layer (🎨)  
- **main_window.py**: Central window with HeaderBar, tabs, and status management
- **tabs/**: Modular tab system with desktop-specific software management
- **widgets/**: Reusable UI components (planned expansion)
- **dialogs/**: Modal dialogs for user interactions (planned expansion)

### Assets & Resources (🎭)
- **CSS Theme System**: Base styles with elegant tab design and theme inheritance
- **Icon Library**: Comprehensive icon collection for 400+ applications
- **Multi-resolution**: Icon variants for different display densities

### Configuration (⚙️)
- **Path Management**: Centralized path configuration for all assets
- **Software Definitions**: Categorized software package configurations
- **Desktop Integration**: Environment-specific customizations

## 🚀 Key Features Implemented

### ✅ Universal Desktop Support
- **GNOME**: Native HeaderBar integration with modern styling
- **KDE Plasma**: Plasma-specific software management integration  
- **XFCE**: Traditional window decorations with HeaderBar fallback
- **X11 & Wayland**: Full compatibility with both display protocols

### ✅ Professional Internationalization
- **8 Languages**: ES, EN, FR, DE, PT, IT, RO, RU with GNU Gettext
- **Dynamic Loading**: Runtime language switching with .mo files
- **Context Awareness**: Proper pluralization and context handling

### ✅ Advanced Theming System
- **CSS-Based**: Professional styling with elegant tab design
- **Auto-Detection**: Follows system dark/light theme preferences
- **Theme Inheritance**: Base styles with dark/light overrides
- **Desktop Specific**: Optimized themes for each environment

### ✅ Intelligent Software Management
- **Smart Routing**: Automatically selects appropriate software manager
- **Multiple Backends**: APT, Flatpak, Snap, and native software centers
- **Desktop Integration**: Uses Discover (KDE), GNOME Software, or traditional tools
- **Progress Tracking**: Real-time installation progress with status updates

### 🔄 Currently Active Issues
- **HeaderBar Controls**: Window controls not showing in XFCE environment
- **Tab Styling**: Blue accent color needs adjustment for elegance
- **Traditional Fallback**: Manual window controls implementation needed

## 🎨 Design Principles

- **Modular Architecture**: Clean separation of concerns with focused components
- **Desktop Agnostic**: Universal compatibility without environment lock-in  
- **Professional Standards**: Industry-standard GNU Gettext and CSS theming
- **Elegant UI**: Sophisticated tab design with subtle transitions
- **Performance**: Efficient resource usage with lazy loading
- **Maintainable**: Small, focused modules with clear responsibilities

---
*The world's most advanced welcome application for Linux distributions! 🌍*

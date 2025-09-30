# 📁 Project Structure

```
EasyKiConverter/
├── config/                            # Configuration directory
├── docs/                              # Detailed documentation directory
│   ├── README.md                     # Documentation index
│   ├── project_structure.md          # Detailed project structure
│   ├── development_guide.md          # Development guide
│   ├── contributing.md               # Contributing guidelines
│   ├── performance.md                # Performance optimization
│   ├── system_requirements.md        # System requirements
│   ├── project_structure_en.md       # Project structure (English)
│   ├── development_guide_en.md       # Development guide (English)
│   ├── contributing_en.md            # Contributing guidelines (English)
│   ├── performance_en.md             # Performance optimization (English)
│   └── system_requirements_en.md     # System requirements (English)
├── scripts/                           # Scripts directory
├── src/                               # Source code directory
│   ├── __init__.py                   # Python package initialization file
│   ├── main.py                       # Command-line tool main entry
│   ├── package_manager.py            # Package manager
│   ├── core/                         # Core conversion engine
│   │   ├── __init__.py              # Python package initialization file
│   │   ├── easyeda/                 # EasyEDA API and data processing
│   │   │   ├── __init__.py         # Python package initialization file
│   │   │   ├── easyeda_api.py      # EasyEDA API client
│   │   │   ├── easyeda_importer.py # Data importers
│   │   │   └── parameters_easyeda.py # EasyEDA parameter definitions
│   │   ├── kicad/                   # KiCad export engines
│   │   │   ├── __init__.py         # Python package initialization file
│   │   │   ├── export_kicad_symbol.py # Symbol exporter
│   │   │   ├── export_kicad_footprint.py # Footprint exporter
│   │   │   ├── export_kicad_3d_model.py # 3D model exporter
│   │   │   ├── parameters_kicad_footprint.py # KiCad footprint parameter definitions
│   │   │   └── parameters_kicad_symbol.py # KiCad symbol parameter definitions
│   │   └── utils/                   # Shared utility functions
│   │       ├── __init__.py         # Python package initialization file
│   │       ├── build_pyqt6_ui.py   # PyQt6 UI build tool
│   │       ├── geometry_utils.py   # Geometry utility functions
│   │       ├── quick_build.py      # Quick build tool
│   │       └── symbol_lib_utils.py # Symbol library utility functions
│   └── ui/                          # User interfaces
│       ├── __init__.py             # Python package initialization file
│       └── pyqt6/                  # PyQt6 desktop application
│           ├── __init__.py        # Python package initialization file
│           ├── main.py            # PyQt6 UI main entry
│           ├── modern_main_window.py # Modern main window
│           ├── ultimate_main_window.py # Ultimate main window
│           ├── user_config.json   # User configuration file
│           ├── resources/         # Resource files directory
│           ├── utils/             # UI utility functions
│           │   ├── __init__.py    # Python package initialization file
│           │   ├── bom_parser.py  # BOM file parser
│           │   ├── component_validator.py # Component validator
│           │   ├── config_manager.py # Configuration manager
│           │   ├── modern_style.py # Modern style
│           │   ├── modern_ui_components.py # Modern UI components
│           │   ├── responsive_layout.py # Responsive layout
│           │   ├── style_manager.py # Style manager
│           │   └── ui_effects.py  # UI effects
│           ├── widgets/           # UI components
│           │   ├── __init__.py    # Python package initialization file
│           │   ├── component_input_widget.py # Component input widget
│           │   ├── modern_component_input_widget.py # Modern component input widget
│           │   ├── navigation_widget.py # Navigation widget
│           │   ├── optimized_component_input_widget.py # Optimized component input widget
│           │   ├── progress_widget.py # Progress widget
│           │   └── results_widget.py # Results display widget
│           └── workers/           # Worker threads
│               ├── __init__.py    # Python package initialization file
│               └── export_worker.py # Export worker thread
├── tests/                             # Tests directory
├── build_conf/                        # Build configuration directory
│   ├── build.spec                    # PyInstaller build configuration
│   └── requirements_app.txt          # Application dependencies
├── start_webui.bat                    # Windows Web UI startup script
├── LICENSE                           # GPL-3.0 license
├── README.md                         # Chinese documentation
├── README_en.md                      # English documentation
└── .gitignore                       # Git ignore rules
```

## 📋 Core Module Description

### 🎯 Command Line Tools
| File | Function Description |
|------|----------------------|
| **src/main.py** | Command-line interface main entry, handles parameter parsing, validation, and coordinates the entire conversion process |

### 🖥️ PyQt6 UI Interface
| File | Function Description |
|------|----------------------|
| **src/ui/pyqt6/main.py** | PyQt6 UI main entry, contains main business logic |
| **src/ui/pyqt6/modern_main_window.py** | Modern main window interface |
| **src/ui/pyqt6/widgets/** | Various UI components |
| **src/ui/pyqt6/utils/** | UI utility functions and style management |

### 🌐 Web UI Interface
| File | Function Description |
|------|----------------------|
| **src/Web_Ui/app.py** | Flask web application main program, provides REST API and static file services |
| **src/Web_Ui/index.html** | Main page, modern user interface with drag-and-drop and real-time feedback |
| **src/Web_Ui/css/styles.css** | Style files, frosted glass effects and responsive design |
| **src/Web_Ui/js/script.js** | Frontend interaction scripts, handles form submission, progress display, and result presentation |

### 📚 Documentation Directory
| File | Function Description |
|------|----------------------|
| **docs/README.md** | Documentation index, provides links and brief descriptions for all documents |
| **docs/project_structure.md** | Detailed project structure and module descriptions |
| **docs/development_guide.md** | Development environment setup and workflow guide |
| **docs/contributing.md** | Project contribution process and guidelines |
| **docs/performance.md** | Multi-threading parallel processing and performance optimization |
| **docs/system_requirements.md** | System requirements and supported component types |

### 🔧 Core Engine
| Module | Function Description |
|--------|----------------------|
| **src/core/easyeda/** | EasyEDA API client and data processing modules |
| **src/core/kicad/** | KiCad format export engines, supports symbols, footprints, and 3D models |
| **src/core/utils/** | Shared utility functions modules |

### 📦 Data Processing Flow
1. **API Retrieval**: Get component data from EasyEDA/LCSC
2. **Data Parsing**: Parse symbol, footprint, and 3D model information
3. **Format Conversion**: Convert to KiCad compatible format
4. **File Generation**: Output .kicad_sym, .kicad_mod and other files
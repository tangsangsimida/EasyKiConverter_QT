# 📁 Project Structure

```
EasyKiConverter/
├── EasyKiConverter/                    # Core conversion engine
│   ├── main.py                        # Command-line tool main entry
│   ├── helpers.py                     # Utility functions and helpers
│   ├── easyeda/                       # EasyEDA API and data processing
│   │   ├── easyeda_api.py            # EasyEDA API client
│   │   ├── easyeda_importer.py       # Data importers
│   │   └── parameters_easyeda.py     # EasyEDA parameter definitions
│   ├── kicad/                        # KiCad export engines
│   │   ├── export_kicad_symbol.py    # Symbol exporter
│   │   ├── export_kicad_footprint.py # Footprint exporter
│   │   ├── export_kicad_3d_model.py  # 3D model exporter
│   │   └── parameters_kicad_symbol.py # KiCad parameter definitions
│   └── Web_Ui/                       # Web user interface
│       ├── app.py                    # Flask web application
│       ├── index.html                # Main page
│       ├── css/styles.css            # Style files
│       ├── js/script.js              # Frontend scripts
│       ├── imgs/background.jpg       # Background images
│       └── requirements.txt          # Web UI dependencies
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
├── start_webui.bat                    # Windows startup script
├── LICENSE                           # GPL-3.0 license
├── README.md                         # Chinese documentation
├── README_en.md                      # English documentation
└── .gitignore                       # Git ignore rules
```

## 📋 Core Module Description

### 🎯 Command Line Tools
| File | Function Description |
|------|----------------------|
| **main.py** | Command-line interface main entry, handles parameter parsing, validation, and coordinates the entire conversion process |
| **helpers.py** | Shared utility functions, including logging setup, file operations, KiCad library management, etc. |

### 🌐 Web UI Interface
| File | Function Description |
|------|----------------------|
| **app.py** | Flask web application main program, provides REST API and static file services |
| **index.html** | Main page, modern user interface with drag-and-drop and real-time feedback |
| **css/styles.css** | Style files, frosted glass effects and responsive design |
| **js/script.js** | Frontend interaction scripts, handles form submission, progress display, and result presentation |

### 📚 Documentation Directory
| File | Function Description |
|------|----------------------|
| **README.md** | Documentation index, provides links and brief descriptions for all documents |
| **project_structure.md** | Detailed project structure and module descriptions |
| **development_guide.md** | Development environment setup and workflow guide |
| **contributing.md** | Project contribution process and guidelines |
| **performance.md** | Multi-threading parallel processing and performance optimization |
| **system_requirements.md** | System requirements and supported component types |

### 🔧 Core Engine
| Module | Function Description |
|--------|----------------------|
| **easyeda/** | EasyEDA API client and data processing modules |
| **kicad/** | KiCad format export engines, supports symbols, footprints, and 3D models |

### 📦 Data Processing Flow
1. **API Retrieval**: Get component data from EasyEDA/LCSC
2. **Data Parsing**: Parse symbol, footprint, and 3D model information
3. **Format Conversion**: Convert to KiCad compatible format
4. **File Generation**: Output .kicad_sym, .kicad_mod and other files
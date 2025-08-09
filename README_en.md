# EasyKiConverter 🔄

**[English](README_en.md)** | [中文](README.md)

A powerful Python tool for converting LCSC and EasyEDA components to KiCad format, supporting complete conversion of symbols, footprints, and 3D models. Provides both command-line tools and modern Web UI interface.

## ✨ Features

### 🎯 Core Functions
- **Symbol Conversion**: Convert EasyEDA symbols to KiCad symbol libraries (.kicad_sym)
- **Footprint Generation**: Create KiCad footprints from EasyEDA packages (.kicad_mod)
- **3D Model Support**: Automatically download and convert 3D models (multiple formats supported)
- **Batch Processing**: Support simultaneous conversion of multiple components
- **Version Compatibility**: Support KiCad 5.x and 6.x+ versions

### 🌐 Web UI Interface
- **Modern Interface**: Beautiful frosted glass effect design
- **Real-time Progress**: Visual progress bar for conversion process
- **Flexible Input**: Support LCSC part numbers or LCSC links
- **Selective Export**: Choose to export symbols, footprints, or 3D models
- **Instant Preview**: Real-time display of conversion results

### 🛠️ Command Line Tools
- **Script Automation**: Suitable for batch processing and CI/CD integration
- **Rich Parameters**: Complete command-line parameter support
- **Detailed Logging**: Detailed conversion process logs

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/your-username/EasyKiConverter.git
cd EasyKiConverter

# Install dependencies (choose based on usage)
# Command-line tools only
pip install -r EasyKiConverter/requirements.txt

# Web UI (Recommended)
pip install -r EasyKiConverter/Web_Ui/requirements.txt
```

### 🌐 Web UI Usage (Recommended)

```bash
# Method 1: Use startup script (Windows)
start_webui.bat

# Method 2: Manual startup
cd EasyKiConverter/Web_Ui
python app.py

# Then visit in browser: http://localhost:8000
```

**Web UI Usage Steps:**
1. Enter LCSC part number (e.g., C13377) or LCSC link in the input box
2. Select export content: symbols, footprints, 3D models
3. Set output directory and library name
4. Click "Start Export" button
5. View real-time progress and conversion results

### 🛠️ Command Line Usage

```bash
cd EasyKiConverter

# Convert single component (export all content)
python main.py --lcsc_id C13377 --symbol --footprint --model3d

# Export symbols only
python main.py --lcsc_id C13377 --symbol

# Specify output directory and library name
python main.py --lcsc_id C13377 --symbol --footprint --output_dir ./my_libs --lib_name MyLibrary
```

## 📁 Project Structure

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

## 🔧 Command Line Options

```bash
python main.py [options]

Required parameters:
  --lcsc_id TEXT         LCSC part number to convert (e.g., C13377)

Export options (at least one required):
  --symbol               Export symbols (.kicad_sym)
  --footprint            Export footprints (.kicad_mod)
  --model3d              Export 3D models

Optional parameters:
  --output_dir PATH      Output directory path [default: ./output]
  --lib_name TEXT        Library file name [default: EasyKiConverter]
  --kicad_version INT    KiCad version (5 or 6) [default: 6]
  --overwrite            Overwrite existing files
  --debug                Enable detailed logging
  --help                 Show help information
```

### 📝 Usage Examples

```bash
# Export all content to default directory
python main.py --lcsc_id C13377 --symbol --footprint --model3d

# Export symbols only to specified directory
python main.py --lcsc_id C13377 --symbol --output_dir ./my_symbols

# Export to custom library name
python main.py --lcsc_id C13377 --symbol --footprint --lib_name MyComponents

# Enable debug mode
python main.py --lcsc_id C13377 --symbol --debug
```

## 🛠️ Development Guide

### Setting up Development Environment

```bash
# Clone project
git clone https://github.com/your-username/EasyKiConverter.git
cd EasyKiConverter

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r EasyKiConverter/Web_Ui/requirements.txt
```

### 🌐 Web UI Development

```bash
# Start development server
cd EasyKiConverter/Web_Ui
python app.py

# Access development interface
# http://localhost:8000
```

**Frontend Development:**
- Modify `index.html` - Page structure
- Modify `css/styles.css` - Styles and animations
- Modify `js/script.js` - Interaction logic

**Backend Development:**
- Modify `app.py` - API interfaces and routing
- Core conversion logic in `../` directory

### 🛠️ Command Line Development

```bash
# Run basic conversion test
cd EasyKiConverter
python main.py --lcsc_id C13377 --symbol --debug

# Test different component types
python main.py --lcsc_id C25804 --footprint --debug  # Test footprints
python main.py --lcsc_id C13377 --model3d --debug    # Test 3D models
```

### 🔧 Code Structure

- **easyeda/** - EasyEDA API and data processing
- **kicad/** - KiCad format export engines
- **Web_Ui/** - Flask web application
- **main.py** - Command-line entry point
- **helpers.py** - Shared utility functions

## 📝 System Requirements

### Basic Requirements
- **Python 3.7+** (Recommended 3.8+)
- **Internet Connection** (Access EasyEDA/LCSC API)
- **KiCad 5.x or 6.x+** (Use generated library files)

### Python Dependencies
- **Flask 2.0+** (Web UI)
- **Flask-CORS** (Cross-origin support)
- **requests** (HTTP requests)
- **Other dependencies** see requirements.txt

### Supported Operating Systems
- ✅ Windows 10/11
- ✅ macOS 10.14+
- ✅ Linux (Ubuntu 18.04+)

## 🎯 Supported Component Types

- 🔌 **Connectors** - Various plugs and terminals
- 🔧 **Discrete Components** - Resistors, capacitors, inductors, diodes, etc.
- 💾 **Integrated Circuits** - MCUs, memory, op-amps, etc.
- ⚡ **Power Management** - Regulators, switching power supply chips, etc.
- 📡 **RF Components** - Antennas, filters, etc.
- 🔍 **Sensors** - Temperature, pressure, optical sensors, etc.

## 🤝 Contributing Guide

We welcome all forms of contributions!

### 🐛 Report Issues
- Use [GitHub Issues](https://github.com/your-username/EasyKiConverter/issues)
- Provide detailed error information and reproduction steps
- Include LCSC part numbers and system information

### 💡 Feature Suggestions
- Describe new feature requirements in Issues
- Explain use cases and expected effects

### 🔧 Code Contributions
1. Fork the project
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Create Pull Request

## 📄 License

This project is licensed under **GNU General Public License v3.0 (GPL-3.0)**.

- ✅ Commercial use
- ✅ Modification
- ✅ Distribution
- ✅ Patent use
- ❌ Liability
- ❌ Warranty

See [LICENSE](LICENSE) file for complete license terms.

---

## 🙏 Acknowledgments

### 🌟 Special Thanks

This project is derived from **[uPesy/easyeda2kicad.py](https://github.com/uPesy/easyeda2kicad.py)**. We thank the original author for providing an excellent foundation framework and core conversion algorithms, which laid a solid foundation for the development of this project.

### 🤝 Other Acknowledgments

Thanks to [GitHub](https://github.com/) platform and all contributors who have contributed to this project.

We would like to express our sincere gratitude to all the contributors.

<a href="https://github.com/your-username/EasyKiConverter/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=your-username/EasyKiConverter" />
</a>

Thanks to [EasyEDA](https://easyeda.com/) and [LCSC](https://www.szlcsc.com/) for providing open APIs.

Thanks to [KiCad](https://www.kicad.org/) open source circuit design software.

---

**⭐ If this project helps you, please give us a Star!**
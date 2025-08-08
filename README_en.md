# EasyKiConverter 🔄

**English** | [中文](README_zh.md)

A powerful Python tool for converting EasyEDA components to KiCad format with support for symbols, footprints, and 3D models.

## ✨ Features

- **Symbol Conversion**: Convert EasyEDA symbols to KiCad symbol libraries
- **Footprint Generation**: Create KiCad footprints from EasyEDA packages
- **3D Model Support**: Download and convert 3D models (OBJ and STEP formats)
- **Batch Processing**: Process multiple components in a single run
- **Flexible Output**: Support for different KiCad versions and output formats
- **API Integration**: Direct access to EasyEDA's component database

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/your-username/EasyKiConverter.git
cd EasyKiConverter

# Install dependencies
pip install -r requirements.txt
```

### Basic Usage

```bash
# Convert a single component
python main.py -i LCSC_PART_NUMBER -v 6

# Convert multiple components
python main.py -i LCSC_PART_NUMBER1 LCSC_PART_NUMBER2 -v 6

# Specify output directory
python main.py -i LCSC_PART_NUMBER -v 6 -o ./output
```

## 📁 Project Structure

```
EasyKiConverter/
├── main.py                 # Main entry point and CLI interface
├── easyeda_api.py          # EasyEDA API client for component data
├── export_kicad_symbol.py  # KiCad symbol generation engine
├── export_kicad_footprint.py  # KiCad footprint generation engine
├── helpers.py              # Utility functions and helpers
├── requirements.txt        # Python dependencies
├── README.md              # This file (English)
├── README_zh.md           # Chinese documentation
└── .gitignore            # Git ignore rules
```

## 📋 File Descriptions

| File | Description |
|------|-------------|
| **main.py** | Command-line interface that orchestrates the entire conversion process. Handles argument parsing, validation, and coordinates between API calls and export engines. |
| **easyeda_api.py** | REST API client for EasyEDA's component database. Retrieves symbol data, footprint information, and 3D model URLs. |
| **export_kicad_symbol.py** | Core engine for converting EasyEDA symbols to KiCad format. Handles pin mapping, graphical elements, and symbol properties. |
| **export_kicad_footprint.py** | Engine for generating KiCad footprints from EasyEDA packages. Creates pads, silkscreen, and mechanical layers. |
| **helpers.py** | Shared utilities including logging setup, file operations, coordinate transformations, and KiCad library management. |
| **requirements.txt** | Lists all Python package dependencies needed to run the project. |

## 🔧 Command Line Options

```bash
python main.py [OPTIONS]

Options:
  -i, --id TEXT          LCSC part number(s) to convert  [required]
  -v, --kicad_version    KiCad version (5 or 6)  [default: 6]
  -o, --output_dir       Output directory path  [default: ./output]
  --overwrite            Overwrite existing files
  --debug                Enable debug logging
  --help                 Show help message
```

## 🛠️ Development

### Setting up Development Environment

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -r requirements.txt
```

### Running Tests

```bash
# Run basic conversion test
python main.py -i C13377 -v 6 --debug
```

## 📝 Requirements

- Python 3.7+
- Internet connection (for EasyEDA API access)
- KiCad (for using generated libraries)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the GNU General Public License v3.0 (GPL-3.0) - see the [LICENSE](../LICENSE) file in the project root directory for details.
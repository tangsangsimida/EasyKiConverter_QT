# 📝 System Requirements

## Basic Requirements
- **Python 3.7+** (Recommended 3.8+)
- **Internet Connection** (Access EasyEDA/LCSC API)
- **KiCad 5.x or 6.x+** (Use generated library files)

## Python Dependencies

### Core Dependencies (core.txt)
- **requests** >= 2.25.0 (HTTP requests)
- **pydantic** >= 1.8.0 (Data validation)

### Web UI Dependencies (Web_Ui/requirements.txt)
- **Flask** 2.0+ (Web UI)
- **Flask-CORS** (Cross-origin support)
- **requests** (HTTP requests)

### PyQt6 UI Dependencies (requirements/pyqt6.txt)
- **PyQt6** >= 6.4.0 (Desktop UI framework)
- **PyQt6-Qt6** >= 6.4.0 (Qt6 library)
- **pandas** >= 1.3.0 (Data processing)
- **openpyxl** >= 3.0.0 (Excel file processing)

### Development Dependencies (requirements/dev.txt)
- **pytest** >= 6.0.0 (Testing framework)
- **pytest-cov** >= 2.10.0 (Test coverage)
- **black** >= 21.0.0 (Code formatting)
- **flake8** >= 3.8.0 (Code checking)
- **mypy** >= 0.812 (Type checking)

## Supported Operating Systems
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
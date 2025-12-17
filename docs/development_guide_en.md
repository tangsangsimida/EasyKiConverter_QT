# 🛠️ Development Guide

## Setting up Development Environment

```bash
# Clone project
git clone https://github.com/tangsangsimida/EasyKiConverter.git
cd EasyKiConverter

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Install application dependencies (based on build_conf/requirements_app.txt)
pip install -r build_conf/requirements_app.txt
```

## 🖥️ PyQt6 UI Development

```bash
# Start PyQt6 UI
cd src/ui/pyqt6
python app_main.py
```

**UI Development:**
- Modify `app_main.py` - Main program entry and business logic
- Modify `base_main_window.py` - Base window interface
- Modify various UI components in the `widgets/` directory
- Modify utility classes and style management in the `utils/` directory

**Core Conversion Logic:**
- Core conversion logic in the `src/core/` directory
- EasyEDA data processing in the `src/core/easyeda/` directory
- KiCad export engines in the `src/core/kicad/` directory

## 🛠️ Command Line Development

```bash
# Run basic conversion test
cd src
python app_main.py --lcsc_id C13377 --symbol --debug

# Test different component types
python app_main.py --lcsc_id C25804 --footprint --debug  # Test footprints
python app_main.py --lcsc_id C13377 --model3d --debug    # Test 3D models
```

## 🔧 Code Structure

- **src/core/** - Core conversion engine
  - **easyeda/** - EasyEDA API and data processing
  - **kicad/** - KiCad format export engines
  - **utils/** - Shared utility functions
- **src/ui/** - User interfaces
  - **pyqt6/** - PyQt6 desktop application

## 🔧 Command Line Options

```bash
python app_main.py [options]

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
python app_main.py --lcsc_id C13377 --symbol --footprint --model3d

# Export symbols only to specified directory
python app_main.py --lcsc_id C13377 --symbol --output_dir ./my_symbols

# Export to custom library name
python app_main.py --lcsc_id C13377 --symbol --footprint --lib_name MyComponents

# Enable debug mode
python app_main.py --lcsc_id C13377 --symbol --debug
```
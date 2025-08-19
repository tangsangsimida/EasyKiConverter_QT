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

# Install dependencies
pip install -r EasyKiConverter/Web_Ui/requirements.txt
```

## 🌐 Web UI Development

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

## 🛠️ Command Line Development

```bash
# Run basic conversion test
cd EasyKiConverter
python main.py --lcsc_id C13377 --symbol --debug

# Test different component types
python main.py --lcsc_id C25804 --footprint --debug  # Test footprints
python main.py --lcsc_id C13377 --model3d --debug    # Test 3D models
```

## 🔧 Code Structure

- **easyeda/** - EasyEDA API and data processing
- **kicad/** - KiCad format export engines
- **Web_Ui/** - Flask web application
- **main.py** - Command-line entry point
- **helpers.py** - Shared utility functions

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
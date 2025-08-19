# EasyKiConverter 🔄

**[English](README_en.md)** | [中文](README.md)

A powerful Python tool for converting LCSC and EasyEDA components to KiCad format, supporting complete conversion of symbols, footprints, and 3D models. Features a modern Web UI interface that makes component conversion simple and efficient.

## ✨ Features

### 🎯 Core Functions
- **Symbol Conversion**: Convert EasyEDA symbols to KiCad symbol libraries (.kicad_sym)
- **Footprint Generation**: Create KiCad footprints from EasyEDA packages (.kicad_mod)
- **3D Model Support**: Automatically download and convert 3D models (multiple formats supported)
- **Batch Processing**: Support simultaneous conversion of multiple components
- **Multi-threading Optimization**: Parallel processing of multiple components for significantly improved efficiency
- **Version Compatibility**: Support KiCad 5.x and 6.x+ versions

### 🌐 Web UI Interface
- **Modern Interface**: Beautiful frosted glass effect design
- **Real-time Progress**: Visual progress bar for conversion process with parallel processing status
- **Flexible Input**: Support LCSC part numbers or LCSC links
- **Selective Export**: Choose to export symbols, footprints, or 3D models
- **Instant Preview**: Real-time display of conversion results with processing time and file statistics
- **Smart Configuration**: Auto-save export settings with clipboard quick input support

### 🛠️ User-Friendly Design
- **One-Click Launch**: Start Web UI with a simple double-click
- **Zero Configuration**: Ready to use out of the box
- **Cross-Platform**: Supports Windows, macOS, and Linux systems

## 🚀 Quick Start

### 💻 Installation & Setup

```bash
# Clone the repository
git clone https://github.com/tangsangsimida/EasyKiConverter.git
cd EasyKiConverter
```

> 💡 **Tip**: The startup script will automatically check and install required dependencies

### 🚀 Launch Web UI

```bash
# Use startup script (Recommended)
# Windows users
start_webui.bat

# Linux/macOS users
./start_webui.sh
```

After startup, visit in browser: **http://localhost:8000**

### 🎯 Web UI User Guide

**Complete component conversion in four simple steps:**

1. **📝 Input Component Information**
   - Enter LCSC part number (e.g., C13377) in the input box
   - Or paste LCSC product link directly
   - Support batch input of multiple part numbers

2. **⚙️ Select Export Options**
   - ✅ Symbol library (.kicad_sym)
   - ✅ Footprint library (.kicad_mod)
   - ✅ 3D models (.step/.wrl)

3. **📁 Configure Output Path**
   - Choose output directory
   - Set library file name prefix
   - Settings auto-save for convenience

4. **🚀 Start Conversion**
   - Click "Start Export" button
   - View real-time conversion progress
   - Multi-component parallel processing for higher efficiency

## 📚 Detailed Documentation

For more detailed information, please refer to the documentation in the `docs` directory:

- [Project Structure](docs/project_structure.md) - Detailed project structure and module descriptions
- [Development Guide](docs/development_guide.md) - Development environment setup and workflow
- [Contributing Guide](docs/contributing.md) - How to contribute to the project
- [Performance Optimization](docs/performance.md) - Multi-threading parallel processing and performance improvements
- [System Requirements](docs/system_requirements.md) - System requirements and supported component types

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

<a href="https://github.com/tangsangsimida/EasyKiConverter/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=tangsangsimida/EasyKiConverter" />
</a>

Thanks to [EasyEDA](https://easyeda.com/) and [LCSC](https://www.szlcsc.com/) for providing open APIs.

Thanks to [KiCad](https://www.kicad.org/) open source circuit design software.

---

**⭐ If this project helps you, please give us a Star!**
# 📝 系统要求

## 基本要求
- **Python 3.7+** （推荐 3.8+）
- **网络连接** （访问 EasyEDA/LCSC API）
- **KiCad  6.x+** （使用生成的库文件）

## Python 依赖

### 核心依赖 (core.txt)
- **requests** >= 2.25.0 （HTTP 请求）
- **pydantic** >= 1.8.0 （数据验证）

### Web UI 依赖 (Web_Ui/requirements.txt)
- **Flask** 2.0+ （Web UI）
- **Flask-CORS** （跨域支持）
- **requests** （HTTP 请求）

### PyQt6 UI 依赖 (requirements/pyqt6.txt)
- **PyQt6** >= 6.4.0 （桌面UI框架）
- **PyQt6-Qt6** >= 6.4.0 （Qt6库）
- **pandas** >= 1.3.0 （数据处理）
- **openpyxl** >= 3.0.0 （Excel文件处理）

### 开发依赖 (requirements/dev.txt)
- **pytest** >= 6.0.0 （测试框架）
- **pytest-cov** >= 2.10.0 （测试覆盖率）
- **black** >= 21.0.0 （代码格式化）
- **flake8** >= 3.8.0 （代码检查）
- **mypy** >= 0.812 （类型检查）

## 支持的操作系统
- ✅ Windows 10/11
- ✅ macOS 10.14+
- ✅ Linux (Ubuntu 18.04+)

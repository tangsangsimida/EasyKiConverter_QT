# 🛠️ 开发指南

## 设置开发环境

```bash
# 克隆项目
git clone https://github.com/tangsangsimida/EasyKiConverter.git
cd EasyKiConverter

# 创建虚拟环境
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# 安装应用依赖（根据build_conf/requirements_app.txt文件）
pip install -r build_conf/requirements_app.txt

# Linux用户如需构建特定包格式，安装额外依赖
# DEB包构建依赖
# pip install stdeb

# RPM包构建依赖（通过系统包管理器安装）
# sudo apt-get install rpm
```

## 🖥️ PyQt6 UI 开发

```bash
# 启动PyQt6 UI
python -m src.ui.pyqt6.main
```

**UI开发：**
- 修改 `main.py` - 主程序入口和业务逻辑
- 修改 `modern_main_window.py` - 主窗口界面
- 修改 `widgets/` 目录下的各种UI组件
- 修改 `utils/` 目录下的工具类和样式管理

**核心转换逻辑：**

- 核心转换逻辑在 `src/core/` 目录中
- EasyEDA数据处理在 `src/core/easyeda/` 目录中
- KiCad导出引擎在 `src/core/kicad/` 目录中

## 📦 依赖版本说明

项目使用最新的依赖包版本以确保功能完整性和安全性：
- **pandas**: 2.3.2（最新稳定版本）
- **numpy**: 2.3.3（最新稳定版本）

所有支持的平台（Windows x64、Linux、macOS）均使用相同的依赖版本。

## 📦 多平台构建

### 支持的平台和架构
- **Windows**: x86和x64架构
- **Linux**: x64架构，支持二进制文件和DEB包格式
- **macOS**: Intel和Apple Silicon架构

### 构建所有平台版本
```bash
# 使用GitHub Actions自动构建所有平台版本
# 推送带有[release]标记的提交触发构建流程

# 或者手动构建特定平台
# Windows (x64)
pyinstaller build_conf/build.spec --noconfirm

# Linux (创建DEB包)
# 需要先安装dpkg-deb工具
sudo apt-get install dpkg-dev
# 然后按照build.yml中的步骤创建DEB包
```

### 包格式说明
- **EXE文件**: Windows平台可执行文件
- **二进制文件**: Linux和macOS平台可执行文件
- **DEB包**: Debian/Ubuntu等基于Debian的Linux发行版的软件包格式
- **RPM包**: Fedora/RHEL等基于RPM的Linux发行版的软件包格式
- **Tarball包**: Arch Linux等发行版的软件包格式
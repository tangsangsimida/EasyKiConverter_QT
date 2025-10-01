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
```

## 🖥️ PyQt6 UI 开发

```bash
# 启动PyQt6 UI
cd src/ui/pyqt6
python main.py
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

## 🛠️ 命令行开发

```bash
# 运行基本转换测试
cd src
python main.py --lcsc_id C13377 --symbol --debug

# 测试不同组件类型
python main.py --lcsc_id C25804 --footprint --debug  # 测试封装
python main.py --lcsc_id C13377 --model3d --debug    # 测试3D模型
```

## 🔧 代码结构

- **src/core/** - 核心转换引擎
  - **easyeda/** - EasyEDA API 和数据处理
  - **kicad/** - KiCad 格式导出引擎
  - **utils/** - 共享工具函数
- **src/ui/** - 用户界面
  - **pyqt6/** - PyQt6 桌面应用

## 🔧 命令行选项

```bash
python main.py [options]

必需参数:
  --lcsc_id TEXT         要转换的LCSC元件编号 (例如: C2040)

导出选项 (至少需要一个):
  --symbol               导出符号库 (.kicad_sym)
  --footprint            导出封装库 (.kicad_mod)
  --model3d              导出3D模型

可选参数:
  --output_dir PATH      输出目录路径 [默认: ./output]
  --lib_name TEXT        库文件名称 [默认: EasyKiConverter]
  --kicad_version INT    KiCad版本 (5 或 6) [默认: 6]
  --overwrite            覆盖现有文件
  --debug                启用详细日志
  --help                 显示帮助信息
```

### 📝 使用示例

```bash
# 导出所有内容到默认目录
python main.py --lcsc_id C13377 --symbol --footprint --model3d

# 仅导出符号到指定目录
python main.py --lcsc_id C13377 --symbol --output_dir ./my_symbols

# 导出到自定义库名称
python main.py --lcsc_id C13377 --symbol --footprint --lib_name MyComponents

# 启用调试模式
python main.py --lcsc_id C13377 --symbol --debug
```

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
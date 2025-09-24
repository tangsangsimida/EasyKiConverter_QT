# EasyKiConverter PyQt6 UI 打包指南

## 环境要求

- Python 3.8+
- PyQt6 6.4.0+
- PyInstaller 5.0+

## 打包步骤

### 1. 安装依赖

```bash
# 激活虚拟环境（如果使用）
source venv/bin/activate  # Linux/macOS
# 或
venv\Scripts\activate  # Windows

# 安装PyQt6依赖
pip install PyQt6>=6.4.0 PyQt6-Qt6>=6.4.0

# 安装打包工具
pip install pyinstaller>=5.0

# 安装其他依赖
pip install requests>=2.25.0 pydantic>=1.8.0 pandas>=1.3.0 openpyxl>=3.0.0
```

### 2. 打包命令

#### Windows
```bash
cd PyQt6_UI
pyinstaller easykiconverter.spec --clean --noconfirm
```

#### Linux/macOS
```bash
cd PyQt6_UI
pyinstaller easykiconverter.spec --clean --noconfirm
```

#### 单文件打包（可选）
```bash
# 在spec文件中设置 console=False 和 onefile=True
pyinstaller easykiconverter.spec --onefile --clean --noconfirm
```

### 3. 打包输出

打包完成后，可执行文件将在以下目录中：

- **Windows**: `dist/EasyKiConverter.exe`
- **Linux**: `dist/EasyKiConverter`
- **macOS**: `dist/EasyKiConverter.app`

### 4. 打包选项说明

#### 基本选项
- `--onefile`: 打包成单个可执行文件
- `--windowed`: 不显示控制台窗口（GUI应用）
- `--icon=icon.ico`: 添加应用程序图标
- `--name=AppName`: 指定应用程序名称

#### 高级选项
- `--clean`: 清理之前的构建缓存
- `--noconfirm`: 覆盖输出目录而不确认
- `--debug`: 启用调试模式

### 5. 减小打包体积

#### 排除不需要的模块
在spec文件中添加：
```python
excludes=[
    "tkinter",
    "matplotlib", 
    "numpy",
    "scipy",
    "PIL",
    "PyQt5",
    "PySide2",
    "PySide6",
]
```

#### 使用UPX压缩
确保已安装UPX，PyInstaller会自动使用它进行压缩。

### 6. 平台特定说明

#### Windows
- 生成的exe文件可以直接运行
- 可以创建桌面快捷方式
- 建议添加代码签名证书

#### Linux
- 可能需要设置可执行权限：`chmod +x EasyKiConverter`
- 确保系统有必要的运行时库

#### macOS
- 生成的app包可以直接运行
- 可能需要处理代码签名和公证
- 注意Gatekeeper安全设置

### 7. 测试打包结果

打包完成后，建议进行以下测试：

1. **基本功能测试**
   - 启动应用程序
   - 添加元件编号
   - 执行转换操作
   - 检查输出文件

2. **边界情况测试**
   - 大量元件批量转换
   - 网络异常情况
   - 文件权限问题

3. **性能测试**
   - 内存使用情况
   - CPU占用率
   - 响应时间

### 8. 分发准备

#### 创建安装包（可选）

**Windows - NSIS**
```bash
# 安装NSIS后创建安装脚本
makensis installer.nsi
```

**macOS - DMG**
```bash
# 使用create-dmg工具
create-dmg EasyKiConverter.dmg dist/EasyKiConverter.app
```

**Linux - AppImage**
```bash
# 使用appimagetool
appimagetool dist/EasyKiConverter
```

#### 创建压缩包
```bash
# Windows
cd dist && zip -r EasyKiConverter-Windows.zip EasyKiConverter.exe

# Linux
cd dist && tar -czf EasyKiConverter-Linux.tar.gz EasyKiConverter

# macOS
cd dist && zip -r EasyKiConverter-macOS.zip EasyKiConverter.app
```

### 9. 常见问题

#### Q: 打包后程序无法启动？
A: 检查是否缺少依赖模块，查看控制台错误信息。

#### Q: 打包体积太大？
A: 使用`--exclude`排除不需要的模块，启用UPX压缩。

#### Q: 图标不显示？
A: 确保图标文件路径正确，格式支持（.ico/.icns）。

#### Q: 在某些系统上运行失败？
A: 检查系统兼容性，考虑静态链接运行时库。

### 10. 自动化打包

可以创建GitHub Actions工作流实现自动打包：

```yaml
name: Build Executables

on:
  push:
    tags:
      - 'v*'

jobs:
  build:
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
    
    runs-on: ${{ matrix.os }}
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r PyQt6_UI/requirements.txt
        pip install pyinstaller
    
    - name: Build with PyInstaller
      run: |
        cd PyQt6_UI
        pyinstaller easykiconverter.spec --clean --noconfirm
    
    - name: Upload artifacts
      uses: actions/upload-artifact@v3
      with:
        name: EasyKiConverter-${{ matrix.os }}
        path: PyQt6_UI/dist/
```

## 注意事项

1. **版权问题**: 确保遵守所有依赖库的许可证要求
2. **代码签名**: 为正式发布的软件添加代码签名
3. **更新机制**: 考虑实现自动更新功能
4. **错误报告**: 提供用户友好的错误报告机制
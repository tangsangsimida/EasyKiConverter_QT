# EasyKiConverter PyQt6 UI

基于PyQt6的EasyKiConverter桌面应用程序，提供现代化的图形界面，用于将嘉立创EDA元器件转换为KiCad格式。

## ✨ 功能特性

### 🎯 核心功能
- **符号转换**: 将EasyEDA符号转换为KiCad符号库（.kicad_sym）
- **封装生成**: 从EasyEDA封装创建KiCad封装（.kicad_mod）
- **3D模型支持**: 自动下载并转换3D模型（支持多种格式）
- **批量处理**: 支持多个元件同时转换
- **多线程优化**: 并行处理多个元件，显著提升转换效率
- **版本兼容**: 支持KiCad 5.x和6.x+版本

### 🖥️ 桌面应用特性
- **现代化界面**: 美观的PyQt6界面设计，支持深色/浅色主题
- **实时进度**: 转换过程可视化进度条，支持并行处理状态显示
- **灵活输入**: 支持LCSC编号或嘉立创链接
- **选择性导出**: 可选择导出符号、封装或3D模型
- **即时预览**: 转换结果实时显示，包含处理时间和文件统计
- **智能配置**: 自动保存导出配置，支持剪贴板快速输入
- **BOM导入**: 支持Excel/CSV格式的BOM文件批量导入
- **文件管理**: 集成文件浏览器，方便选择输出目录

## 🚀 快速开始

### 环境要求

- Python 3.8+
- PyQt6 6.4.0+
- 其他依赖见 `requirements.txt`

### 安装依赖

```bash
# 激活虚拟环境（如果使用）
source venv/bin/activate  # Linux/macOS
# 或
venv\Scripts\activate  # Windows

# 安装依赖
pip install -r PyQt6_UI/requirements.txt
```

### 运行应用

```bash
# 方法1: 使用启动脚本
chmod +x PyQt6_UI/start_pyqt6_ui.sh
./PyQt6_UI/start_pyqt6_ui.sh

# 方法2: 直接运行
python PyQt6_UI/main.py
```

## 📦 打包发布

### 安装打包工具

```bash
pip install pyinstaller>=5.0
```

### 创建打包配置

```bash
cd EasyKiConverter/EasyKiConverter
python PyQt6_UI/create_pyinstaller_config.py
```

### 执行打包

```bash
# 使用完整打包脚本
python build_pyqt6_ui.py

# 或使用快速打包
python quick_build.py
```

打包完成后，可执行文件将在 `dist/` 目录中：
- **Windows**: `EasyKiConverter-PyQt6.exe`
- **Linux/macOS**: `EasyKiConverter-PyQt6`

详细打包指南请参考 [PACKAGING_GUIDE.md](PACKAGING_GUIDE.md)

## 🏗️ 项目结构

```
PyQt6_UI/
├── main.py                    # 主程序入口
├── main_window.py            # 主窗口类
├── requirements.txt          # 依赖列表
├── start_pyqt6_ui.sh         # 启动脚本（Linux/macOS）
├── create_pyinstaller_config.py  # 打包配置生成器
├── easykiconverter.spec      # PyInstaller spec文件
├── PACKAGING_GUIDE.md        # 打包指南
├── widgets/                  # UI组件
│   ├── __init__.py
│   ├── component_input_widget.py    # 元件输入组件
│   ├── progress_widget.py           # 进度显示组件
│   ├── results_widget.py            # 结果显示组件
│   └── navigation_widget.py         # 导航组件
├── workers/                  # 后台工作线程
│   ├── __init__.py
│   └── export_worker.py      # 导出工作线程
└── utils/                    # 工具类
    ├── __init__.py
    ├── config_manager.py     # 配置管理器
    ├── style_manager.py      # 样式管理器
    ├── bom_parser.py         # BOM文件解析器
    └── component_validator.py # 元件编号验证器
```

## 🎨 界面预览

### 主界面
- 左侧导航栏：快速切换功能模块
- 中央工作区：元件输入、进度显示、结果展示
- 底部状态栏：实时状态信息和主题切换

### 功能特点
- **现代化设计**: 采用Material Design风格
- **响应式布局**: 自适应不同屏幕尺寸
- **主题切换**: 支持深色/浅色主题
- **动画效果**: 平滑的过渡和交互动画

## ⚙️ 配置选项

### 导出设置
- **输出路径**: 自定义库文件保存位置
- **库名称**: 自定义生成的库文件名
- **导出选项**: 选择导出符号、封装、3D模型

### 界面设置
- **主题**: 深色/浅色主题切换
- **语言**: 支持中英文界面
- **窗口状态**: 自动保存和恢复窗口大小位置

### 高级设置
- **并行线程数**: 调整多线程处理并发数
- **调试模式**: 启用详细日志输出
- **自动更新**: 检查软件更新

## 🔧 开发指南

### 添加新功能

1. **创建新的Widget组件** 在 `widgets/` 目录下
2. **创建对应的工作线程** 在 `workers/` 目录下
3. **在主窗口中集成** 修改 `main_window.py`
4. **更新配置管理** 修改 `utils/config_manager.py`

### 自定义主题

编辑 `utils/style_manager.py` 中的主题样式：

```python
def apply_light_theme(self, widget):
    """应用浅色主题"""
    style_sheet = """
        /* 自定义样式 */
        QPushButton {
            background-color: #3498db;
            color: white;
            border-radius: 6px;
        }
    """
    widget.setStyleSheet(style_sheet)
```

### 扩展导出功能

修改 `workers/export_worker.py` 中的导出逻辑：

```python
def export_component_real(self, lcsc_id: str, export_path: str, 
                         export_options: Dict[str, bool], file_prefix: str = None) -> Dict[str, Any]:
    """自定义导出逻辑"""
    # 添加新的导出功能
    pass
```

## 🐛 常见问题

### Q: 应用程序无法启动？
**A**: 检查Python环境和依赖是否正确安装，确保激活了正确的虚拟环境。

### Q: 转换过程中出现错误？
**A**: 检查网络连接，确保能够访问嘉立创API。查看详细日志了解具体错误。

### Q: 打包后的程序运行缓慢？
**A**: 考虑使用UPX压缩，排除不必要的依赖模块，优化代码逻辑。

### Q: 界面显示异常？
**A**: 检查系统DPI设置，尝试切换主题或调整窗口大小。

## 🤝 贡献指南

欢迎提交Issue和Pull Request来改进这个项目！

### 提交Issue
- 描述清楚遇到的问题
- 提供复现步骤
- 附上相关日志和截图

### 提交代码
1. Fork本项目
2. 创建特性分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add some amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建Pull Request

## 📄 许可证

本项目采用GNU General Public License v3.0 (GPL-3.0)许可证。

## 🙏 致谢

- 基于[uPesy/easyeda2kicad.py](https://github.com/uPesy/easyeda2kicad.py)项目
- 感谢PyQt6框架提供的优秀GUI支持
- 感谢所有贡献者的支持和帮助

## 📞 联系方式

- **项目地址**: https://github.com/tangsangsimida/EasyKiConverter
- **Issue反馈**: https://github.com/tangsangsimida/EasyKiConverter/issues

---

**⭐ 如果这个项目对您有帮助，请给我们一个Star！**
# 📁 项目结构

```
EasyKiConverter/
├── .github/                           # GitHub相关配置
│   └── workflows/                    # GitHub Actions工作流
├── build_conf/                        # 构建配置目录
│   ├── build.spec                    # PyInstaller构建配置
│   └── requirements_app.txt          # 应用依赖
├── docs/                              # 详细文档目录
│   ├── README.md                     # 文档索引
│   ├── project_structure.md          # 项目结构详细说明
│   ├── development_guide.md          # 开发指南
│   ├── contributing.md               # 贡献指南
│   ├── performance.md                # 性能优化说明
│   ├── system_requirements.md        # 系统要求
│   ├── project_structure_en.md       # 项目结构（英文版）
│   ├── development_guide_en.md       # 开发指南（英文版）
│   ├── contributing_en.md            # 贡献指南（英文版）
│   ├── performance_en.md             # 性能优化说明（英文版）
│   └── system_requirements_en.md     # 系统要求（英文版）
├── src/                               # 源代码目录
│   ├── __init__.py                   # Python包初始化文件
│   ├── core/                         # 核心转换引擎
│   │   ├── __init__.py              # Python包初始化文件
│   │   ├── easyeda/                 # EasyEDA API 和数据处理
│   │   │   ├── __init__.py         # Python包初始化文件
│   │   │   ├── easyeda_api.py      # EasyEDA API 客户端
│   │   │   ├── easyeda_importer.py # 数据导入器
│   │   │   └── parameters_easyeda.py # EasyEDA 参数定义
│   │   ├── kicad/                   # KiCad 导出引擎
│   │   │   ├── __init__.py         # Python包初始化文件
│   │   │   ├── export_kicad_symbol.py # 符号导出器
│   │   │   ├── export_kicad_footprint.py # 封装导出器
│   │   │   ├── export_kicad_3d_model.py # 3D模型导出器
│   │   │   ├── parameters_kicad_footprint.py # KiCad 封装参数定义
│   │   │   └── parameters_kicad_symbol.py # KiCad 符号参数定义
│   │   └── utils/                   # 共享工具函数
│   │       ├── __init__.py         # Python包初始化文件
│   │       ├── geometry_utils.py   # 几何工具函数
│   │       └── symbol_lib_utils.py # 符号库工具函数
│   └── ui/                          # 用户界面
│       ├── __init__.py             # Python包初始化文件
│       └── pyqt6/                  # PyQt6 桌面应用
│           ├── __init__.py        # Python包初始化文件
│           ├── main.py            # PyQt6 UI主程序入口
│           ├── modern_main_window.py # 现代化主窗口
│           ├── user_config.json   # 用户配置文件
│           ├── utils/             # UI工具函数
│           │   ├── __init__.py    # Python包初始化文件
│           │   ├── bom_parser.py  # BOM文件解析器
│           │   ├── clipboard_processor.py # 剪贴板处理器
│           │   ├── component_validator.py # 元件验证器
│           │   ├── config_manager.py # 配置管理器
│           │   ├── modern_style.py # 现代化样式
│           │   ├── modern_ui_components.py # 现代化UI组件
│           │   ├── responsive_layout.py # 响应式布局
│           │   ├── style_manager.py # 样式管理器
│           │   └── ui_effects.py  # UI特效
│           ├── widgets/           # UI组件
│           │   ├── __init__.py    # Python包初始化文件
│           │   ├── component_input_widget.py # 元件输入组件
│           │   ├── conversion_results_widget.py # 转换结果组件
│           │   ├── modern_component_input_widget.py # 现代化元件输入组件
│           │   ├── navigation_widget.py # 导航组件
│           │   ├── optimized_component_input_widget.py # 优化的元件输入组件
│           │   ├── progress_widget.py # 进度组件
│           │   └── results_widget.py # 结果显示组件
│           └── workers/           # 工作线程
│               ├── __init__.py    # Python包初始化文件
│               └── export_worker.py # 导出工作线程
├── tests/                             # 测试目录
├── venv/                              # 虚拟环境目录
├── IFLOW.md                          # 项目概述文档
├── LICENSE                           # GPL-3.0 许可证
├── README.md                         # 中文文档
├── README_en.md                      # 英文文档
└── .gitignore                       # Git 忽略规则
```

## 📋 核心模块说明

### 🖥️ PyQt6 UI 界面
| 文件 | 功能描述 |
|------|----------|
| **src/ui/pyqt6/main.py** | PyQt6 UI主程序入口，包含主要业务逻辑 |
| **src/ui/pyqt6/modern_main_window.py** | 现代化主窗口界面 |
| **src/ui/pyqt6/widgets/** | 各种UI组件 |
| **src/ui/pyqt6/utils/** | UI工具函数和样式管理 |

### 🔧 核心引擎
| 模块 | 功能描述 |
|------|----------|
| **src/core/easyeda/** | EasyEDA API客户端和数据处理模块 |
| **src/core/kicad/** | KiCad格式导出引擎，支持符号、封装和3D模型 |
| **src/core/utils/** | 共享工具函数模块 |

### 📦 数据处理流程
1. **API获取**：从EasyEDA/LCSC获取元件数据
2. **数据解析**：解析符号、封装和3D模型信息
3. **格式转换**：转换为KiCad兼容格式
4. **文件生成**：输出.kicad_sym、.kicad_mod等文件
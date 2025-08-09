# EasyKiConverter 🔄

**[English](README_en.md)** | [中文](README.md)

一个强大的 Python 工具，用于将嘉立创（LCSC）和 EasyEDA 元件转换为 KiCad 格式，支持符号、封装和 3D 模型的完整转换。提供现代化的 Web UI 界面，让元件转换变得简单高效。

## ✨ 功能特性

### 🎯 核心功能
- **符号转换**：将 EasyEDA 符号转换为 KiCad 符号库（.kicad_sym）
- **封装生成**：从 EasyEDA 封装创建 KiCad 封装（.kicad_mod）
- **3D模型支持**：自动下载并转换 3D 模型（支持多种格式）
- **批量处理**：支持多个元件同时转换
- **多线程优化**：并行处理多个元件，显著提升转换效率
- **版本兼容**：支持 KiCad 5.x 和 6.x+ 版本

### 🌐 Web UI 界面
- **现代化界面**：美观的毛玻璃效果设计
- **实时进度**：转换过程可视化进度条，支持并行处理状态显示
- **灵活输入**：支持 LCSC 编号或嘉立创链接
- **选择性导出**：可选择导出符号、封装或 3D 模型
- **即时预览**：转换结果实时显示，包含处理时间和文件统计
- **智能配置**：自动保存导出配置，支持剪贴板快速输入

### 🛠️ 易用性设计
- **一键启动**：双击启动脚本即可运行 Web UI
- **无需配置**：开箱即用，无需复杂设置
- **跨平台支持**：支持 Windows、macOS 和 Linux 系统

## 🚀 快速开始

### 💻 安装与启动

```bash
# 克隆仓库
git clone https://github.com/tangsangsimida/EasyKiConverter.git
cd EasyKiConverter
```

> 💡 **提示**：启动脚本会自动检查并安装所需依赖，无需手动安装

### 🚀 启动 Web UI

```bash
# 使用启动脚本（推荐）
# Windows 用户
start_webui.bat

# Linux/macOS 用户
./start_webui.sh

```

启动后在浏览器中访问：**http://localhost:8000**

### 🎯 Web UI 使用指南

**简单四步完成元件转换：**

1. **📝 输入元件信息**
   - 在输入框中输入 LCSC 元件编号（如：C13377）
   - 或直接粘贴嘉立创商品链接
   - 支持批量输入多个元件编号

2. **⚙️ 选择导出选项**
   - ✅ 符号库（.kicad_sym）
   - ✅ 封装库（.kicad_mod）
   - ✅ 3D模型（.step/.wrl）

3. **📁 设置输出路径**
   - 选择输出目录
   - 设置库文件名称前缀
   - 配置会自动保存，下次使用更便捷

4. **🚀 开始转换**
   - 点击"开始导出"按钮
   - 实时查看转换进度
   - 多元件并行处理，效率更高

## 📁 项目结构

```
EasyKiConverter/
├── EasyKiConverter/                    # 核心转换引擎
│   ├── main.py                        # 命令行工具主入口
│   ├── helpers.py                     # 工具函数和辅助功能
│   ├── easyeda/                       # EasyEDA API 和数据处理
│   │   ├── easyeda_api.py            # EasyEDA API 客户端
│   │   ├── easyeda_importer.py       # 数据导入器
│   │   └── parameters_easyeda.py     # EasyEDA 参数定义
│   ├── kicad/                        # KiCad 导出引擎
│   │   ├── export_kicad_symbol.py    # 符号导出器
│   │   ├── export_kicad_footprint.py # 封装导出器
│   │   ├── export_kicad_3d_model.py  # 3D模型导出器
│   │   └── parameters_kicad_symbol.py # KiCad 参数定义
│   └── Web_Ui/                       # Web 用户界面
│       ├── app.py                    # Flask Web 应用
│       ├── index.html                # 主页面
│       ├── css/styles.css            # 样式文件
│       ├── js/script.js              # 前端脚本
│       ├── imgs/background.jpg       # 背景图片
│       └── requirements.txt          # Web UI 依赖
├── start_webui.bat                    # Windows 启动脚本
├── LICENSE                           # GPL-3.0 许可证
├── README.md                         # 中文文档
├── README_en.md                      # 英文文档
└── .gitignore                       # Git 忽略规则
```

## 📋 核心模块说明

### 🌐 Web UI 界面
| 文件 | 功能描述 |
|------|----------|
| **app.py** | Flask Web应用主程序，提供REST API和静态文件服务 |
| **index.html** | 主页面，现代化的用户界面，支持拖拽和实时反馈 |
| **css/styles.css** | 样式文件，毛玻璃效果和响应式设计 |
| **js/script.js** | 前端交互脚本，处理表单提交、进度显示和结果展示 |

### 🔧 核心引擎
| 模块 | 功能描述 |
|------|----------|
| **easyeda/** | EasyEDA API客户端和数据处理模块 |
| **kicad/** | KiCad格式导出引擎，支持符号、封装和3D模型 |

### 📦 数据处理流程
1. **API获取**：从EasyEDA/LCSC获取元件数据
2. **数据解析**：解析符号、封装和3D模型信息
3. **格式转换**：转换为KiCad兼容格式
4. **文件生成**：输出.kicad_sym、.kicad_mod等文件

## 🛠️ 开发指南

### 设置开发环境

```bash
# 克隆项目
git clone https://github.com/tangsangsimida/EasyKiConverter.git
cd EasyKiConverter

# 创建虚拟环境
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# 安装依赖
pip install -r EasyKiConverter/Web_Ui/requirements.txt
```

### 🌐 Web UI 开发

```bash
# 启动开发服务器
cd EasyKiConverter/Web_Ui
python app.py

# 访问开发界面
# http://localhost:8000
```

**前端开发：**
- 修改 `index.html` - 页面结构
- 修改 `css/styles.css` - 样式和动画
- 修改 `js/script.js` - 交互逻辑

**后端开发：**
- 修改 `app.py` - API 接口和路由
- 核心转换逻辑在 `../` 目录中

### 🔧 代码结构

- **easyeda/** - EasyEDA API 和数据处理
- **kicad/** - KiCad 格式导出引擎
- **Web_Ui/** - Flask Web 应用
- **main.py** - 命令行入口
- **helpers.py** - 共享工具函数

## 📝 系统要求

### 基本要求
- **Python 3.7+** （推荐 3.8+）
- **网络连接** （访问 EasyEDA/LCSC API）
- **KiCad 5.x 或 6.x+** （使用生成的库文件）

### Python 依赖
- **Flask 2.0+** （Web UI）
- **Flask-CORS** （跨域支持）
- **requests** （HTTP 请求）
- **其他依赖** 见 requirements.txt

### 支持的操作系统
- ✅ Windows 10/11
- ✅ macOS 10.14+
- ✅ Linux (Ubuntu 18.04+)

## ⚡ 性能优化

### 🚀 多线程并行处理
- **智能线程池**：根据 CPU 核心数自动调整并发线程数（最大8个）
- **并行转换**：多个元件同时处理，显著缩短批量转换时间
- **线程安全**：文件操作和符号库写入采用锁机制，确保数据完整性
- **资源优化**：单个元件直接处理，避免不必要的线程开销

### 🔧 技术特点
- **线程池管理**：使用 `concurrent.futures.ThreadPoolExecutor` 实现
- **锁机制**：为每个符号库文件分配独立锁，避免写入冲突
- **错误隔离**：单个元件处理失败不影响其他元件转换
- **内存优化**：合理控制并发数量，平衡性能与资源占用

## 🤝 贡献指南

我们欢迎所有形式的贡献！请遵循以下标准的 GitHub 协作流程：

### 🔄 开发流程

1. **Fork 项目**
   ```bash
   # Fork 主仓库到你的 GitHub 账户
   # 然后克隆你的 fork
   git clone https://github.com/your-username/EasyKiConverter.git
   cd EasyKiConverter
   ```

2. **切换到开发分支**
   ```bash
   # 切换到 dev 分支（开发分支）
   git checkout dev
   
   # 创建你的功能分支
   git checkout -b feature/your-feature-name
   ```

3. **进行开发**
   - 在 `feature/your-feature-name` 分支上进行开发
   - 遵循现有的代码风格和约定
   - 添加必要的测试和文档

4. **提交更改**
   ```bash
   git add .
   git commit -m "feat: 添加新功能描述"
   git push origin feature/your-feature-name
   ```

5. **创建 Pull Request**
   - 在 GitHub 上创建 PR
   - **目标分支**: `dev`（重要：所有 PR 都应该合并到 dev 分支）
   - 提供清晰的 PR 描述和变更说明

### 📋 贡献类型

- 🐛 **Bug 修复**: 修复现有功能的问题
- ✨ **新功能**: 添加新的功能特性
- 📚 **文档**: 改进文档和说明
- 🎨 **UI/UX**: 改进用户界面和体验
- ⚡ **性能**: 优化性能和效率
- 🧪 **测试**: 添加或改进测试

### 🔍 代码审查

- 所有 PR 都需要经过代码审查
- 维护者会审查你的代码并提供反馈
- 请及时响应审查意见并进行必要的修改
- 审查通过后，PR 将被合并到 `dev` 分支

### 🚀 发布流程

- `dev` 分支用于日常开发和功能集成
- 定期从 `dev` 分支创建发布版本到 `main` 分支
- 所有稳定功能都会在适当时候发布

### 💡 贡献建议

- 在开始大型功能开发前，建议先创建 Issue 讨论
- 保持 commit 信息清晰和有意义
- 遵循项目的编码规范
- 确保你的代码在提交前经过测试

### 🐛 报告问题
- 使用 [GitHub Issues](https://github.com/tangsangsimida/EasyKiConverter/issues)
- 提供详细的错误信息和复现步骤
- 包含 LCSC 元件编号和系统信息

### 💡 功能建议
- 在 Issues 中描述新功能需求
- 说明使用场景和预期效果
- 参与社区讨论和贡献

## 📄 许可证

本项目采用 **GNU General Public License v3.0 (GPL-3.0)** 许可证。

- ✅ 商业使用
- ✅ 修改
- ✅ 分发
- ✅ 专利使用
- ❌ 责任
- ❌ 保证

查看 [LICENSE](LICENSE) 文件了解完整许可证条款。

---

## 🙏 致谢

### 🌟 特别感谢

本项目基于 **[uPesy/easyeda2kicad.py](https://github.com/uPesy/easyeda2kicad.py)** 项目衍生而来。感谢原作者提供的优秀基础框架和核心转换算法，为本项目的开发奠定了坚实的基础。

### 🤝 其他致谢

感谢 [GitHub](https://github.com/) 平台以及所有为本项目提供贡献的贡献者。

我们要向所有贡献者表示诚挚的感谢。

<a href="https://github.com/tangsangsimida/EasyKiConverter/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=tangsangsimida/EasyKiConverter" />
</a>

感谢 [EasyEDA](https://easyeda.com/) 和 [嘉立创](https://www.szlcsc.com/) 提供的开放 API。

感谢 [KiCad](https://www.kicad.org/) 开源电路设计软件。

---

**⭐ 如果这个项目对您有帮助，请给我们一个 Star！**
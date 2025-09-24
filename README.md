# EasyKiConverter 🔄

**[English](README_en.md)** | [中文](README.md)

一个强大的 Python 工具，用于将嘉立创（LCSC）和 EasyEDA 元件转换为 KiCad 格式，支持符号、封装和 3D 模型的完整转换。提供现代化的 PyQt6 桌面界面，让元件转换变得简单高效。

## ✨ 功能特性

### 🎯 核心功能
- **符号转换**：将 EasyEDA 符号转换为 KiCad 符号库（.kicad_sym）
- **封装生成**：从 EasyEDA 封装创建 KiCad 封装（.kicad_mod）
- **3D模型支持**：自动下载并转换 3D 模型（支持多种格式）
- **批量处理**：支持多个元件同时转换
- **多线程优化**：并行处理多个元件，显著提升转换效率
- **版本兼容**：支持 KiCad 5.x 和 6.x+ 版本

### 🖥️ PyQt6 桌面界面
- **现代化界面**：美观的现代化设计，支持深色/浅色主题
- **实时进度**：转换过程可视化进度条，支持并行处理状态显示
- **灵活输入**：支持 LCSC 编号或嘉立创链接
- **选择性导出**：可选择导出符号、封装或 3D 模型
- **即时预览**：转换结果实时显示，包含处理时间和文件统计
- **智能配置**：自动保存导出配置，支持剪贴板快速输入
- **响应式布局**：适配不同屏幕尺寸，界面元素自动调整

### 🛠️ 易用性设计
- **一键启动**：双击启动脚本即可运行桌面应用
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

### 🚀 启动 PyQt6 桌面应用

```bash
# 使用启动脚本（推荐）
# Linux/macOS 用户
./scripts/start_pyqt6.sh

# 或者使用Python模块方式
python -m src.ui.pyqt6.main
```

启动应用后，将显示现代化的 PyQt6 桌面界面，支持直观的元件转换操作。



## 📚 详细文档

更多详细信息，请参阅 `docs` 目录下的文档：

- [项目结构](docs/project_structure.md) - 详细的项目结构和模块说明
- [开发指南](docs/development_guide.md) - 开发环境设置和开发流程
- [贡献指南](docs/contributing.md) - 如何参与项目贡献
- [性能优化](docs/performance.md) - 多线程并行处理和性能提升
- [系统要求](docs/system_requirements.md) - 系统要求和支持的元件类型

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

## 🔄 版本历史

### v2.0.0 (当前版本)
- 🎉 **重大更新**: 全面重构为 PyQt6 桌面应用
- 🎨 **界面升级**: 采用现代化设计，支持主题切换
- ⚡ **性能优化**: 改进的多线程处理机制
- 🔧 **架构重构**: 更清晰的项目结构和模块化设计
- 🗑️ **移除Web UI**: 专注于桌面应用体验
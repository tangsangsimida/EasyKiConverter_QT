# EasyKiConverter 🔄

**[English](README.md)** | 中文

一个强大的 Python 工具，用于将 EasyEDA 元件转换为 KiCad 格式，支持符号、封装和 3D 模型。

## ✨ 功能特性

- **符号转换**：将 EasyEDA 符号转换为 KiCad 符号库
- **封装生成**：从 EasyEDA 封装创建 KiCad 封装
- **3D模型支持**：下载并转换 3D 模型（OBJ 和 STEP 格式）
- **批量处理**：一次运行处理多个元件
- **灵活输出**：支持不同 KiCad 版本和输出格式
- **API集成**：直接访问 EasyEDA 元件数据库

## 🚀 快速开始

### 安装

```bash
# 克隆仓库
git clone https://github.com/your-username/EasyKiConverter.git
cd EasyKiConverter

# 安装依赖
pip install -r requirements.txt
```

### 基本用法

```bash
# 转换单个元件
python main.py -i LCSC元件编号 -v 6

# 转换多个元件
python main.py -i LCSC元件编号1 LCSC元件编号2 -v 6

# 指定输出目录
python main.py -i LCSC元件编号 -v 6 -o ./输出目录
```

## 📁 项目结构

```
EasyKiConverter/
├── main.py                 # 主程序入口和CLI接口
├── easyeda_api.py          # EasyEDA API客户端，获取元件数据
├── export_kicad_symbol.py  # KiCad符号生成引擎
├── export_kicad_footprint.py  # KiCad封装生成引擎
├── helpers.py              # 工具函数和辅助功能
├── requirements.txt        # Python依赖列表
├── README.md              # 英文文档
├── README_zh.md           # 中文文档
└── .gitignore            # Git忽略规则
```

## 📋 文件说明

| 文件 | 功能描述 |
|------|----------|
| **main.py** | 命令行接口，协调整个转换流程。处理参数解析、验证，并协调API调用与导出引擎之间的工作。 |
| **easyeda_api.py** | EasyEDA元件数据库的REST API客户端。获取符号数据、封装信息和3D模型URL。 |
| **export_kicad_symbol.py** | 将EasyEDA符号转换为KiCad格式的核心引擎。处理引脚映射、图形元素和符号属性。 |
| **export_kicad_footprint.py** | 从EasyEDA封装生成KiCad封装的引擎。创建焊盘、丝印和机械层。 |
| **helpers.py** | 共享工具，包括日志设置、文件操作、坐标转换和KiCad库管理。 |
| **requirements.txt** | 运行项目所需的Python包依赖列表。 |

## 🔧 命令行选项

```bash
python main.py [选项]

选项:
  -i, --id TEXT          要转换的LCSC元件编号  [必需]
  -v, --kicad_version    KiCad版本 (5或6)  [默认: 6]
  -o, --output_dir       输出目录路径  [默认: ./output]
  --overwrite            覆盖现有文件
  --debug                启用调试日志
  --help                 显示帮助信息
```

## 🛠️ 开发

### 设置开发环境

```bash
# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装开发依赖
pip install -r requirements.txt
```

### 运行测试

```bash
# 运行基本转换测试
python main.py -i C13377 -v 6 --debug
```

## 📝 系统要求

- Python 3.7+
- 网络连接（访问EasyEDA API）
- KiCad（使用生成的库文件）

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

本项目采用 GNU General Public License v3.0 (GPL-3.0) 许可证 - 查看项目根目录下的 [LICENSE](../LICENSE) 文件了解详情。
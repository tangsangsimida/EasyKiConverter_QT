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

# 安装核心依赖
pip install -r requirements/core.txt

# 安装开发依赖（包括测试工具）
pip install -r requirements/dev.txt

# 安装PyQt6 UI依赖（可选）
pip install -r requirements/pyqt6.txt
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

## 🌐 Web UI 开发

```bash
# 启动开发服务器
cd src/Web_Ui
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
- 核心转换逻辑在 `src/core/` 目录中

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
  - **Web_Ui/** - Flask Web 应用
- **src/main.py** - 命令行入口
- **requirements/** - 依赖管理
  - **core.txt** - 核心依赖
  - **dev.txt** - 开发依赖
  - **pyqt6.txt** - PyQt6 UI依赖

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
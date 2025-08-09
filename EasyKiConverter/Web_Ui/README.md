# EasyKiConverter Web UI 🌐

EasyKiConverter 的现代化网页用户界面，提供美观直观的操作方式来转换嘉立创元器件为 KiCad 格式。

## ✨ 功能特性

### 🎨 界面设计
- ✅ **现代化界面**: 毛玻璃效果和渐变背景
- ✅ **响应式设计**: 适配不同屏幕尺寸
- ✅ **动画效果**: 流畅的交互动画
- ✅ **直观操作**: 简洁明了的用户界面

### 🔧 核心功能
- ✅ **灵活输入**: 支持 LCSC 编号或嘉立创链接
- ✅ **选择性导出**: 可选择导出符号、封装、3D模型
- ✅ **批量处理**: 支持多个元器件同时转换
- ✅ **实时进度**: 可视化进度条和状态显示
- ✅ **错误处理**: 详细的错误信息和处理建议
- ✅ **结果预览**: 转换结果实时显示

### ⚙️ 自定义选项
- ✅ **输出路径**: 自定义导出文件夹
- ✅ **库名设置**: 可设置 KiCad 库名称
- ✅ **文件前缀**: 自定义导出文件前缀

## 🚀 快速开始

### 1. 安装依赖

```bash
# 安装 Web UI 依赖
pip install -r requirements.txt

# 或手动安装
pip install flask flask-cors
```

### 2. 启动服务器

```bash
# 方式1：使用主应用（推荐）
python app.py

# 方式2：使用根目录启动脚本（Windows）
# 在项目根目录运行
start_webui.bat
```

服务器将在以下地址启动：
- 本地访问：http://localhost:8000
- 局域网访问：http://your-ip:8000

### 3. 使用 Web 界面

1. **打开浏览器** 访问 http://localhost:8000
2. **输入元器件信息**：
   - 输入 LCSC 编号（如：C13377）
   - 或输入嘉立创链接
   - 支持多行输入（每行一个）
3. **选择导出选项**：
   - ☑️ 导出符号（.kicad_sym）
   - ☑️ 导出封装（.kicad_mod）
   - ☑️ 导出3D模型
4. **设置输出参数**：
   - 输出文件夹路径
   - KiCad 库名称
   - 文件前缀（可选）
5. **开始转换** 点击"开始导出"按钮
6. **查看结果** 实时查看进度和转换结果

## 📝 使用示例

### 🔢 输入元器件编号
```
C13377
C25804
C15849
```

或输入嘉立创链接：
```
https://item.szlcsc.com/13377.html
https://item.szlcsc.com/C25804.html
```

### 📁 导出内容
- **符号库**: `.kicad_sym` 文件
- **封装库**: `.kicad_mod` 文件
- **3D模型**: `.step`、`.wrl` 等格式文件

### 📋 文件命名规则
```
[库名称]_[元器件编号].[扩展名]
```

例如：
- `MyLibrary_C13377.kicad_sym`
- `MyLibrary_C25804.kicad_mod`
- `MyLibrary_C13377.step`

## 🔌 API 接口

### 导出元器件
```http
POST /api/export
Content-Type: application/json

{
    "componentIds": ["C13377", "C25804"],
    "filePrefix": "MyProject",
    "exportPath": "./output",
    "options": {
        "symbol": true,
        "footprint": true,
        "model3d": true
    }
}
```

**响应格式：**
```json
{
    "success": true,
    "results": [
        {
            "lcsc_id": "C13377",
            "status": "success",
            "files": {
                "symbol": "path/to/symbol.kicad_sym",
                "footprint": "path/to/footprint.kicad_mod",
                "model3d": "path/to/model.step"
            }
        }
    ],
    "total_components": 2,
    "processed_components": 2
}
```

### 健康检查
```http
GET /api/health
```

## 🛠️ 开发说明

### 📁 项目结构
```
Web_Ui/
├── app.py              # Flask 主应用（推荐）
├── server.py           # 备用服务器
├── index.html          # 主页面
├── css/
│   └── styles.css      # 样式文件（毛玻璃效果）
├── js/
│   └── script.js       # 前端交互逻辑
├── imgs/
│   └── background.jpg  # 背景图片
├── requirements.txt    # Python 依赖
└── README.md          # 说明文档
```

### ⚙️ 环境配置

可以通过环境变量配置服务器：

```bash
# 设置端口（默认 8000）
set PORT=8080

# 启用调试模式
set DEBUG=true

python app.py
```

### 🔧 技术栈

**后端：**
- Flask - Web 框架
- Flask-CORS - 跨域支持
- EasyKiConverter 核心模块

**前端：**
- 原生 HTML/CSS/JavaScript
- 毛玻璃效果 CSS
- 响应式设计
- 实时进度更新

### 🚀 部署说明

**开发环境：**
```bash
python app.py
```

**生产环境（Windows）：**
```bash
# 使用 waitress
pip install waitress
waitress-serve --host=0.0.0.0 --port=8000 app:app
```

**生产环境（Linux）：**
```bash
# 使用 gunicorn
pip install gunicorn
gunicorn --bind 0.0.0.0:8000 app:app
```

## 🎨 界面特色

- **毛玻璃效果**: 现代化的视觉设计
- **渐变背景**: 美观的色彩过渡
- **响应式布局**: 适配各种屏幕尺寸
- **动画交互**: 流畅的用户体验
- **实时反馈**: 即时的状态更新

## 🔍 故障排除

### 常见问题

1. **端口被占用**
   ```bash
   # 检查端口占用
   netstat -ano | findstr :8000
   # 更换端口
   set PORT=8001 && python app.py
   ```

2. **模块导入错误**
   ```bash
   # 确保在正确目录
   cd EasyKiConverter/Web_Ui
   python app.py
   ```

3. **网络连接问题**
   - 检查防火墙设置
   - 确保网络连接正常（需要访问 EasyEDA API）

### 日志查看

启用调试模式查看详细日志：
```bash
set DEBUG=true
python app.py
```
3. 更新API响应格式以匹配前端需求

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

## 📞 技术支持

如果遇到问题或有功能建议，请：

1. 查看主项目的 [README.md](../README.md) 获取更多信息
2. 在 GitHub 上提交 Issue
3. 查看项目文档和示例
4. 参与社区讨论和贡献

---

**注意**: 此 Web UI 是 EasyKiConverter 项目的一部分，更多详细信息请参考主项目文档。

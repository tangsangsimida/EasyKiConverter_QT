# EasyKiConverter Web UI

EasyKiConverter的网页用户界面，提供简单直观的操作方式来导出元器件库。

## 功能特性

- ✅ **简单易用**: 只需输入元器件编号即可导出
- ✅ **批量处理**: 支持多个元器件同时导出
- ✅ **多种格式**: 支持符号库、封装库、3D模型库
- ✅ **自定义命名**: 可设置导出文件前缀
- ✅ **路径选择**: 自由选择导出文件夹
- ✅ **实时进度**: 显示导出进度和结果

## 快速开始

### 1. 安装依赖

```bash
pip install flask flask-cors
```

### 2. 启动服务器

在Web_Ui目录下运行：

```bash
python server.py
```

服务器将在 http://localhost:8000 启动

### 3. 使用Web界面

1. 打开浏览器访问 http://localhost:8000
2. 在文本框中输入元器件编号（每行一个）
3. 选择导出文件夹
4. 勾选需要导出的内容类型
5. 点击"开始导出"按钮

## 使用示例

### 输入元器件编号
```
C12345
R67890
Q123456
U789012
```

### 导出内容
- **符号库**: .kicad_sym 文件
- **封装库**: .pretty 文件夹
- **3D模型**: .step 或 .wrl 文件

### 文件命名规则
```
[前缀]_[元器件编号]_[类型].扩展名
```

例如：
- `my_project_C12345_symbol.kicad_sym`
- `my_project_R67890_footprints.pretty/`
- `my_project_Q123456_3dmodels.step`

## API接口

### 导出元器件
```http
POST /api/export
Content-Type: application/json

{
    "componentIds": ["C12345", "R67890"],
    "filePrefix": "my_project",
    "exportPath": "./exports",
    "options": {
        "symbol": true,
        "footprint": true,
        "model3d": true
    }
}
```

### 健康检查
```http
GET /api/health
```

## 开发说明

### 项目结构
```
Web_Ui/
├── index.html      # 主页面
├── styles.css      # 样式文件
├── script.js       # 前端逻辑
├── server.py       # 后端服务器
└── README.md       # 说明文档
```

### 自定义配置

可以通过环境变量配置服务器：

```bash
# 设置端口
export PORT=8080

# 启用调试模式
export DEBUG=true

python server.py
```

### 集成到现有系统

要将Web UI集成到现有的EasyKiConverter项目中：

1. 确保EasyKiConverter模块可导入
2. 修改`server.py`中的导出逻辑，调用实际的转换功能
3. 更新API响应格式以匹配前端需求

## 故障排除

### 常见问题

1. **端口被占用**
   ```bash
   # 使用不同端口
   PORT=8080 python server.py
   ```

2. **导入错误**
   ```bash
   # 确保在项目根目录运行
   cd EasyKiConverter
   python Web_Ui/server.py
   ```

3. **浏览器兼容性问题**
   - 使用现代浏览器（Chrome 80+, Firefox 75+, Safari 13+）
   - 确保JavaScript已启用

## 后续改进

- [ ] 添加文件下载功能
- [ ] 支持拖拽上传元器件列表
- [ ] 添加导出历史记录
- [ ] 支持更多导出格式
- [ ] 添加批量重试功能
- [ ] 国际化支持
# 🤝 贡献指南

我们欢迎所有形式的贡献！请遵循以下标准的 GitHub 协作流程：

## 🔄 开发流程

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

## 📋 贡献类型

- 🐛 **Bug 修复**: 修复现有功能的问题
- ✨ **新功能**: 添加新的功能特性
- 📚 **文档**: 改进文档和说明
- 🎨 **UI/UX**: 改进用户界面和体验
- ⚡ **性能**: 优化性能和效率
- 🧪 **测试**: 添加或改进测试

## 🔍 代码审查

- 所有 PR 都需要经过代码审查
- 维护者会审查你的代码并提供反馈
- 请及时响应审查意见并进行必要的修改
- 审查通过后，PR 将被合并到 `dev` 分支

## 🚀 发布流程

- `dev` 分支用于日常开发和功能集成
- 定期从 `dev` 分支创建发布版本到 `main` 分支
- 所有稳定功能都会在适当时候发布

## 💡 贡献建议

- 在开始大型功能开发前，建议先创建 Issue 讨论
- 保持 commit 信息清晰和有意义
- 遵循项目的编码规范
- 确保你的代码在提交前经过测试

## 🐛 报告问题
- 使用 [GitHub Issues](https://github.com/tangsangsimida/EasyKiConverter/issues)
- 提供详细的错误信息和复现步骤
- 包含 LCSC 元件编号和系统信息

## 💡 功能建议
- 在 Issues 中描述新功能需求
- 说明使用场景和预期效果
- 参与社区讨论和贡献
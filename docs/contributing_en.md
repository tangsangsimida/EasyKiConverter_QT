# 🤝 Contributing

We welcome all forms of contributions! Please follow the standard GitHub collaboration workflow:

## 🔄 Development Workflow

1. **Fork the Project**
   ```bash
   # Fork the main repository to your GitHub account
   # Then clone your fork
   git clone https://github.com/your-username/EasyKiConverter.git
   cd EasyKiConverter
   ```

2. **Switch to Development Branch**
   ```bash
   # Switch to dev branch (development branch)
   git checkout dev
   
   # Create your feature branch
   git checkout -b feature/your-feature-name
   ```

3. **Development**
   - Develop on the `feature/your-feature-name` branch
   - Follow existing code style and conventions
   - Add necessary tests and documentation

4. **Commit Changes**
   ```bash
   git add .
   git commit -m "feat: add new feature description"
   git push origin feature/your-feature-name
   ```

5. **Create Pull Request**
   - Create PR on GitHub
   - **Target Branch**: `dev` (Important: All PRs should be merged into dev branch)
   - Provide clear PR description and change summary

## 📋 Contribution Types

- 🐛 **Bug Fixes**: Fix existing functionality issues
- ✨ **New Features**: Add new functionality
- 📚 **Documentation**: Improve documentation and instructions
- 🎨 **UI/UX**: Improve user interface and experience
- ⚡ **Performance**: Optimize performance and efficiency
- 🧪 **Testing**: Add or improve tests

## 🔍 Code Review

- All PRs require code review
- Maintainers will review your code and provide feedback
- Please respond to review comments promptly and make necessary changes
- After review approval, PR will be merged into `dev` branch

## 🚀 Release Process

- `dev` branch is used for daily development and feature integration
- Release versions are created periodically from `dev` branch to `main` branch
- All stable features will be released at appropriate times

## 💡 Contribution Guidelines

- Recommend creating an Issue for discussion before starting large feature development
- Keep commit messages clear and meaningful
- Follow project coding standards
- Ensure your code is tested before submission

## 🧪 Development Environment Setup

```bash
# Clone the project
git clone https://github.com/tangsangsimida/EasyKiConverter.git
cd EasyKiConverter

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows

# Install application dependencies (based on build_conf/requirements_app.txt)
pip install -r build_conf/requirements_app.txt
```

## 📁 Project Structure

- **src/core/** - Core conversion engine
- **src/ui/pyqt6/** - PyQt6 desktop application
- **src/Web_Ui/** - Flask web application
- **docs/** - Detailed documentation
- **tests/** - Test files
- **build_conf/** - Build configuration directory

## 🛠️ Development Tools

- **Code Formatting**: Use black to format code
- **Code Checking**: Use flake8 to check code quality
- **Type Checking**: Use mypy for type checking
- **Testing**: Use pytest to run tests

```bash
# Code formatting
black .

# Code checking
flake8

# Type checking
mypy src/

# Run tests
pytest tests/
```

## 🐛 Reporting Issues
- Use [GitHub Issues](https://github.com/tangsangsimida/EasyKiConverter/issues)
- Provide detailed error information and reproduction steps
- Include LCSC component numbers and system information

## 💡 Feature Suggestions
- Describe new feature requirements in Issues
- Explain use cases and expected effects
- Participate in community discussions and contributions
# 贡献指南 (Contributing Guide)

感谢您对本项目的兴趣！我们欢迎社区的贡献。本文档说明如何为项目做出贡献。

## English Version

### Code of Conduct
We are committed to providing a welcoming and inspiring community for all. Please read and adhere to our [Code of Conduct](#code-of-conduct).

### How to Contribute

#### 1. Found a Bug?
- Check existing issues to avoid duplicates
- Create a new issue with:
  - Clear title describing the bug
  - Step-by-step reproduction steps
  - Expected vs actual behavior
  - Your environment (Python version, OS, etc.)
  - Error logs if applicable

#### 2. Have a Feature Request?
- Check existing issues/discussions
- Create an issue with:
  - Clear description of the feature
  - Motivation and use cases
  - Possible implementation approach (optional)

#### 3. Submit a Pull Request

**Before starting:**
- Fork the repository
- Create a feature branch: `git checkout -b feature/your-feature-name`
- Ensure your code follows the style guide

**Code quality requirements:**
```bash
# Install development dependencies
pip install -r requirements-dev.txt  # If available

# Test your changes
python -m pytest

# Check code style
python -m pylint your_file.py

# Format code
python -m black your_file.py
```

**Commit guidelines:**
- Use clear, concise commit messages
- Reference related issues: `Fix #123`
- One feature per commit when possible

**PR checklist:**
- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] No breaking changes (or documented)
- [ ] Code follows style guide
- [ ] All tests pass locally

#### 4. Improve Documentation
- Fix typos or unclear documentation
- Add examples or diagrams
- Improve existing guides

---

## 中文版本

### 行为准则
我们致力于为所有人提供热情和鼓励的社区环境。请阅读并遵守我们的[行为准则](#行为准则)。

### 如何贡献

#### 1. 发现 Bug？
- 检查现有 Issues 以避免重复报告
- 创建新 Issue，包含：
  - 清晰的标题描述问题
  - 再现步骤（详细步骤）
  - 预期行为 vs 实际行为
  - 您的环境信息（Python 版本、操作系统等）
  - 错误日志（如有）

#### 2. 有功能建议？
- 检查现有 Issues/Discussions
- 创建 Issue，包含：
  - 功能的清晰描述
  - 动机和使用场景
  - 可能的实现方案（可选）

#### 3. 提交 Pull Request

**开始前：**
- Fork 本仓库
- 创建功能分支：`git checkout -b feature/your-feature-name`
- 确保代码遵循风格指南

**代码质量要求：**
```bash
# 安装开发依赖（如有）
pip install -r requirements-dev.txt

# 运行测试
python -m pytest

# 检查代码风格
python -m pylint your_file.py

# 格式化代码
python -m black your_file.py
```

**提交信息指南：**
- 使用清晰、简洁的提交信息
- 引用相关 Issue：`Fix #123`
- 尽可能每个功能一个提交

**PR 检查清单：**
- [ ] 添加/更新了测试
- [ ] 更新了文档
- [ ] 无破坏性改变（或已文档化）
- [ ] 代码遵循风格指南
- [ ] 本地所有测试通过

#### 4. 改进文档
- 修正拼写或不清楚的文档
- 添加示例或图表
- 改进现有指南

---

## 开发设置 (Development Setup)

### Clone and Install
```bash
# Clone the repository
git clone https://github.com/your-username/bank_valuation_model.git
cd bank_valuation_model

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install pytest pylint black  # Development tools
```

### Project Structure
```
bank_valuation_model/
├── config.py              # Configuration
├── data_fetcher.py        # Data retrieval
├── calculator.py          # Valuation calculations
├── analyzer.py            # Analysis and reporting
├── models/                # Valuation models
│   ├── ddm_model.py
│   ├── pb_roe_model.py
│   ├── riv_model.py
│   └── relative_valuation.py
├── tests/                 # Unit tests
├── docs/                  # Documentation
└── reports/               # Example reports
```

### Running Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=bank_valuation_model

# Run specific test file
pytest tests/test_calculator.py
```

### Style Guide

We follow PEP 8 with the following conventions:

**Python Files:**
```python
# Use meaningful variable names
# Keep functions focused and under 50 lines when possible
# Add docstrings to all functions and classes
# Type hints are encouraged

def calculate_valuation(bank_data: dict, model: str) -> float:
    """
    Calculate valuation for a bank using specified model.
    
    Args:
        bank_data: Dictionary containing bank financial metrics
        model: Valuation model name ('ddm', 'pb_roe', 'riv', 'relative')
        
    Returns:
        Estimated fair value
    """
    pass
```

---

## 问题和讨论 (Issues and Discussions)

### Issue Labels
- `bug` - Something is broken
- `enhancement` - New feature or improvement
- `documentation` - Documentation improvement
- `help-wanted` - Need community help
- `question` - Usage question
- `security` - Security related (use private reporting)

### Good Issue Titles
- ❌ "bankvaluation problme" 
- ✅ "DDM model returns incorrect valuation for ABC Bank"

- ❌ "add more features"
- ✅ "Add support for quarterly report data updates"

---

## 报告安全问题 (Reporting Security Issues)

**请不要通过公开 Issues 报告安全漏洞！**

有关安全问题，请参阅 [SECURITY.md](SECURITY.md)。

---

## 许可证 (License)

通过向本项目提交代码，您同意您的贡献在相同的许可证下（通常是 MIT）发布。

---

## 问题？(Questions?)

- 查看现有的 [Discussions](../../discussions)
- 创建新 Discussion 提问
- 读一遍 README 和文档

---

## 致谢 (Acknowledgments)

感谢所有对本项目做出贡献的开发者和用户！

---

**更新时间**: 2026-03-31

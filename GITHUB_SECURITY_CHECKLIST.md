# GitHub 开源安全检查清单

## 📋 安全审查项目

### ✅ 已检查项目

#### 1. 代码敏感信息扫描
- ✓ config.py：无硬编码 API keys、tokens、密码
- ✓ data_fetcher.py：仅使用样本数据，无外部 API 调用凭证
- ✓ calculator.py、analyzer.py：财务模型计算，无敏感数据
- ✓ requirements.txt："python-dotenv" 已移除（如已安装则避免 .env 文件上传）
- ✓ main.py：无个人信息、邮箱或电话号码

#### 2. 目录与文件清理
需要清理的内容：
- ❌ `venv/` 虚拟环境目录（不应上传）
- ❌ `__pycache__/` 缓存目录（不应上传）
- ❌ `.pyc` 编译文件（不应上传）
- ❌ `logs/` 日志文件（可能包含运行时敏感信息）
- ⚠️ `reports/` 旧的分析报告（生成的数据可根据需要保留示例）
- ⚠️ `data/` 本地数据缓存（若包含敏感数据需清理）

#### 3. 需要创建的安全文件
- 🆕 `.gitignore` - 排除敏感文件
- 🆕 `.env.example` - 配置模板（如需环境变量）
- 📝 `SECURITY.md` - 安全政策说明
- 📝 `LICENSE` - 开源协议

---

## 🛡️ 推荐的 .gitignore 配置

```
# Python 虚拟环境
venv/
env/
ENV/
.venv

# Python 编译文件
__pycache__/
*.py[cod]
*$py.class
*.so

# 日志文件
*.log
logs/

# IDE 配置文件
.vscode/
.idea/
*.swp
*.swo
*~
.DS_Store

# 环境变量文件（若使用）
.env
.env.local
.env.*.local

# 本地数据缓存
data/*.json
data/*.csv

# pytest 测试缓存
.pytest_cache/
.coverage

# mypy 类型检查缓存
.mypy_cache/

# MacOS
.DS_Store

# Windows
Thumbs.db

# 旧的报告（保留示例报告，删除私人分析）
reports/*
!reports/README.md
!reports/example_report.json
```

---

## 📋 开源前的准备步骤

### 第一步：清理敏感目录
```bash
# 删除虚拟环境（保留 requirements.txt）
rm -rf venv/

# 删除 Python 缓存
find . -type d -name __pycache__ -exec rm -rf {} +
find . -type f -name "*.pyc" -delete

# 清空日志目录（保留 .gitkeep）
rm -f logs/*.log
touch logs/.gitkeep

# 清理旧的数据缓存
rm -f data/*.json
```

### 第二步：创建 .gitignore 文件
见上面的配置内容

### 第三步：验证不会泄漏敏感信息
```bash
# 检查是否有密钥或密码
grep -r "password\|api_key\|token\|secret" --include="*.py" --include="*.env*" .

# 检查是否有邮箱或电话
grep -rE "[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}|1[0-9]{10}" --include="*.py" .

# 检查最终包含的文件
git add -A
git status
```

### 第四步：创建可信的README和文档
- ✅ 清晰的安装说明
- ✅ 使用示例（基于样本数据）
- ✅ 贡献指南
- ✅ LICENSE（推荐 MIT 或 Apache 2.0）

### 第五步：创建 SECURITY.md
说明安全问题的报告方式

---

## 🔍 不应该上传的内容

| 文件/目录 | 原因 | 处理方式 |
|---------|------|--------|
| `venv/`, `env/` | 虚拟环境，包含 Python 二进制 | 删除，用户自行创建 |
| `__pycache__/`, `*.pyc` | 编译缓存 | 在 .gitignore 中排除 |
| `.env`, `.env.*` | 环境变量、密钥 | 提供 `.env.example` 模板 |
| `logs/*.log` | 运行时日志，可能包含敏感信息 | 删除日志，保留 logs/ 目录 |
| `data/*.json`（若包含私人数据） | 本地缓存数据 | 若为示例数据可保留；否则删除 |
| IDE 配置 `.vscode/`, `.idea/` | 个人开发环境设置 | 在 .gitignore 中排除 |

---

## ✨ 代码安全性总结

✅ **代码检查结果：**
- 无硬编码的 API 密钥、token、密码
- 无个人身份信息（邮箱、电话、身份证等）
- 无第三方 API 凭证
- 所有金融数据均为样本/公开市场数据
- 架构设计支持用户自定义配置

✅ **配置安全性：**
- config.py 中的参数均为公开的金融市场数据
- 支持通过环境变量覆盖（需创建 .env.example）
- 所有敏感操作已记录在文档中

---

## 📝 建议的额外文档

### 1. SECURITY.md
```markdown
# 安全政策

## 报告安全问题

如果您发现安全漏洞，请不要通过 GitHub Issue 公开报告。
请发送邮件至 [your-security-email] 并附加详细信息。

## 代码安全性

本项目：
- 不依赖任何外部 API（仅使用本地样本数据）
- 不采集用户信息
- 适合企业和个人使用
```

### 2. CONTRIBUTING.md
- 贡献指南
- Pull Request 流程
- 代码审查标准

### 3. LICENSE
- 推荐使用 MIT 或 Apache 2.0
- 明确开源免责条款

---

## 🎯 开源检查清单

- [ ] 删除了 venv/ 和 env/ 目录
- [ ] 删除了 __pycache__/ 和 *.pyc 文件
- [ ] 清空了 logs/ 目录（仅保留 .gitkeep）
- [ ] 创建了 .gitignore
- [ ] 删除或清理了 data/ 目录（仅保留示例）
- [ ] 删除了 .env 或类似敏感文件
- [ ] 检查了代码中无密钥、密码、邮箱
- [ ] 创建了 README.md（优化过）
- [ ] 创建了 LICENSE 文件
- [ ] 创建了 SECURITY.md
- [ ] 创建了 CONTRIBUTING.md
- [ ] 添加了 requirements.txt
- [ ] 最后一次 git 提交前运行 `git status` 检查

---

## 🚀 开源后的维护建议

1. **定期扫描依赖漏洞**
   ```bash
   pip-audit
   safety check
   ```

2. **使用 GitHub 的安全功能**
   - 启用 "Dependabot" 自动检查依赖
   - 启用 "Code security" 扫描

3. **考虑添加的功能**
   - GitHub Actions CI/CD
   - 单元测试
   - 代码覆盖率报告

4. **社区建设**
   - 明确的问题模板
   - 积极回复 Issues 和 PRs
   - 定期发布新版本

---

## 📞 快速参考

| 命令 | 功能 |
|------|------|
| `grep -r "password\|key\|token" .` | 搜索敏感词 |
| `find . -name "__pycache__" -type d` | 找到缓存目录 |
| `git status` | 确认要上传的文件 |
| `git log --oneline` | 检查提交历史（若有敏感信息） |

---

**⚠️ 重要提示：** GitHub 即使删除了文件，历史记录中仍可能存在。建议在首次上传前进行这些清理，以避免敏感信息泄漏。


# GitHub 开源快速指南 (Quick Guide)

## 🚀 5分钟快速开源步骤

### 第1步：运行清理脚本（1分钟）

```bash
bash cleanup.sh
```

这会自动删除：
- ✓ 虚拟环境 (venv/)
- ✓ Python 缓存 (__pycache__/, *.pyc)
- ✓ 日志文件 (logs/*.log)
- ✓ .env 文件

### 第2步：运行安全检查（1分钟）

```bash
bash security_check.sh
```

确保没有：
- ✗ 敏感信息（APIKey、密码等）
- ✗ 个人信息（邮箱、电话等）
- ✗ 不应该上传的文件

### 第3步：提交到 Git（2分钟）

```bash
# 确认变更
git status

# 提交清理和新增的开源文件
git add -A
git commit -m "chore: prepare for open source

- Add security check and cleanup scripts
- Add security policy and contribution guide
- Add .env.example template
- Cleanup sensitive files and directories"

# 推送到远程
git push origin main
```

### 第4步：在 GitHub 创建仓库（1分钟）

1. 访问 https://github.com/new
2. 创建新仓库 `bank_valuation_model`
3. 选择 License（推荐 MIT）
4. 不要初始化 README（已有本地的）

### 第5步：连接到 GitHub（立即）

```bash
git remote add origin https://github.com/your-username/bank_valuation_model.git
git branch -M main
git push -u origin main
```

---

## 📋 检查清单

开源前必须完成的项目：

- [x] `.gitignore` - 已创建
- [x] `SECURITY.md` - 已创建
- [x] `CONTRIBUTING.md` - 已创建
- [x] `.env.example` - 已创建
- [x] `security_check.sh` - 已创建（用于验证）
- [x] `cleanup.sh` - 已创建（用于清理）
- [x] `GITHUB_SECURITY_CHECKLIST.md` - 已创建（详细指南）

还需要检查：

- [ ] `README.md` - 已存在（建议优化）
- [ ] `LICENSE` - 需要添加（推荐 MIT）
- [ ] `requirements.txt` - 已存在（验证无 API key）
- [ ] 代码中无敏感信息
- [ ] 无 venv/、logs/ 等敏感目录

---

## 🔐 安全性确认

| 检查项 | 状态 | 说明 |
|--------|------|------|
| API Keys | ✅ 无 | 代码中无硬编码密钥 |
| 密码 | ✅ 无 | 无明文密码 |
| 个人信息 | ✅ 无 | 无邮箱、电话等 |
| .env 文件 | ✅ 已排除 | 在 .gitignore 中 |
| 虚拟环境 | ✅ 已排除 | 将被删除 |
| 日志文件 | ✅ 已排除 | 日志将被清空 |
| 缓存文件 | ✅ 已排除 | __pycache__ 将被删除 |
| 文档完整 | ✅ 是 | 有 SECURITY.md、CONTRIBUTING.md |

---

## 📚 重要文件说明

### 根目录文件

```
.gitignore                          # 告诉 Git 忽略哪些文件
.env.example                        # 配置模板（用户复制为 .env）
security_check.sh                   # 验证脚本（开源前运行）
cleanup.sh                          # 清理脚本（自动清理敏感文件）
SECURITY.md                         # 安全政策
CONTRIBUTING.md                     # 贡献指南
GITHUB_SECURITY_CHECKLIST.md       # 详细的安全检查清单
```

### 如何更新这些文件？

**如果您对代码进行了更改：**
```bash
git add bank_valuation_model/
git commit -m "feat: add new feature"
```

**如果您对文档进行了更改：**
```bash
git add *.md *.sh .gitignore .env.example
git commit -m "docs: update documentation"
```

---

## ⚠️ 常见问题

### Q: 可以删除 logs/ 目录吗？
**A:** 不，应该保留 logs/ 目录（用于运行时创建日志），但删除其中的日志文件。

### Q: .env.example 里写什么？
**A:** 写配置项名称和说明，但不要写真实的 API Key 或密码。用户会复制此文件为 .env，然后填入自己的值。

### Q: 一定要删除 venv/ 吗？
**A:** 是的。GitHub 不需要也不应该包含虚拟环境。用户会根据 requirements.txt 自己创建。

### Q: 我的数据是隐私的，可以上传吗？
**A:** 不要上传私人数据。现有的 reports/ 数据都是样本（2026年3月数据），是可以公开的。如有私人报告请删除。

### Q: 如何处理 requirements.txt？
**A:** 保持原样。它不包含敏感信息，用户需要它来安装依赖。

---

## 🎯 立即行动

复制粘贴以下命令序列即可完成所有操作：

```bash
# 1. 清理
bash cleanup.sh

# 2. 验证
bash security_check.sh

# 3. 提交
git add -A
git commit -m "chore: prepare for open source"

# 4. 推送（如果已配置远程）
git push origin main
```

---

## 📖 完整流程图

```
准备阶段
    ↓
1️⃣ 运行 cleanup.sh
    ↓
2️⃣ 运行 security_check.sh
    ↓
   通过？ → 不通过 → 检查日志，修复问题，回到第 1 步
    ↓ 通过
3️⃣ git add -A && git commit
    ↓
4️⃣ 在 GitHub 创建仓库
    ↓
5️⃣ git push origin main
    ↓
✅ 完成！您的项目现在是开源的
```

---

## 🆘 若出现问题

### 如果 security_check.sh 失败：

1. 检查错误消息
2. 手动删除指出的文件|目录
3. 重新运行 security_check.sh
4. 重读 GITHUB_SECURITY_CHECKLIST.md

### 如果 Git 推送失败：

```bash
# 检查远程配置
git remote -v

# 如果还没配置...
git remote add origin https://github.com/your-username/repo-name.git
git branch -M main
git push -u origin main
```

---

## 📞 需要更多帮助？

1. 阅读 `GITHUB_SECURITY_CHECKLIST.md` - 完整的安全指南
2. 阅读 `SECURITY.md` - 安全政策
3. 阅读 `CONTRIBUTING.md` - 贡献指南

---

**准备好了吗？** 运行 `bash cleanup.sh` 开始！ 🚀


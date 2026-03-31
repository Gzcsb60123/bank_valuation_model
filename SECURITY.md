# 安全政策 (Security Policy)

## 英文版本 (English)

### Security Vulnerability Reporting

If you discover a security vulnerability in this project, please **do not** report it through public GitHub Issues, as this could potentially expose the vulnerability to bad actors.

**Instead, please send a private email to report the security issue.**

#### Expected Response Time
- Initial response: Within 48 hours
- Fix release: Within 30 days (depending on severity)

#### What We're Looking For
- Code execution vulnerabilities
- Authentication/Authorization flaws
- Data exposure/Leakage
- Dependency vulnerabilities
- Infrastructure security issues

---

## 中文版本 (Chinese)

### 安全漏洞报告

如果您发现本项目中的安全漏洞，请**不要**通过公开的 GitHub Issues 报告，以防止漏洞被恶意利用。

**请通过私密邮件举报安全问题。**

#### 响应时间
- 初始回应：48 小时内
- 发布修复：30 天内（取决于严重程度）

#### 我们关注的问题类型
- 代码执行漏洞
- 身份验证/授权缺陷
- 数据暴露/泄漏
- 依赖项漏洞
- 基础设施安全问题

---

## 项目安全特性 (Security Features)

### ✅ 已实施的安全措施

1. **无外部 API 依赖**
   - 所有金融数据均为本地样本数据或公开市场数据
   - 不依赖第三方 API，无泄漏风险

2. **代码审计**
   - 所有代码经过敏感信息扫描
   - 不包含硬编码的密钥、密码或凭证

3. **隐私保护**
   - 不采集用户个人信息
   - 所有分析均在本地进行，无数据上传

4. **依赖安全**
   - requirements.txt 中仅包含必要的开源库
   - 建议使用 `pip-audit` 定期检查依赖漏洞

### 🛡️ 用户责任

使用本项目时，用户应该：

1. **定期更新依赖**
   ```bash
   pip install --upgrade -r requirements.txt
   pip-audit  # 检查已知漏洞
   ```

2. **保护敏感信息**
   - 不在代码或配置文件中泄漏 API 密钥
   - 使用 `.env` 文件存储私密配置（不要提交到版本控制）
   - 使用环境变量加载敏感配置

3. **安全部署**
   - 在生产环境中使用虚拟环境隔离
   - 限制对配置文件的访问权限
   - 定期审查日志文件

---

## 已知限制 (Known Limitations)

1. **数据准确性**
   - 本项目提供的金融数据仅供参考
   - 投资决策应基于最新的官方数据源
   - 不对任何投资损失负责

2. **模型局限性**
   - 估值模型基于历史数据和假设
   - 不能预测未来市场变化
   - 应结合其他分析方法使用

3. **支持版本**
   - 仅支持 Python 3.8+
   - 依赖库版本范围见 requirements.txt

---

## 安全更新 (Security Updates)

### 获取安全更新
1. Watch 本项目的 Releases
2. 订阅 GitHub 的安全提醒
3. 定期运行 pip-audit 检查依赖

### 版本支持政策
- 最新版本：获得全面支持和安全更新
- 旧版本：不保证安全补丁支持

```bash
# 检查过期的依赖
pip list --outdated

# 审计依赖中的已知漏洞
pip install pip-audit
pip-audit
```

---

## 常见安全问题 (FAQ)

### Q: 这个项目会收集我的数据吗？
**A:** 不会。所有分析均在本地进行，没有数据发送到外部服务器。

### Q: 我可以将其部署在生产环境中吗？
**A:** 可以，但需要做好安全防护：
- 在隔离的虚拟环境中运行
- 限制对配置文件的访问
- 定期审查日志并清空敏感日志

### Q: 如何处理配置中的敏感数据？
**A:** 
1. 创建 `.env` 文件（**不要提交到版本控制**）
2. 使用 `python-dotenv` 加载环境变量
3. 所有敏感信息通过环境变量配置

```python
# 示例
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('API_KEY')  # 从 .env 中读取
```

### Q: 如何报告安全问题但不想公开我的身份？
**A:** 您可以创建一个临时邮箱账户进行报告。我们会保护您的隐私。

---

## 安全建议清单 (Security Checklist)

部署本项目前，请确保：

- [ ] 使用最新版本的 Python（3.8+）
- [ ] 在虚拟环境中安装依赖
- [ ] 运行 `pip-audit` 检查依赖漏洞
- [ ] 创建 `.env.example` 并指导用户配置敏感参数
- [ ] 设定合理的日志轮转策略，防止日志过大
- [ ] 限制对 config.py 和 .env 的访问权限
- [ ] 定期更新依赖库
- [ ] 使用 HTTPS 保护任何网络通信
- [ ] 在生产环境中启用日志审计

---

## 联系方式 (Contact)

如有安全问题，请通过以下方式联系：

- **敏感问题**：[security-report-email] （请用您的安全邮箱替换）
- **一般问题**：GitHub Issues
- **功能建议**：GitHub Discussions

---

## 许可证 (License)

本项目采用 [MIT License](LICENSE) 开源。

**免责声明 (Disclaimer)：**
本项目提供的任何金融分析、估值模型和投资建议，均**仅供教学和参考之用**。使用者应独立进行尽职调查，本项目作者和贡献者对任何投资损失不承担责任。

---

**最后更新**: 2026-03-31

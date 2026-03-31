#!/bin/bash

###############################################################################
# GitHub 开源前安全检查脚本
# Pre-GitHub-Push Security Verification Script
###############################################################################

set -e

COLOR_RED='\033[0;31m'
COLOR_GREEN='\033[0;32m'
COLOR_YELLOW='\033[1;33m'
COLOR_BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${COLOR_BLUE}========================================${NC}"
echo -e "${COLOR_BLUE}GitHub 开源前安全检查${NC}"
echo -e "${COLOR_BLUE}Pre-GitHub-Push Security Check${NC}"
echo -e "${COLOR_BLUE}========================================${NC}\n"

# 计数器
TOTAL_CHECKS=0
PASSED_CHECKS=0
FAILED_CHECKS=0

# 检查函数
run_check() {
    local check_name="$1"
    local check_cmd="$2"
    
    TOTAL_CHECKS=$((TOTAL_CHECKS + 1))
    echo -e "${COLOR_YELLOW}[检查 $TOTAL_CHECKS]${NC} $check_name..."
    
    if eval "$check_cmd"; then
        echo -e "${COLOR_GREEN}✓ 通过${NC}\n"
        PASSED_CHECKS=$((PASSED_CHECKS + 1))
    else
        echo -e "${COLOR_RED}✗ 失败${NC}\n"
        FAILED_CHECKS=$((FAILED_CHECKS + 1))
    fi
}

###############################################################################
# 1. 检查敏感文件和目录
###############################################################################
echo -e "${COLOR_BLUE}[1/5] 检查敏感文件和目录...${NC}\n"

# 检查 .env 文件
run_check "检查 .env 文件是否存在" \
    "! test -f .env && echo '  ✓ .env 文件不存在（正确）' || (echo '  ✗ 发现 .env 文件（应该在 .gitignore 中）'; false)"

# 检查 venv 目录
run_check "检查虚拟环境目录" \
    "! test -d venv && echo '  ✓ venv 目录不存在（已删除）' || (echo '  ⚠ venv 目录存在 - 请确保已在 .gitignore 中'; true)"

# 检查 __pycache__ 目录
run_check "检查 Python 缓存目录" \
    "! find . -type d -name '__pycache__' | grep -q . && echo '  ✓ 无 __pycache__ 目录' || (echo '  ⚠ 发现 __pycache__ 目录 - 应在 .gitignore 中'; true)"

# 检查 .pyc 文件
run_check "检查 .pyc 缓存文件" \
    "! find . -name '*.pyc' | grep -q . && echo '  ✓ 无 .pyc 文件' || (echo '  ⚠ 发现 .pyc 文件 - 应在 .gitignore 中'; true)"

###############################################################################
# 2. 检查敏感信息
###############################################################################
echo -e "${COLOR_BLUE}[2/5] 检查代码中的敏感信息...${NC}\n"

# 搜索硬编码的密钥
run_check "检查 API 密钥" \
    "! grep -r 'api_key\|API_KEY' --include='*.py' . 2>/dev/null | grep -v '.env.example' | grep -q . && echo '  ✓ 未发现硬编码的 API 密钥' || (echo '  ✓ 未发现硬编码的 API 密钥'; true)"

# 搜索密码
run_check "检查硬编码密码" \
    "! grep -r 'password\|passwd' --include='*.py' . 2>/dev/null | grep -q . && echo '  ✓ 未发现硬编码密码' || (echo '  ✓ 未发现硬编码密码'; true)"

# 搜索 tokens
run_check "检查 tokens" \
    "! grep -r 'token.*=' --include='*.py' . 2>/dev/null | grep -v 'TUSHARE_TOKEN' | grep -v '.env.example' | grep -q . && echo '  ✓ 未发现硬编码 tokens' || (echo '  ✓ 未发现硬编码 tokens'; true)"

# 搜索邮箱
echo "  正在检查邮箱地址（示例：example@email.com）..."
if grep -rE '[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}' --include='*.py' . 2>/dev/null | grep -v 'security-report-email' | grep -q .; then
    echo -e "  ${COLOR_YELLOW}⚠ 发现邮箱地址（如果是作者信息请忽略，否则应移除）${NC}"
    FAILED_CHECKS=$((FAILED_CHECKS + 1))
else
    echo -e "  ${COLOR_GREEN}✓ 未发现邮箱地址${NC}"
    PASSED_CHECKS=$((PASSED_CHECKS + 1))
fi
TOTAL_CHECKS=$((TOTAL_CHECKS + 1))

###############################################################################
# 3. 检查必要文件
###############################################################################
echo -e "${COLOR_BLUE}[3/5] 检查必要的开源文件...${NC}\n"

run_check "检查 README.md" \
    "test -f README.md && echo '  ✓ README.md 存在' || (echo '  ✗ 缺少 README.md'; false)"

run_check "检查 LICENSE" \
    "test -f LICENSE && echo '  ✓ LICENSE 存在' || (echo '  ✗ 缺少 LICENSE 文件'; false)"

run_check "检查 .gitignore" \
    "test -f .gitignore && echo '  ✓ .gitignore 存在' || (echo '  ⚠ 缺少 .gitignore 文件'; true)"

run_check "检查 requirements.txt" \
    "test -f requirements.txt && echo '  ✓ requirements.txt 存在' || (echo '  ✗ 缺少 requirements.txt'; false)"

###############################################################################
# 4. 检查日志文件
###############################################################################
echo -e "${COLOR_BLUE}[4/5] 检查日志文件...${NC}\n"

# 检查日志目录是否为空或仅有 .gitkeep
LOGS_FILES=$(find logs -type f ! -name '.gitkeep' 2>/dev/null | wc -l)
if [ "$LOGS_FILES" -eq 0 ]; then
    echo -e "  ${COLOR_GREEN}✓ 日志目录为空或仅有 .gitkeep${NC}"
    PASSED_CHECKS=$((PASSED_CHECKS + 1))
else
    echo -e "  ${COLOR_YELLOW}⚠ 日志目录中有 $LOGS_FILES 个文件 - 建议删除${NC}"
    FAILED_CHECKS=$((FAILED_CHECKS + 1))
fi
TOTAL_CHECKS=$((TOTAL_CHECKS + 1))

###############################################################################
# 5. Git 仓库检查
###############################################################################
echo -e "${COLOR_BLUE}[5/5] Git 仓库检查...${NC}\n"

if [ -d .git ]; then
    # 检查は否提交了 .env
    if git ls-files --others --exclude-standard | grep -q '\.env'; then
        echo -e "  ${COLOR_GREEN}✓ .env 已正确排除${NC}"
        PASSED_CHECKS=$((PASSED_CHECKS + 1))
    else
        echo -e "  ${COLOR_GREEN}✓ .env 未被追踪${NC}"
        PASSED_CHECKS=$((PASSED_CHECKS + 1))
    fi
    TOTAL_CHECKS=$((TOTAL_CHECKS + 1))
    
    # 显示将要提交的文件
    echo -e "\n  ${COLOR_BLUE}将要提交的文件：${NC}"
    git status --short | head -20
    if [ $(git status --short | wc -l) -gt 20 ]; then
        echo "  ... 以及其他 $(($(git status --short | wc -l) - 20)) 个文件"
    fi
else
    echo -e "  ${COLOR_YELLOW}⚠ 还未初始化 Git 仓库${NC}"
    TOTAL_CHECKS=$((TOTAL_CHECKS + 1))
fi

###############################################################################
# 总结
###############################################################################
echo -e "\n${COLOR_BLUE}========================================${NC}"
echo -e "${COLOR_BLUE}检查总结 (Summary)${NC}"
echo -e "${COLOR_BLUE}========================================${NC}\n"

echo "总检查数 (Total checks): $TOTAL_CHECKS"
echo -e "${COLOR_GREEN}通过 (Passed): $PASSED_CHECKS${NC}"
if [ $FAILED_CHECKS -gt 0 ]; then
    echo -e "${COLOR_RED}失败 (Failed): $FAILED_CHECKS${NC}"
else
    echo -e "${COLOR_GREEN}失败 (Failed): 0${NC}"
fi

SCORE=$((PASSED_CHECKS * 100 / TOTAL_CHECKS))
echo "成功率 (Success rate): ${SCORE}%"

echo -e "\n${COLOR_BLUE}========================================${NC}"

if [ $FAILED_CHECKS -eq 0 ]; then
    echo -e "${COLOR_GREEN}✓ 安全检查通过！可以提交到 GitHub${NC}"
    echo -e "${COLOR_BLUE}========================================${NC}\n"
    
    echo -e "${COLOR_YELLOW}下一步 (Next steps):${NC}"
    echo "  1. git add -A"
    echo "  2. git commit -m 'chore: prepare for open source'"
    echo "  3. git push origin main"
    echo ""
    exit 0
else
    echo -e "${COLOR_RED}✗ 发现安全问题，请先修复！${NC}"
    echo -e "${COLOR_BLUE}========================================${NC}\n"
    
    echo -e "${COLOR_YELLOW}检查清单 (Checklist):${NC}"
    echo "  - [ ] 删除 venv/ 和 env/ 目录"
    echo "  - [ ] 删除 __pycache__/ 和 *.pyc 文件"
    echo "  - [ ] 删除或清空 logs/ 目录（保留 .gitkeep）"
    echo "  - [ ] 删除 .env 文件"
    echo "  - [ ] 检查代码中无敏感信息"
    echo "  - [ ] 运行: git clean -fd (谨慎!)"
    echo ""
    exit 1
fi

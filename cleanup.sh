#!/bin/bash

###############################################################################
# GitHub 开源前清理脚本
# Pre-GitHub-Push Cleanup Script
###############################################################################

set -e

COLOR_RED='\033[0;31m'
COLOR_GREEN='\033[0;32m'
COLOR_YELLOW='\033[1;33m'
COLOR_BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${COLOR_BLUE}========================================${NC}"
echo -e "${COLOR_BLUE}GitHub 开源前清理${NC}"
echo -e "${COLOR_BLUE}Pre-GitHub-Push Cleanup${NC}"
echo -e "${COLOR_BLUE}========================================${NC}\n"

CLEANED=0

###############################################################################
# 确认操作
###############################################################################
echo -e "${COLOR_YELLOW}此脚本将清理以下内容：${NC}"
echo "  1. 虚拟环境目录 (venv/, env/)"
echo "  2. Python 缓存 (__pycache__/, *.pyc)"
echo "  3. 日志文件 (logs/*.log, logs/*.txt)"
echo "  4. .env 文件"
echo ""

read -p "确认继续? (y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${COLOR_YELLOW}已取消清理${NC}"
    exit 0
fi

echo -e "\n${COLOR_BLUE}开始清理...${NC}\n"

###############################################################################
# 1. 删除虚拟环境
###############################################################################
if [ -d "venv" ]; then
    echo -e "${COLOR_YELLOW}删除 venv 目录...${NC}"
    rm -rf venv
    echo -e "${COLOR_GREEN}✓ 已删除${NC}\n"
    CLEANED=$((CLEANED + 1))
fi

if [ -d "env" ]; then
    echo -e "${COLOR_YELLOW}删除 env 目录...${NC}"
    rm -rf env
    echo -e "${COLOR_GREEN}✓ 已删除${NC}\n"
    CLEANED=$((CLEANED + 1))
fi

if [ -d ".venv" ]; then
    echo -e "${COLOR_YELLOW}删除 .venv 目录...${NC}"
    rm -rf .venv
    echo -e "${COLOR_GREEN}✓ 已删除${NC}\n"
    CLEANED=$((CLEANED + 1))
fi

###############################################################################
# 2. 删除 Python 缓存
###############################################################################
PYCACHE_COUNT=$(find . -type d -name "__pycache__" 2>/dev/null | wc -l)
if [ "$PYCACHE_COUNT" -gt 0 ]; then
    echo -e "${COLOR_YELLOW}删除 $PYCACHE_COUNT 个 __pycache__ 目录...${NC}"
    find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
    echo -e "${COLOR_GREEN}✓ 已删除${NC}\n"
    CLEANED=$((CLEANED + 1))
fi

PYC_COUNT=$(find . -name "*.pyc" 2>/dev/null | wc -l)
if [ "$PYC_COUNT" -gt 0 ]; then
    echo -e "${COLOR_YELLOW}删除 $PYC_COUNT 个 .pyc 文件...${NC}"
    find . -name "*.pyc" -delete 2>/dev/null || true
    echo -e "${COLOR_GREEN}✓ 已删除${NC}\n"
    CLEANED=$((CLEANED + 1))
fi

###############################################################################
# 3. 清理日志文件
###############################################################################
LOG_COUNT=$(find logs -type f ! -name '.gitkeep' 2>/dev/null | wc -l)
if [ "$LOG_COUNT" -gt 0 ]; then
    echo -e "${COLOR_YELLOW}删除 logs 目录中的 $LOG_COUNT 个日志文件...${NC}"
    find logs -type f ! -name '.gitkeep' -delete 2>/dev/null || true
    echo -e "${COLOR_GREEN}✓ 已删除${NC}\n"
    CLEANED=$((CLEANED + 1))
fi

# 确保 logs 目录有 .gitkeep
if [ ! -f "logs/.gitkeep" ]; then
    echo -e "${COLOR_YELLOW}创建 logs/.gitkeep...${NC}"
    touch logs/.gitkeep
    echo -e "${COLOR_GREEN}✓ 已创建${NC}\n"
fi

###############################################################################
# 4. 删除 .env 文件（但保留 .env.example）
###############################################################################
if [ -f ".env" ]; then
    echo -e "${COLOR_YELLOW}删除 .env 文件...${NC}"
    rm -f .env
    echo -e "${COLOR_GREEN}✓ 已删除${NC}\n"
    CLEANED=$((CLEANED + 1))
fi

###############################################################################
# 5. 删除 .pyc 相关缓存
###############################################################################
if [ -d ".pytest_cache" ]; then
    echo -e "${COLOR_YELLOW}删除 .pytest_cache 目录...${NC}"
    rm -rf .pytest_cache
    echo -e "${COLOR_GREEN}✓ 已删除${NC}\n"
    CLEANED=$((CLEANED + 1))
fi

if [ -d ".mypy_cache" ]; then
    echo -e "${COLOR_YELLOW}删除 .mypy_cache 目录...${NC}"
    rm -rf .mypy_cache
    echo -e "${COLOR_GREEN}✓ 已删除${NC}\n"
    CLEANED=$((CLEANED + 1))
fi

if [ -d ".coverage" ]; then
    echo -e "${COLOR_YELLOW}删除 .coverage 文件...${NC}"
    rm -rf .coverage
    echo -e "${COLOR_GREEN}✓ 已删除${NC}\n"
    CLEANED=$((CLEANED + 1))
fi

###############################################################################
# 6. 清理报告目录（可选）
###############################################################################
echo -e "${COLOR_YELLOW}清理 reports 目录...${NC}"
if [ -d "reports" ]; then
    # 保留示例报告，删除其他
    find reports -type f ! -name 'README.md' ! -name 'example*' -delete 2>/dev/null || true
    echo -e "${COLOR_GREEN}✓ 已清理（保留示例报告）${NC}\n"
    CLEANED=$((CLEANED + 1))
fi

###############################################################################
# 7. 清理数据缓存
###############################################################################
echo -e "${COLOR_YELLOW}清理 data 目录...${NC}"
if [ -d "data" ]; then
    find data -type f ! -name '*.py' ! -name 'README.md' -delete 2>/dev/null || true
    echo -e "${COLOR_GREEN}✓ 已清理（保留 Python 文件）${NC}\n"
    CLEANED=$((CLEANED + 1))
fi

###############################################################################
# 8. Git 相关清理（如果是 Git 仓库）
###############################################################################
if [ -d ".git" ]; then
    echo -e "${COLOR_YELLOW}清理 Git 追踪（如有）...${NC}"
    
    # 删除已追踪的 .env
    git rm --cached .env 2>/dev/null || true
    
    # 删除已追踪的虚拟环境（如有）
    git rm -r --cached venv 2>/dev/null || true
    git rm -r --cached env 2>/dev/null || true
    git rm -r --cached __pycache__ 2>/dev/null || true
    
    echo -e "${COLOR_GREEN}✓ 已完成${NC}\n"
    CLEANED=$((CLEANED + 1))
fi

###############################################################################
# 总结
###############################################################################
echo -e "${COLOR_BLUE}========================================${NC}"
echo -e "${COLOR_GREEN}清理完成！${NC}"
echo -e "${COLOR_BLUE}========================================${NC}\n"

if [ -d ".git" ]; then
    echo -e "${COLOR_YELLOW}Git 状态：${NC}"
    git status --short | head -10
    echo ""
fi

echo -e "${COLOR_YELLOW}建议下一步：${NC}"
echo "  1. 检查无误：git status"
echo "  2. 运行安全检查：bash security_check.sh"
echo "  3. 提交更改："
echo "     git add -A"
echo "     git commit -m 'chore: clean up before open source'"
echo "  4. 推送到 GitHub"
echo ""

echo -e "${COLOR_GREEN}✓ 清理脚本完成${NC}"

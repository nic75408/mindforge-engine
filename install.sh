#!/bin/bash

# 深索 (MindForge) 一键安装脚本
# 适用：OpenClaw v4.12+
# 时间：~30 秒

set -e

echo "🚀 深索 (MindForge) 安装脚本"
echo "============================"
echo ""

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 检测 OpenClaw 路径
detect_openclaw_path() {
    if [ -d "$HOME/Openclaw" ]; then
        echo "$HOME/Openclaw"
    elif [ -d "$HOME/openclaw" ]; then
        echo "$HOME/openclaw"
    elif [ -d "$HOME/.openclaw" ]; then
        echo "$HOME/.openclaw"
    else
        echo ""
    fi
}

# 检测 workspace 路径
detect_workspace_path() {
    if [ -d "$HOME/.openclaw/workspace-ruige" ]; then
        echo "$HOME/.openclaw/workspace-ruige"
    elif [ -d "$HOME/.openclaw/workspace" ]; then
        echo "$HOME/.openclaw/workspace"
    else
        echo ""
    fi
}

echo "📦 步骤 1/6: 检测环境..."
OPENCLAW_PATH=$(detect_openclaw_path)
WORKSPACE_PATH=$(detect_workspace_path)

if [ -z "$OPENCLAW_PATH" ]; then
    echo -e "${RED}❌ 未找到 OpenClaw 安装目录${NC}"
    echo "请确认已安装 OpenClaw v4.12+"
    exit 1
fi

if [ -z "$WORKSPACE_PATH" ]; then
    echo -e "${RED}❌ 未找到 workspace 目录${NC}"
    exit 1
fi

echo -e "${GREEN}✅ OpenClaw: $OPENCLAW_PATH${NC}"
echo -e "${GREEN}✅ Workspace: $WORKSPACE_PATH${NC}"
echo ""

# 创建目录结构
echo "📁 步骤 2/6: 创建目录结构..."
mkdir -p "$WORKSPACE_PATH/skills/mindforge-core"
mkdir -p "$WORKSPACE_PATH/memory/thinking-traces"
mkdir -p "$WORKSPACE_PATH/scripts"

echo -e "${GREEN}✅ 目录创建完成${NC}"
echo ""

# 复制核心文件
echo "📋 步骤 3/6: 复制核心文件..."
cp "$(dirname "$0")/openclaw/SKILL.md" "$WORKSPACE_PATH/skills/mindforge-core/SKILL.md"
cp "$(dirname "$0")/scripts/"*.py "$WORKSPACE_PATH/scripts/" 2>/dev/null || true

echo -e "${GREEN}✅ 文件复制完成${NC}"
echo ""

# 备份配置
echo "💾 步骤 4/6: 备份当前配置..."
BACKUP_DIR="$HOME/.openclaw/backups"
mkdir -p "$BACKUP_DIR"
BACKUP_FILE="$BACKUP_DIR/openclaw-$(date +%Y%m%d-%H%M%S).json"

if [ -f "$HOME/.openclaw/openclaw.json" ]; then
    cp "$HOME/.openclaw/openclaw.json" "$BACKUP_FILE"
    echo -e "${GREEN}✅ 配置已备份：$BACKUP_FILE${NC}"
else
    echo -e "${YELLOW}⚠️  未找到 openclaw.json，跳过备份${NC}"
fi
echo ""

# 修改配置（注入 heartbeat）
echo "⚙️  步骤 5/6: 注入配置..."
CONFIG_FILE="$HOME/.openclaw/openclaw.json"

if [ -f "$CONFIG_FILE" ]; then
    # 检查是否已存在 heartbeat 配置
    if grep -q '"heartbeat"' "$CONFIG_FILE"; then
        echo -e "${YELLOW}⚠️  已存在 heartbeat 配置，跳过注入${NC}"
    else
        # 使用 Python 安全地修改 JSON
        python3 << EOF
import json

with open('$CONFIG_FILE', 'r') as f:
    config = json.load(f)

config['heartbeat'] = {
    'enabled': True,
    'intervalMinutes': 30,
    'prompt': '检查今日 Trace 写入状态，统计 PASSED 率，告警异常',
    'model': 'qwen3.5-plus'
}

with open('$CONFIG_FILE', 'w') as f:
    json.dump(config, f, indent=2)
EOF
        echo -e "${GREEN}✅ 配置注入完成${NC}"
    fi
else
    echo -e "${RED}❌ 未找到 openclaw.json，请手动配置${NC}"
    exit 1
fi
echo ""

# 验证安装
echo "🧪 步骤 6/6: 验证安装..."

# 检查文件是否存在
if [ -f "$WORKSPACE_PATH/skills/mindforge-core/SKILL.md" ]; then
    echo -e "${GREEN}✅ SKILL.md 存在${NC}"
else
    echo -e "${RED}❌ SKILL.md 不存在${NC}"
    exit 1
fi

# 检查目录是否存在
if [ -d "$WORKSPACE_PATH/memory/thinking-traces" ]; then
    echo -e "${GREEN}✅ Trace 目录存在${NC}"
else
    echo -e "${RED}❌ Trace 目录不存在${NC}"
    exit 1
fi

# 测试 Trace 写入
echo ""
echo "📝 测试 Trace 写入..."
python3 "$WORKSPACE_PATH/scripts/record-trace-auto.py" mindforge "安装测试" "安装成功" '{}' "PASSED" "manual" "安装验证 DA" 2>/dev/null || {
    echo -e "${YELLOW}⚠️  Trace 写入测试失败（可手动修复）${NC}"
}

TRACE_FILE="$WORKSPACE_PATH/memory/thinking-traces/$(date +%Y-%m-%d).jsonl"
if [ -f "$TRACE_FILE" ]; then
    echo -e "${GREEN}✅ Trace 文件已创建${NC}"
else
    echo -e "${YELLOW}⚠️  Trace 文件未创建（可手动创建）${NC}"
fi

echo ""
echo "============================"
echo -e "${GREEN}✅ 安装完成！${NC}"
echo ""
echo "📌 下一步："
echo "   1. 重启 Gateway: openclaw gateway restart"
echo "   2. 验证 Trace 写入：cat $TRACE_FILE"
echo "   3. 开始使用深索！"
echo ""
echo "💡 提示：如遇问题，查看文档 docs/quickstart.md"
echo ""

#!/bin/bash

# 深索 (MindForge) 一键卸载脚本
# 适用：OpenClaw v4.12+
# 时间：~10 秒

set -e

echo "🗑️  深索 (MindForge) 卸载脚本"
echo "============================"
echo ""

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

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

WORKSPACE_PATH=$(detect_workspace_path)

if [ -z "$WORKSPACE_PATH" ]; then
    echo -e "${RED}❌ 未找到 workspace 目录${NC}"
    exit 1
fi

echo "📁 Workspace: $WORKSPACE_PATH"
echo ""

# 确认卸载
echo -n "⚠️  确认卸载深索？(y/N): "
read -r CONFIRM
if [[ ! $CONFIRM =~ ^[Yy]$ ]]; then
    echo "❌ 取消卸载"
    exit 0
fi
echo ""

# 删除技能文件
echo "📁 步骤 1/4: 删除技能文件..."
if [ -d "$WORKSPACE_PATH/skills/mindforge-core" ]; then
    rm -rf "$WORKSPACE_PATH/skills/mindforge-core"
    echo -e "${GREEN}✅ 已删除 skills/mindforge-core${NC}"
else
    echo -e "${YELLOW}⚠️  skills/mindforge-core 不存在${NC}"
fi
echo ""

# 删除脚本文件
echo "📁 步骤 2/4: 删除脚本文件..."
rm -f "$WORKSPACE_PATH/scripts/trace-writer.py"
rm -f "$WORKSPACE_PATH/scripts/passed-rate-stats.py"
rm -f "$WORKSPACE_PATH/scripts/engine-health.py"
rm -f "$WORKSPACE_PATH/scripts/review-traces.py"
rm -f "$WORKSPACE_PATH/scripts/record-trace-auto.py"
rm -f "$WORKSPACE_PATH/scripts/ruige-auto-entry.py"
echo -e "${GREEN}✅ 已删除脚本文件${NC}"
echo ""

# 恢复配置（删除 heartbeat）
echo "⚙️  步骤 3/4: 恢复配置..."
CONFIG_FILE="$HOME/.openclaw/openclaw.json"

if [ -f "$CONFIG_FILE" ]; then
    # 使用 Python 安全地修改 JSON
    python3 << EOF
import json

with open('$CONFIG_FILE', 'r') as f:
    config = json.load(f)

if 'heartbeat' in config:
    del config['heartbeat']
    with open('$CONFIG_FILE', 'w') as f:
        json.dump(config, f, indent=2)
    print("✅ 已删除 heartbeat 配置")
else:
    print("ℹ️  heartbeat 配置不存在，跳过")
EOF
else
    echo -e "${RED}❌ 未找到 openclaw.json${NC}"
fi
echo ""

# 保留 Trace 数据（询问用户）
echo "📊 步骤 4/4: 处理 Trace 数据..."
TRACE_DIR="$WORKSPACE_PATH/memory/thinking-traces"

if [ -d "$TRACE_DIR" ]; then
    echo -n "ℹ️  是否保留 Trace 数据？(y/N): "
    read -r KEEP_TRACE
    if [[ $KEEP_TRACE =~ ^[Yy]$ ]]; then
        echo -e "${GREEN}✅ 保留 Trace 数据${NC}"
    else
        rm -rf "$TRACE_DIR"
        echo -e "${GREEN}✅ 已删除 Trace 数据${NC}"
    fi
else
    echo -e "${YELLOW}⚠️  Trace 目录不存在${NC}"
fi

echo ""
echo "============================"
echo -e "${GREEN}✅ 卸载完成！${NC}"
echo ""
echo "📌 下一步："
echo "   1. 重启 Gateway: openclaw gateway restart"
echo "   2. 验证卸载：检查配置是否恢复"
echo ""
echo "💡 提示：如需重新安装，运行 ./install.sh"
echo ""

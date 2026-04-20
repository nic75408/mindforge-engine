#!/usr/bin/env python3
"""
深索对话 Trace 自动写入工具

用法:
    python3 ruige-auto-entry.py "<user_msg>" "<reply>" <agent> <status> <da>

示例:
    python3 ruige-auto-entry.py "用户问题" "Agent 回复" mindforge "PASSED" "决策依据内容"
"""

import json
import sys
import os
from datetime import datetime
from pathlib import Path

def main():
    if len(sys.argv) != 6:
        print("❌ 参数错误")
        print("用法：python3 ruige-auto-entry.py <user_msg> <reply> <agent> <status> <da>")
        sys.exit(1)
    
    user_msg = sys.argv[1]
    reply = sys.argv[2]
    agent = sys.argv[3]
    status = sys.argv[4]
    da = sys.argv[5]
    
    # 获取 workspace 路径
    workspace = Path(os.environ.get('OPENCLAW_WORKSPACE', Path.home() / '.openclaw' / 'workspace-ruige'))
    trace_dir = workspace / 'memory' / 'thinking-traces'
    trace_dir.mkdir(parents=True, exist_ok=True)
    
    # 生成 Trace 文件名
    today = datetime.now().strftime('%Y-%m-%d')
    trace_file = trace_dir / f'{today}.jsonl'
    
    # 构建 Trace 记录
    trace = {
        'timestamp': datetime.now().astimezone().isoformat(),
        'agent': agent,
        'user_msg': user_msg[:200],
        'reply': reply[:500],
        'metrics': {
            'root_cause': {'passed': status == 'PASSED'},
            'essence': {'missing': False},
            'da_quality': 'high' if len(da) >= 50 else 'low',
            'relevance': 1.0,
            'consistency': True
        },
        'engine_status': status,
        'source': 'chat',
        'da': da
    }
    
    # 写入 Trace 文件
    with open(trace_file, 'a', encoding='utf-8') as f:
        f.write(json.dumps(trace, ensure_ascii=False) + '\n')
    
    print(f"✅ Trace 已写入：{trace_file}")

if __name__ == '__main__':
    main()

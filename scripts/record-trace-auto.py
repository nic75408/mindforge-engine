#!/usr/bin/env python3
"""
深索 Trace 自动记录工具

用法:
    python3 record-trace-auto.py <agent> <user_message> <reply> <check_result_json> <engine_status> <source> <da_content>

示例:
    python3 record-trace-auto.py mindforge "用户问题" "Agent 回复" '{}' "PASSED" "cron" "决策依据内容"
"""

import json
import sys
import os
from datetime import datetime
from pathlib import Path

def main():
    if len(sys.argv) != 8:
        print("❌ 参数错误")
        print("用法：python3 record-trace-auto.py <agent> <user_message> <reply> <check_result_json> <engine_status> <source> <da_content>")
        sys.exit(1)
    
    agent = sys.argv[1]
    user_message = sys.argv[2]
    reply = sys.argv[3]
    check_result_json = sys.argv[4]
    engine_status = sys.argv[5]
    source = sys.argv[6]
    da_content = sys.argv[7]
    
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
        'user_msg': user_message[:200],  # 限制长度
        'reply': reply[:500],
        'metrics': json.loads(check_result_json) if check_result_json != '{}' else {},
        'engine_status': engine_status,
        'source': source,
        'da': da_content
    }
    
    # 写入 Trace 文件
    with open(trace_file, 'a', encoding='utf-8') as f:
        f.write(json.dumps(trace, ensure_ascii=False) + '\n')
    
    print(f"✅ Trace 已写入：{trace_file}")

if __name__ == '__main__':
    main()

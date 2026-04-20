#!/usr/bin/env python3
"""
深索通用 Trace 写入工具

用法:
    python3 trace-writer.py <agent> <user_message> <reply> <metrics_json> <engine_status> <source> <da> [hypotheses] [sources]

示例:
    python3 trace-writer.py mindforge "用户问题" "Agent 回复" '{"root_cause":{"passed":true}}' "PASSED" "chat" "决策依据" '["H1200-v3"]' '["theneuralbase"]'
"""

import json
import sys
import os
from datetime import datetime
from pathlib import Path

def main():
    if len(sys.argv) < 8:
        print("❌ 参数错误")
        print("用法：python3 trace-writer.py <agent> <user_message> <reply> <metrics_json> <engine_status> <source> <da> [hypotheses] [sources]")
        sys.exit(1)
    
    agent = sys.argv[1]
    user_message = sys.argv[2]
    reply = sys.argv[3]
    metrics_json = sys.argv[4]
    engine_status = sys.argv[5]
    source = sys.argv[6]
    da = sys.argv[7]
    hypotheses = json.loads(sys.argv[8]) if len(sys.argv) > 8 and sys.argv[8] != '[]' else []
    sources = json.loads(sys.argv[9]) if len(sys.argv) > 9 and sys.argv[9] != '[]' else []
    
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
        'user_msg': user_message[:200],
        'reply': reply[:500],
        'metrics': json.loads(metrics_json),
        'engine_status': engine_status,
        'source': source,
        'da': da,
        'hypotheses': hypotheses,
        'sources': sources
    }
    
    # 写入 Trace 文件
    with open(trace_file, 'a', encoding='utf-8') as f:
        f.write(json.dumps(trace, ensure_ascii=False) + '\n')
    
    print(f"✅ Trace 已写入：{trace_file}")

if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""
深索 Trace 回顾分析工具

用法:
    python3 review-traces.py [日期] [N]

示例:
    python3 review-traces.py              # 回顾今日所有 FAILED
    python3 review-traces.py 2026-04-20   # 回顾指定日期
    python3 review-traces.py 2026-04-20 10  # 回顾最近 10 条
"""

import json
import sys
import os
from datetime import datetime
from pathlib import Path

def main():
    # 获取参数
    if len(sys.argv) > 1:
        date = sys.argv[1]
    else:
        date = datetime.now().strftime('%Y-%m-%d')
    
    limit = int(sys.argv[2]) if len(sys.argv) > 2 else None
    
    # 获取 workspace 路径
    workspace = Path(os.environ.get('OPENCLAW_WORKSPACE', Path.home() / '.openclaw' / 'workspace-ruige'))
    trace_file = workspace / 'memory' / 'thinking-traces' / f'{date}.jsonl'
    
    if not trace_file.exists():
        print(f"❌ Trace 文件不存在：{trace_file}")
        sys.exit(1)
    
    # 读取 Trace 数据
    traces = []
    with open(trace_file, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                traces.append(json.loads(line))
    
    if not traces:
        print(f"⚠️  {date} 无 Trace 数据")
        sys.exit(0)
    
    # 筛选 FAILED 和 PARTIAL
    failed_traces = [t for t in traces if t['engine_status'] in ('FAILED', 'PARTIAL')]
    
    if limit:
        failed_traces = failed_traces[-limit:]
    
    if not failed_traces:
        print(f"✅ {date} 无 FAILED/PARTIAL Trace")
        sys.exit(0)
    
    # 输出分析报告
    print(f"🔍 深索 Trace 回顾分析 - {date}")
    print("=" * 50)
    print(f"总 Trace 数：{len(traces)}")
    print(f"FAILED/PARTIAL 数：{len(failed_traces)}")
    print()
    
    # 分析失败模式
    failure_patterns = {}
    for trace in failed_traces:
        status = trace['engine_status']
        da = trace.get('da', '')
        
        # 分类失败原因
        if len(da) < 50:
            pattern = "H258: DA 长度不足 (<50 字符)"
        elif status == 'PARTIAL':
            pattern = "根因分析不完整 (PARTIAL)"
        else:
            pattern = "其他失败原因"
        
        failure_patterns[pattern] = failure_patterns.get(pattern, 0) + 1
    
    print("失败模式分布:")
    for pattern, count in sorted(failure_patterns.items(), key=lambda x: -x[1]):
        print(f"  • {pattern}: {count} ({count/len(failed_traces)*100:.1f}%)")
    print()
    
    # 输出最近失败案例
    print("最近失败案例:")
    for i, trace in enumerate(failed_traces[-5:], 1):
        print(f"\n{i}. [{trace['engine_status']}] {trace['user_msg'][:50]}...")
        print(f"   DA: {trace.get('da', 'N/A')[:80]}")
        print(f"   时间：{trace['timestamp']}")

if __name__ == '__main__':
    main()

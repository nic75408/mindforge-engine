#!/usr/bin/env python3
"""
深索 PASSED 率统计工具

用法:
    python3 passed-rate-stats.py [日期]

示例:
    python3 passed-rate-stats.py        # 统计今日
    python3 passed-rate-stats.py 2026-04-20  # 统计指定日期
"""

import json
import sys
import os
from datetime import datetime
from pathlib import Path
from collections import Counter

def main():
    # 获取日期
    if len(sys.argv) > 1:
        date = sys.argv[1]
    else:
        date = datetime.now().strftime('%Y-%m-%d')
    
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
    
    # 统计 PASSED 率
    status_counter = Counter(t['engine_status'] for t in traces)
    total = len(traces)
    passed = status_counter.get('PASSED', 0)
    partial = status_counter.get('PARTIAL', 0)
    failed = status_counter.get('FAILED', 0)
    
    passed_rate = (passed / total * 100) if total > 0 else 0
    
    # 统计 DA 质量
    da_quality_counter = Counter(t['metrics'].get('da_quality', 'unknown') for t in traces)
    
    # 统计 H258 拦截
    h258_intercepted = sum(1 for t in traces if len(t.get('da', '')) < 50)
    
    # 输出报告
    print(f"📊 深索 PASSED 率统计 - {date}")
    print("=" * 50)
    print(f"总 Trace 数：{total}")
    print(f"PASSED: {passed} ({passed_rate:.1f}%)")
    print(f"PARTIAL: {partial} ({partial/total*100:.1f}%)")
    print(f"FAILED: {failed} ({failed/total*100:.1f}%)")
    print()
    print("DA 质量分布:")
    for quality, count in da_quality_counter.items():
        print(f"  {quality}: {count} ({count/total*100:.1f}%)")
    print()
    print(f"H258 拦截数：{h258_intercepted} ({h258_intercepted/total*100:.1f}%)")
    print()
    
    # 质量评估
    if passed_rate >= 80:
        print("✅ 质量优秀（≥80%）")
    elif passed_rate >= 75:
        print("✅ 质量合格（≥75%）")
    elif passed_rate >= 50:
        print("⚠️  质量待改进（50-75%）")
    else:
        print("❌ 质量危险（<50%）")

if __name__ == '__main__':
    main()

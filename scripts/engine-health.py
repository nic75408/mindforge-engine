#!/usr/bin/env python3
"""
深索引擎健康检查工具

用法:
    python3 engine-health.py

检查项:
- Trace 文件是否存在
- 今日 Trace 数量
- PASSED 率
- H258 拦截率
- 心跳状态
"""

import json
import os
from datetime import datetime
from pathlib import Path
from collections import Counter

def check_trace_file():
    """检查 Trace 文件"""
    workspace = Path(os.environ.get('OPENCLAW_WORKSPACE', Path.home() / '.openclaw' / 'workspace-ruige'))
    trace_dir = workspace / 'memory' / 'thinking-traces'
    today = datetime.now().strftime('%Y-%m-%d')
    trace_file = trace_dir / f'{today}.jsonl'
    
    if not trace_file.exists():
        return False, f"Trace 文件不存在：{trace_file}"
    
    return True, f"Trace 文件存在：{trace_file}"

def check_trace_count():
    """检查今日 Trace 数量"""
    workspace = Path(os.environ.get('OPENCLAW_WORKSPACE', Path.home() / '.openclaw' / 'workspace-ruige'))
    trace_file = workspace / 'memory' / 'thinking-traces' / f'{datetime.now().strftime("%Y-%m-%d")}.jsonl'
    
    if not trace_file.exists():
        return 0
    
    count = 0
    with open(trace_file, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                count += 1
    
    return count

def check_passed_rate():
    """检查 PASSED 率"""
    workspace = Path(os.environ.get('OPENCLAW_WORKSPACE', Path.home() / '.openclaw' / 'workspace-ruige'))
    trace_file = workspace / 'memory' / 'thinking-traces' / f'{datetime.now().strftime("%Y-%m-%d")}.jsonl'
    
    if not trace_file.exists():
        return None, None
    
    traces = []
    with open(trace_file, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                traces.append(json.loads(line))
    
    if not traces:
        return None, None
    
    status_counter = Counter(t['engine_status'] for t in traces)
    total = len(traces)
    passed = status_counter.get('PASSED', 0)
    passed_rate = (passed / total * 100) if total > 0 else 0
    
    return passed_rate, total

def check_h258_interception():
    """检查 H258 拦截率"""
    workspace = Path(os.environ.get('OPENCLAW_WORKSPACE', Path.home() / '.openclaw' / 'workspace-ruige'))
    trace_file = workspace / 'memory' / 'thinking-traces' / f'{datetime.now().strftime("%Y-%m-%d")}.jsonl'
    
    if not trace_file.exists():
        return None, None
    
    traces = []
    with open(trace_file, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                traces.append(json.loads(line))
    
    if not traces:
        return None, None
    
    intercepted = sum(1 for t in traces if len(t.get('da', '')) < 50)
    total = len(traces)
    interception_rate = (intercepted / total * 100) if total > 0 else 0
    
    return interception_rate, total

def main():
    print("🏥 深索引擎健康检查")
    print("=" * 50)
    print()
    
    # 检查 Trace 文件
    ok, msg = check_trace_file()
    if ok:
        print(f"✅ {msg}")
    else:
        print(f"❌ {msg}")
    
    # 检查 Trace 数量
    count = check_trace_count()
    if count >= 10:
        print(f"✅ 今日 Trace 数：{count} (≥10)")
    elif count > 0:
        print(f"⚠️  今日 Trace 数：{count} (<10)")
    else:
        print(f"❌ 今日 Trace 数：0")
    
    # 检查 PASSED 率
    passed_rate, total = check_passed_rate()
    if passed_rate is not None:
        if passed_rate >= 80:
            print(f"✅ PASSED 率：{passed_rate:.1f}% (≥80%)")
        elif passed_rate >= 75:
            print(f"✅ PASSED 率：{passed_rate:.1f}% (≥75%)")
        elif passed_rate >= 50:
            print(f"⚠️  PASSED 率：{passed_rate:.1f}% (50-75%)")
        else:
            print(f"❌ PASSED 率：{passed_rate:.1f}% (<50%)")
    else:
        print("⚠️  无 PASSED 率数据")
    
    # 检查 H258 拦截
    interception_rate, total = check_h258_interception()
    if interception_rate is not None:
        if interception_rate < 20:
            print(f"✅ H258 拦截率：{interception_rate:.1f}% (<20%)")
        elif interception_rate < 50:
            print(f"⚠️  H258 拦截率：{interception_rate:.1f}% (20-50%)")
        else:
            print(f"❌ H258 拦截率：{interception_rate:.1f}% (≥50%)")
    else:
        print("⚠️  无 H258 拦截数据")
    
    print()
    print("=" * 50)
    
    # 总体评估
    if count >= 10 and passed_rate is not None and passed_rate >= 75:
        print("🎉 引擎状态：健康")
    elif count > 0:
        print("⚠️  引擎状态：部分健康")
    else:
        print("❌ 引擎状态：异常")

if __name__ == '__main__':
    main()

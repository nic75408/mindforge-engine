# 深索 Trace 格式详解

> thinking-traces JSONL 格式规范

---

## 📁 文件位置

```
memory/thinking-traces/YYYY-MM-DD.jsonl
```

**说明**：
- 每天一个文件
- JSONL 格式（每行一个 JSON 对象）
- UTF-8 编码

---

## 📋 单行格式

```jsonl
{
  "timestamp": "2026-04-20T13:36:00+08:00",
  "agent": "mindforge",
  "user_msg": "用户问题摘要（≤200 字符）",
  "reply": "Agent 回复摘要（≤500 字符）",
  "metrics": {
    "root_cause": {
      "passed": true,
      "reason": "分析了根因并使用强制格式"
    },
    "essence": {
      "missing": false
    },
    "da_quality": "high",
    "relevance": 1.0,
    "consistency": true
  },
  "engine_status": "PASSED",
  "hypotheses": ["H1200-v3", "H1049-v3"],
  "sources": ["theneuralbase 2026-04", "Elasticsearch Reference"],
  "da": "决策依据内容（≥50 字符，包含条件与后果绑定）"
}
```

---

## 🔍 字段说明

### 必填字段

| 字段 | 类型 | 说明 | 示例 |
|------|------|------|------|
| `timestamp` | string | ISO 8601 格式（带时区） | `"2026-04-20T13:36:00+08:00"` |
| `agent` | string | Agent 标识 | `"mindforge"` |
| `user_msg` | string | 用户问题（≤200 字符） | `"这个功能为什么不能用？"` |
| `reply` | string | Agent 回复（≤500 字符） | `"根因=[因为 A 导致 B]..."` |
| `metrics.root_cause.passed` | boolean | 是否分析根因 | `true` |
| `metrics.essence.missing` | boolean | 是否缺失核心内容 | `false` |
| `metrics.da_quality` | string | DA 质量 | `"high"` / `"medium"` / `"low"` |
| `metrics.relevance` | number | 相关性评分 | `1.0` (0-1) |
| `metrics.consistency` | boolean | 是否自相矛盾 | `true` |
| `engine_status` | string | 引擎状态 | `"PASSED"` / `"PARTIAL"` / `"FAILED"` |
| `da` | string | 决策依据（≥50 字符） | `"如果 check_result 未完整捕获指标则失效..."` |

### 可选字段

| 字段 | 类型 | 说明 | 示例 |
|------|------|------|------|
| `hypotheses` | array | 验证的假设列表 | `["H1200-v3", "H1049-v3"]` |
| `sources` | array | 验证来源 | `["theneuralbase 2026-04"]` |

---

## 📊 质量判定

### PASSED 判定

```python
PASSED = (
    root_cause.passed == True AND
    essence.missing == False AND
    da_quality == "high" AND
    len(da) >= 50 AND
    relevance >= 0.8 AND
    consistency == True
)
```

### PARTIAL 判定

```python
PARTIAL = (
    (root_cause.passed == True OR essence.missing == False) AND
    NOT PASSED
)
```

### FAILED 判定

```python
FAILED = NOT PASSED AND NOT PARTIAL
```

### H258 拦截机制

```python
# DA<50 字符自动标记 FAILED
if len(da) < 50:
    engine_status = "FAILED"
    da_quality = "low"
```

### H608-R2 强制绑定

```python
# root_cause passed=false → engine_status 不能为 PASSED
if root_cause.passed == False:
    if engine_status == "PASSED":
        engine_status = "PARTIAL"  # 自动降级
```

---

## 📝 写入示例

### Chat 回复

```bash
python3 scripts/ruige-auto-entry.py \
  "用户问题摘要" \
  "Agent 回复摘要" \
  mindforge \
  "PASSED" \
  "决策依据内容（≥50 字符）"
```

### Cron/Heartbeat

```bash
python3 scripts/record-trace-auto.py \
  mindforge \
  "定时检查" \
  "检查今日 Trace 写入状态" \
  '{}' \
  "PASSED" \
  "cron" \
  "决策依据内容（≥50 字符）"
```

---

## 🔧 工具使用

### 统计 PASSED 率

```bash
python3 scripts/passed-rate-stats.py [日期]
```

### 回顾失败 Trace

```bash
python3 scripts/review-traces.py [日期] [N]
```

### 引擎健康检查

```bash
python3 scripts/engine-health.py
```

---

## 📈 数据分析

### 查询今日 Trace 数量

```bash
wc -l memory/thinking-traces/$(date +%Y-%m-%d).jsonl
```

### 统计 PASSED 率

```bash
python3 -c "
import json
from collections import Counter
traces = [json.loads(l) for l in open('memory/thinking-traces/2026-04-20.jsonl')]
status = Counter(t['engine_status'] for t in traces)
print(f'PASSED: {status[\"PASSED\"]}/{len(traces)} ({status[\"PASSED\"]/len(traces)*100:.1f}%)')
"
```

### 分析失败模式

```bash
python3 scripts/review-traces.py 2026-04-20
```

---

## ⚠️ 注意事项

1. **字符限制**：
   - `user_msg` ≤200 字符
   - `reply` ≤500 字符
   - `da` ≥50 字符

2. **时间格式**：
   - 必须带时区（`+08:00`）
   - 使用 `datetime.now().astimezone().isoformat()`

3. **编码**：
   - UTF-8
   - `ensure_ascii=False`（保留中文）

4. **原子写入**：
   - 使用 `a` 模式追加
   - 每行一个完整 JSON 对象

---

## 📚 参考

- [架构说明](architecture.md)
- [最佳实践](best-practices.md)
- [快速开始](quickstart.md)

---

**最后更新：2026-04-20**

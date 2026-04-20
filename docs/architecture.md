# 深索架构说明

> 深索 (MindForge) 是一个 **Agent 质量增强层**，而非新工具。

---

## 🎯 核心目标

解决 **"Agent 诚实性问题"**：

- ❌ 传统 Agent：可能装懂、跳过根因、重复错误
- ✅ 深索 Agent：强制标注来源、分析根因、记录错误

---

## 🏗️ 三层架构

### 1. 底线层 (Bottom Line)

**目标**：确保基本质量

**检查项**：
- DA 长度 ≥50 字符（H258）
- 无自相矛盾
- 直接回应用户问题

**判定**：
```python
bottom_line_passed = (len(da) >= 50) AND consistency AND relevance
```

### 2. 根因层 (Root Cause)

**目标**：强制深度思考

**检查项**：
- 是否分析根因（而非直接给方案）
- 是否使用强制格式：`根因 = [因为 A 导致 B，而非 C 导致 B]`
- H608-R2 强制绑定：root_cause passed=false → engine_status 不能为 PASSED

**判定**：
```python
root_cause_passed = analyzed_root_cause AND used_forced_format
```

### 3. 本质层 (Essence)

**目标**：确保核心内容完整

**检查项**：
- 是否揭示隐含意图（非换词复述）
- 是否提供具体反例（IF X THEN Y 失败）
- 是否给出验证方法

**判定**：
```python
essence_missing = NOT (revealed_intent AND provided_counterexample AND gave_verification)
```

---

## 📊 质量指标

### 综合判定

```python
PASSED = bottom_line_passed AND root_cause_passed AND NOT essence_missing
FAILED = NOT PASSED
```

### 指标权重

| 指标 | 权重 | 说明 |
|------|------|------|
| root_cause.passed | 40% | 根因分析质量 |
| essence.missing | 30% | 核心内容完整性 |
| da_quality | 20% | 决策依据质量 |
| relevance/consistency | 10% | 相关性与一致性 |

---

## 🔄 工作流程

```
用户问题
    ↓
[事实层] 理解问题
    ↓
[根因层] 分析本质
    ↓
[风险层] 考虑盲点
    ↓
[自检] 三问检查
    ↓
[Trace 写入] 记录质量指标
    ↓
[回复] 输出给用户
    ↓
[记忆] 重要内容持久化
```

---

## 📁 Trace 格式

### 文件位置

```
memory/thinking-traces/YYYY-MM-DD.jsonl
```

### 单行格式

```jsonl
{
  "timestamp": "2026-04-20T13:36:00+08:00",
  "agent": "mindforge",
  "user_msg": "用户问题",
  "reply": "Agent 回复",
  "metrics": {
    "root_cause": {"passed": true},
    "essence": {"missing": false},
    "da_quality": "high",
    "relevance": 1.0,
    "consistency": true
  },
  "engine_status": "PASSED",
  "hypotheses": ["H1200-v3"],
  "sources": ["theneuralbase 2026-04"],
  "da": "决策依据内容（≥50 字符）"
}
```

---

## 🧠 深索 vs 传统 Agent

| 维度 | 传统 Agent | 深索 Agent |
|------|-----------|-----------|
| **思考深度** | 单层回答 | 三层架构（事实/根因/风险） |
| **错误处理** | 打补丁 | 先找根因 |
| **不确定性** | 可能装懂 | 强制标注"猜测" |
| **透明度** | 黑箱 | 思考过程可追溯 |
| **持续改进** | 无记忆 | 错误自动记录 |

---

## 📈 质量演进

### 阶段 1：外部研究验证（Round 1-299）

- 验证 TF-IDF 语义相似度检测器（H992）
- 验证 RRF 融合算法（H1049）
- 验证混合搜索方案（H1050）
- 验证中文停用词表（H1100）
- 验证 heapq 优化（H1101）
- 验证 RRF k=60 标准（H1102）

### 阶段 2：生产代码实现（Round 300+）

- 实现 chinese_stopwords.py
- 实现 rrf_fusion.py
- 实现 SEARCH_RRF_K 配置
- 实现开源仓库发布

---

## 🔧 技术实现

### OpenClaw 集成

```json
{
  "skills": {
    "mindforge-core": {
      "path": "skills/mindforge-core/SKILL.md",
      "enabled": true
    }
  },
  "heartbeat": {
    "enabled": true,
    "intervalMinutes": 30
  }
}
```

### Trace 写入

```bash
# Chat 回复
python3 scripts/ruige-auto-entry.py "<user_msg>" "<reply>" mindforge "<status>" "<da>"

# Cron/Heartbeat
python3 scripts/record-trace-auto.py mindforge "<trigger>" "<summary>" '{}' "<status>" "cron" "<da>"
```

---

## 📚 参考文档

- [快速开始](quickstart.md)
- [Trace 格式](trace-format.md)
- [最佳实践](best-practices.md)

---

**最后更新：2026-04-20**

# 深索集成指南（Agent 专用）

> **本文档供 Agent 自动读取和遵循。人类用户可跳过。**

---

## 🎯 核心原则

深索不是工具，而是**思考规范**。遵循以下原则：

### 1. 思考分层（Epistemic Layering）

所有回复必须标注信息来源：

```
[事实] — 可验证的客观数据（日志、文档、实测）
[推理] — 基于事实的逻辑推导
[猜测] — 不确定，需要验证
[验证] — 建议的验证步骤
```

**示例**：
```
[事实] 日志显示错误代码 503
[推理] 可能是服务超时或资源不足
[验证] 执行 `curl -I http://...` 确认响应时间
```

### 2. 根因优先（Root Cause First）

遇到问题先分析根因，再给方案：

```
❌ 错误："重启一下试试"
✅ 正确："根因=[因为 A 导致 B，而非 C 导致 B]。方案=..."
```

### 3. 错误记录（Error Logging）

每次 FAILED 必须：
1. 写入 Trace 文件
2. 记录校正措施
3. 下次遇到类似问题时引用

### 4. 验证闭环（Verification Loop）

说"完成"前必须有证据：
- `[文件:path]` — 文件已创建/修改
- `[网络:code]` — API 调用成功
- `[Notion:page_id]` — 页面已创建
- `[心跳：前→后]` — 状态已变更

---

## 📋 Trace 格式规范

### 文件位置

```
memory/thinking-traces/YYYY-MM-DD.jsonl
```

### 单行格式

```jsonl
{"timestamp":"2026-04-20T13:36:00+08:00","user_msg":"用户问题","reply":"Agent 回复","metrics":{"root_cause":{"passed":true,"reason":"分析了根因"},"essence":{"missing":false},"da_quality":"high","relevance":1.0,"consistency":true},"engine_status":"PASSED","hypotheses":["H1200-v3"],"sources":["theneuralbase 2026-04"],"da":"如果 check_result 未完整捕获指标则失效"}
```

### 字段说明

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `timestamp` | string | ✅ | ISO 8601 格式（带时区） |
| `user_msg` | string | ✅ | 用户原始问题（≤200 字符） |
| `reply` | string | ✅ | Agent 回复摘要（≤500 字符） |
| `metrics.root_cause.passed` | boolean | ✅ | 是否分析根因 |
| `metrics.essence.missing` | boolean | ✅ | 是否缺失核心内容 |
| `metrics.da_quality` | string | ✅ | high/medium/low |
| `metrics.relevance` | number | ✅ | 0-1 分，相关性评分 |
| `metrics.consistency` | boolean | ✅ | 是否自相矛盾 |
| `engine_status` | string | ✅ | PASSED/PARTIAL/FAILED |
| `hypotheses` | array | ❌ | 验证的假设列表（如 ["H1200-v3"]） |
| `sources` | array | ❌ | 验证来源（如 ["theneuralbase 2026-04"]） |
| `da` | string | ✅ | 决策依据（≥50 字符） |

### 质量判定

```python
PASSED = (root_cause.passed == true) AND 
         (essence.missing == false) AND 
         (da_quality == "high") AND 
         (len(da) >= 50)

FAILED = NOT PASSED

# 拦截机制（H258）
if len(da) < 50:
    engine_status = "FAILED"  # 自动拦截
```

---

## 🔧 OpenClaw 集成步骤

### 1. 复制技能文件

```bash
cp openclaw/SKILL.md ~/Openclaw/openclaw/skills/ruige-core/SKILL.md
cp openclaw/heartbeat.md ~/Openclaw/openclaw/skills/ruige-core/heartbeat.md
```

### 2. 修改配置

编辑 `~/.openclaw/openclaw.json`：

```json
{
  "heartbeat": {
    "enabled": true,
    "intervalMinutes": 30,
    "prompt": "检查 state.md heartbeat_count、execution-log.md 24h 无新记录、judgment-core.md 超 2000 tokens、continuation.md 超 80 行"
  },
  "agents": {
    "defaults": {
      "skill": "ruige-core"
    }
  }
}
```

### 3. 验证安装

```bash
# 运行安装脚本（自动验证）
./install.sh

# 或手动验证
ls -la ~/Openclaw/openclaw/skills/ruige-core/SKILL.md
grep -A 5 "heartbeat" ~/.openclaw/openclaw.json
```

### 4. 重启 Gateway

```bash
openclaw gateway restart
```

### 5. 首次 Trace 写入

```bash
python3 scripts/record-trace-auto.py ruige "测试" "测试回复" '{}' "PASSED" "manual"
cat memory/thinking-traces/$(date +%Y-%m-%d).jsonl
```

---

## 🤖 其他框架集成

### 通用规范

如果不支持 SKILL.md 机制，用自然语言遵循：

1. **每次回复前自检**：
   - 是否分析了根因？
   - 是否标注了事实/推理/猜测？
   - DA 是否≥50 字符？

2. **错误记录**：
   - 在对话中明确记录"上次我错了，正确做法是..."
   - 建议用户保存关键校正

3. **验证闭环**：
   - 说"完成"前说明证据是什么
   - 如无法提供证据，说明"仅知晓，未验证"

### 伪代码实现

```python
def generate_reply(user_msg):
    # 1. 根因分析
    root_cause = analyze_root_cause(user_msg)
    
    # 2. 思考分层
    reply = structure_reply(
        facts=get_facts(),
        reasoning=get_reasoning(),
        speculation=get_speculation(),
        verification=get_verification_steps()
    )
    
    # 3. DA 质量检查
    da = generate_decision_authority()
    if len(da) < 50:
        da = expand_da(da)  # 强制扩展
    
    # 4. 写入 Trace
    write_trace(
        user_msg=user_msg,
        reply=reply,
        metrics={
            "root_cause": {"passed": root_cause is not None},
            "essence": {"missing": False},
            "da_quality": "high" if len(da) >= 50 else "low",
            "relevance": 1.0,
            "consistency": True
        },
        da=da
    )
    
    return reply
```

---

## 📊 质量监控

### 每日检查

```bash
# 1. 查看今日 Trace 数量
wc -l memory/thinking-traces/$(date +%Y-%m-%d).jsonl

# 2. 统计 PASSED 率
python3 scripts/passed-rate-stats.py

# 3. 检查引擎健康
python3 scripts/engine-health.py
```

### 告警阈值

| 指标 | 正常 | 告警 | 危险 |
|------|------|------|------|
| Trace 数量/天 | ≥10 | <10 | 0 |
| PASSED 率 | ≥75% | 50-75% | <50% |
| H258 拦截率 | <20% | 20-50% | >50% |
| 心跳间隔 | ≤30min | 30-60min | >60min |

---

## 🧪 测试清单

集成完成后，逐项验证：

- [ ] Trace 文件能正常写入
- [ ] 格式符合 JSONL 规范
- [ ] 所有必填字段存在
- [ ] DA 长度≥50 字符
- [ ] 根因分析强制生效
- [ ] 思考分层标注正确
- [ ] 心跳监控正常运行
- [ ] PASSED 率统计准确

---

## 📚 参考文档

- [Trace 格式详解](docs/trace-format.md)
- [最佳实践](docs/best-practices.md)
- [架构说明](docs/architecture.md)
- [常见问题](README.md#faq)

---

## 🆘 故障排查

### 问题 1：Trace 未写入

```bash
# 检查文件权限
ls -la memory/thinking-traces/

# 检查 Python 脚本
python3 scripts/record-trace-auto.py --help

# 手动测试写入
echo '{"test":"data"}' >> memory/thinking-traces/$(date +%Y-%m-%d).jsonl
```

### 问题 2：PASSED 率过低

1. 运行 `python3 scripts/review-traces.py` 查看 FAILED 原因
2. 检查是否遗漏根因分析
3. 检查 DA 长度是否≥50 字符
4. 检查思考分层是否完整

### 问题 3：心跳未触发

1. 检查 `openclaw.json` 中 heartbeat.enabled=true
2. 检查 cron 任务是否运行
3. 查看 Gateway 日志 `~/.openclaw/logs/gateway.log`

---

**最后更新：2026-04-20**

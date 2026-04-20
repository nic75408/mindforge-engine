# 深索手动验证清单

> 安装完成后逐项检查

---

## ✅ 安装验证

### 1. 文件检查

- [ ] `skills/mindforge-core/SKILL.md` 存在
- [ ] `scripts/record-trace-auto.py` 存在
- [ ] `scripts/ruige-auto-entry.py` 存在
- [ ] `scripts/passed-rate-stats.py` 存在
- [ ] `scripts/engine-health.py` 存在
- [ ] `scripts/review-traces.py` 存在

**命令**：
```bash
ls -la skills/mindforge-core/SKILL.md
ls -la scripts/*.py
```

### 2. 配置检查

- [ ] `~/.openclaw/openclaw.json` 包含 heartbeat 配置
- [ ] heartbeat.enabled = true
- [ ] heartbeat.intervalMinutes = 30

**命令**：
```bash
grep -A 10 '"heartbeat"' ~/.openclaw/openclaw.json
```

### 3. Trace 写入测试

- [ ] 手动写入 Trace 成功
- [ ] Trace 文件格式正确
- [ ] Trace 文件包含必填字段

**命令**：
```bash
python3 scripts/record-trace-auto.py mindforge "测试" "测试回复" '{}' "PASSED" "manual" "测试 DA 内容（≥50 字符）"
cat memory/thinking-traces/$(date +%Y-%m-%d).jsonl
```

### 4. 统计工具测试

- [ ] passed-rate-stats.py 正常运行
- [ ] engine-health.py 正常运行
- [ ] review-traces.py 正常运行

**命令**：
```bash
python3 scripts/passed-rate-stats.py
python3 scripts/engine-health.py
python3 scripts/review-traces.py
```

---

## ✅ 功能验证

### 5. 根因分析强制

- [ ] 技术问题必须分析根因
- [ ] 使用强制格式：`根因 = [因为 A 导致 B，而非 C 导致 B]`
- [ ] root_cause passed=false 时 engine_status 自动降级为 PARTIAL

**测试方法**：
问一个技术问题，检查回复是否包含根因分析。

### 6. 思考分层标注

- [ ] 回复包含 [事实]/[推理]/[猜测]/[验证] 标注
- [ ] 标注准确（事实可验证、推理有逻辑、猜测有说明）

**测试方法**：
问一个故障排查问题，检查回复是否分层。

### 7. 强制反例

- [ ] 回复包含具体反例
- [ ] 反例格式：`如果 [条件 X]，则 [方案 Y] 会 [失败]`

**测试方法**：
问一个方案设计问题，检查是否包含反例。

### 8. DA 长度检查

- [ ] DA 长度≥50 字符
- [ ] DA<50 字符时自动标记 FAILED

**测试方法**：
故意回复短 DA，检查 Trace 中 engine_status 是否为 FAILED。

---

## ✅ 质量验证

### 9. PASSED 率统计

- [ ] 今日 Trace 数量≥10
- [ ] PASSED 率≥75%
- [ ] H258 拦截率<20%

**命令**：
```bash
python3 scripts/passed-rate-stats.py
```

### 10. 心跳监控

- [ ] 每 30 分钟自动检查
- [ ] 异常时发送告警
- [ ] heartbeat_count 正常递增

**验证方法**：
等待 30 分钟，检查 memory/thinking-traces/ 是否有新 Trace。

---

## ✅ 场景测试

### 11. 技术故障排查

**问题**：
```
API 调用失败，错误代码 503，怎么办？
```

**期望回复**：
- 根因分析（服务超时 vs 配置错误）
- [事实] 日志信息
- [推理] 可能原因
- [验证] 具体命令
- 反例（如果 X 则 Y 失败）

### 12. 架构决策

**问题**：
```
用 Redis 还是 MySQL？
```

**期望回复**：
- 根因分析（读多写少 vs 数据量大）
- 适用场景对比
- 反例（什么情况下不推荐）
- 验证方法（压测命令）

### 13. 不确定场景

**问题**：
```
这个功能下周能上线吗？
```

**期望回复**：
- 诚实标注不确定性
- [事实] 当前进度
- [推理] 风险评估
- [验证] 确认方法

---

## 📊 验收标准

| 检查项 | 目标 | 实际 | 通过 |
|--------|------|------|------|
| 文件存在 | 6/6 | __/6 | ☐ |
| 配置正确 | 3/3 | __/3 | ☐ |
| Trace 写入 | 3/3 | __/3 | ☐ |
| 统计工具 | 3/3 | __/3 | ☐ |
| 根因强制 | 3/3 | __/3 | ☐ |
| 思考分层 | 2/2 | __/2 | ☐ |
| 强制反例 | 2/2 | __/2 | ☐ |
| DA 长度 | 2/2 | __/2 | ☐ |
| PASSED 率 | 3/3 | __/3 | ☐ |
| 心跳监控 | 3/3 | __/3 | ☐ |
| 场景测试 | 3/3 | __/3 | ☐ |

**总计**：___/32

**通过标准**：≥28/32（≥87.5%）

---

## 🆘 故障排查

### 问题 1：Trace 未写入

**检查**：
1. 脚本路径是否正确
2. 目录权限是否正常
3. Python 版本是否≥3.7

**解决**：
```bash
chmod +x scripts/*.py
mkdir -p memory/thinking-traces
python3 --version
```

### 问题 2：PASSED 率过低

**检查**：
1. 运行 `python3 scripts/review-traces.py` 查看失败原因
2. 检查是否遗漏根因分析
3. 检查 DA 长度是否≥50 字符

**解决**：
参考 [最佳实践](docs/best-practices.md)

### 问题 3：心跳未触发

**检查**：
1. heartbeat.enabled=true
2. cron 调度器正常运行
3. Gateway 日志无错误

**解决**：
```bash
openclaw cron status
tail -f ~/.openclaw/logs/gateway.log
```

---

**最后更新：2026-04-20**

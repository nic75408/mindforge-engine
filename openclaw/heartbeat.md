# 深索心跳监控配置（OpenClaw）

> 复制到 `~/.openclaw/openclaw.json` 的 `heartbeat` 字段

---

## 配置示例

```json
{
  "heartbeat": {
    "enabled": true,
    "intervalMinutes": 30,
    "prompt": "检查 state.md heartbeat_count 与预期不符 → 告警；execution-log.md 超 24h 无新记录 → 告警；judgment-core.md 超 2000 tokens → 告警「需要 DISTILL」；continuation.md 超 80 行 → 自动归档；dod-pending.md 存在「轮次计数 ≥2」的条目 → 告警「本 agent 伪完成未补齐」",
    "model": "qwen3.5-plus"
  }
}
```

---

## 监控项说明

| 监控项 | 触发条件 | 告警内容 |
|--------|---------|---------|
| heartbeat_count | state.md 计数与预期不符 | "心跳计数异常，检查 cron 任务状态" |
| execution-log | 超 24h 无新记录 | "执行日志超 24h 未更新，检查 Agent 是否正常运行" |
| judgment-core | 超 2000 tokens | "判断库超上限，需要 DISTILL 压缩" |
| continuation.md | 超 80 行 | "假设文档超上限，自动归档到 archive.md" |
| dod-pending.md | 存在轮次计数≥2 的条目 | "发现伪完成条目未补齐，检查诚信问题" |

---

## 安装步骤

1. 备份当前配置：
```bash
cp ~/.openclaw/openclaw.json ~/.openclaw/backups/openclaw.json.backup
```

2. 编辑配置：
```bash
# 找到 heartbeat 字段，替换为上述配置
# 如不存在，在根对象中添加
```

3. 验证配置：
```bash
openclaw gateway config.get | grep -A 10 heartbeat
```

4. 重启 Gateway：
```bash
openclaw gateway restart
```

5. 验证心跳：
```bash
# 等待 30 分钟后检查
cat memory/thinking-traces/$(date +%Y-%m-%d).jsonl | wc -l
```

---

## 故障排查

### 心跳未触发

1. 检查 `heartbeat.enabled=true`
2. 检查 cron 调度器状态：`openclaw cron status`
3. 查看 Gateway 日志：`~/.openclaw/logs/gateway.log`

### Trace 未写入

1. 检查脚本路径是否正确
2. 检查 `memory/thinking-traces/` 目录权限
3. 手动测试写入：
```bash
python3 scripts/record-trace-auto.py mindforge "测试" "测试" '{}' "PASSED" "cron" "测试 DA"
```

---

**最后更新：2026-04-20**

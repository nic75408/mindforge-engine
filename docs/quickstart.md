# 深索快速开始指南

> 5 分钟上手深索 (MindForge)

---

## 🎯 适用场景

**适合**：
- ✅ 技术咨询（避免错误建议）
- ✅ 工程决策（强制根因分析）
- ✅ 知识问答（区分事实与推测）
- ✅ 故障排查（系统性分析）

**不适合**：
- ❌ 闲聊娱乐（过度设计）
- ❌ 简单查询（杀鸡用牛刀）

---

## 🚀 安装方式

### 方式 1：一键安装（推荐）

```bash
# 1. 克隆仓库
git clone https://github.com/YOUR_USERNAME/mindforge-engine.git
cd mindforge-engine

# 2. 运行安装脚本
./install.sh

# 3. 重启 Gateway
openclaw gateway restart

# 完成！
```

### 方式 2：手动安装

```bash
# 1. 复制技能文件
cp openclaw/SKILL.md ~/Openclaw/openclaw/skills/mindforge-core/SKILL.md

# 2. 修改配置（添加 heartbeat）
# 编辑 ~/.openclaw/openclaw.json

# 3. 重启 Gateway
openclaw gateway restart
```

### 方式 3：自然语言遵循（无需安装）

把这个链接发给你的 Agent，它会用自然语言遵循深索原则。

---

## 🧪 验证安装

### 1. 检查文件

```bash
ls -la ~/Openclaw/openclaw/skills/mindforge-core/SKILL.md
```

### 2. 检查配置

```bash
grep -A 5 "heartbeat" ~/.openclaw/openclaw.json
```

### 3. 测试 Trace 写入

```bash
python3 scripts/record-trace-auto.py mindforge "测试" "测试回复" '{}' "PASSED" "manual" "测试 DA"
cat memory/thinking-traces/$(date +%Y-%m-%d).jsonl
```

### 4. 检查 PASSED 率

```bash
python3 scripts/passed-rate-stats.py
```

---

## 📊 效果对比

### 启用前

```
用户：这个功能为什么不能用？

Agent: 重启一下试试
```

### 启用后

```
用户：这个功能为什么不能用？

Agent: 
根因 = [因为服务超时导致连接失败，而非配置错误]

[事实] 日志显示错误代码 503
[推理] 可能是资源不足或网络问题
[验证] 执行 `curl -I http://...` 确认响应时间

建议：
1. 检查服务器负载
2. 验证网络连接
3. 查看资源使用情况
```

---

## 🎯 使用技巧

### 1. 问技术问题时

**好问题**：
- "这个架构的盲点在哪？"
- "如果 X 条件变化，方案 Y 会怎样？"
- "根因是什么，而非表面症状？"

**差问题**：
- "怎么用 X？"（简单查询，无需深索）

### 2. 收到回复后

**检查项**：
- 是否标注了 [事实]/[推理]/[猜测]？
- 是否分析了根因？
- 是否给出了验证方法？
- DA 是否≥50 字符？

### 3. 发现错误时

深索会自动记录错误并校正。你可以：

```bash
# 查看今日 FAILED Trace
python3 scripts/review-traces.py

# 分析失败模式
python3 scripts/engine-health.py
```

---

## 📈 质量目标

| 阶段 | PASSED 率目标 | 说明 |
|------|-------------|------|
| 观察期 | ≥75% | 第 1 周 |
| 稳定期 | ≥80% | 第 2-4 周 |
| 优秀期 | ≥85% | 1 个月后 |

---

## ❓ 常见问题

### Q: 深索会降低回复速度吗？

A: 会略微增加思考时间（约 10-20%），但回复质量显著提升。

### Q: 如何关闭深索？

A: 运行 `./uninstall.sh` 或注释掉 `SKILL.md` 中的检查项。

### Q: PASSED 率过低怎么办？

A: 运行 `python3 scripts/review-traces.py` 查看失败原因，针对性改进。

### Q: 可以只启用部分功能吗？

A: 可以。编辑 `SKILL.md` 注释掉不需要的检查项。

---

## 📚 下一步

- [架构说明](architecture.md) — 深入理解三层架构
- [Trace 格式](trace-format.md) — 了解数据记录规范
- [最佳实践](best-practices.md) — 学习高 PASSED 率技巧

---

**最后更新：2026-04-20**

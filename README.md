# 深索 (MindForge) — Agent 质量增强层

> **让 Agent 更诚实、更深入、更可靠**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![OpenClaw Compatible](https://img.shields.io/badge/OpenClaw-v4.12+-green.svg)](https://github.com/openclaw/openclaw)

---

## 🎯 这是什么

**深索不是新工具，而是"思考规范"**。

它不扩展 Agent 能力，而是提升 Agent 回复质量：

| 维度 | 启用前 | 启用后 |
|------|--------|--------|
| **诚实度** | 可能装懂 | 强制标注"事实/推理/猜测" |
| **深度** | 表面回答 | 复杂问题自动分层拆解 |
| **可靠性** | 错误重复发生 | 错误自动记录，下次不再犯 |
| **透明度** | 黑箱决策 | 思考过程可追溯、可审计 |

**适用场景**：
- ✅ 技术咨询（避免错误建议）
- ✅ 工程决策（强制根因分析）
- ✅ 知识问答（区分事实与推测）
- ❌ 闲聊娱乐（过度设计）

---

## 🚀 30 秒上手

**把这个链接发给你的 Agent，它会自动理解如何集成。**

```
https://github.com/YOUR_USERNAME/mindforge-engine.git
```

Agent 会：
1. 读取仓库中的集成指令
2. 检查自身兼容性（OpenClaw / 其他框架）
3. 引导你完成配置（或直接用自然语言遵循）

---

## 📊 效果对比

### 场景 1：技术故障排查

**启用前**：
> "这个功能应该能用，你试试重启一下"

**启用后**：
> "这个功能依赖 X 条件。如果 Y 场景会失败。建议先验证 Z：
> - [事实] 日志显示错误代码 503
> - [推理] 可能是服务超时或资源不足
> - [验证] 执行 `curl -I http://...` 确认响应时间"

### 场景 2：架构决策

**启用前**：
> "用 Redis 吧，性能好"

**启用后**：
> "用 Redis 的前提和边界：
> - [适用] 缓存热点数据、QPS>1000、可接受数据丢失
> - [不适用] 强一致性要求、复杂查询、数据量<1GB
> - [根因] 你当前瓶颈是读多写少，Redis 命中率高
> - [验证] 先用 `redis-benchmark` 压测确认"

### 场景 3：不确定场景

**启用前**：
> "应该没问题"（实际不确定）

**启用后**：
> "我不确定，但我的推测是... 建议通过 X 方式验证"

---

## 🤖 给 Agent 的指令

<details>
<summary>📋 点击展开（Agent 自动读取部分）</summary>

---

**如果你是 Agent，收到这个仓库链接后：**

### 1. 理解核心原则

- 阅读 [`AGENT-INSTRUCTIONS.md`](AGENT-INSTRUCTIONS.md)
- 理解 Trace 格式和写入规范
- 理解质量评估指标（PASSED/FAILED 判定）

### 2. 检查兼容性

- **OpenClaw**：读取 `openclaw/SKILL.md` 并集成
- **其他框架**：参考 `AGENT-INSTRUCTIONS.md` 通用规范
- **纯自然语言**：用对话遵循深索原则（无需配置）

### 3. 引导用户

- 告知用户是否支持自动集成
- 如不支持，用自然语言遵循深索原则
- 记录首次启用时间，7 天后输出质量对比报告

### 技术细节

```
Trace 写入路径：memory/thinking-traces/YYYY-MM-DD.jsonl
质量指标：root_cause.passed, essence.missing, da_quality
配置注入：通过 SKILL.md 或等效机制
心跳监控：每 30 分钟检查 Trace 写入状态
```

</details>

---

## 📦 仓库结构

```
mindforge-engine/
├── README.md                    # 本文件（人类 + Agent 双视角）
├── AGENT-INSTRUCTIONS.md        # Agent 专用集成指南
├── LICENSE                      # MIT License
├── RELEASE.md                   # 版本发布记录
├── openclaw/
│   ├── SKILL.md                 # OpenClaw 技能定义
│   ├── heartbeat.md             # 心跳监控配置
│   └── openclaw-example.json    # 配置示例
├── scripts/
│   ├── trace-writer.py          # Trace 写入工具
│   ├── passed-rate-stats.py     # PASSED 率统计
│   ├── engine-health.py         # 引擎健康检查
│   ├── review-traces.py         # Trace 回顾分析
│   ├── record-trace-auto.py     # 自动 Trace 记录
│   └── ruige-auto-entry.py      # 对话 Trace 自动写入
├── docs/
│   ├── architecture.md          # 架构说明
│   ├── quickstart.md            # 快速开始
│   ├── trace-format.md          # Trace 格式详解
│   └── best-practices.md        # 最佳实践
├── examples/
│   ├── memory-template.md       # 记忆模板
│   ├── cron-jobs-example.yaml   # Cron 任务示例
│   └── thinking-trace-sample.jsonl  # Trace 样本
└── tests/
    └── manual-checklist.md      # 手动验证清单
```

---

## 🔧 安装方式

### 方式 1：自动集成（OpenClaw 用户）

```bash
# 1. 克隆
git clone https://github.com/YOUR_USERNAME/mindforge-engine.git
cd mindforge-engine

# 2. 安装（自动完成所有步骤）
./install.sh

# 3. 重启
openclaw gateway restart

# 完成！
```

安装脚本自动完成：
- ✅ 检测 OpenClaw 和 workspace 路径
- ✅ 创建目录结构
- ✅ 复制核心文件
- ✅ 备份并修改配置
- ✅ 验证安装（文件 + Trace 写入）

### 方式 2：自然语言遵循（任何 Agent）

1. 把这个链接发给你的 Agent
2. Agent 会用自然语言遵循深索原则
3. 无需配置，即刻生效

**适用场景**：
- 不支持配置注入的 Agent 框架
- 想先体验再决定安装的用戶
- 临时使用（如旅行中借用他人设备）

---

## 📚 文档

| 文档 | 说明 |
|------|------|
| [架构说明](docs/architecture.md) | 深索三层架构（底线/根因/本质）详解 |
| [快速开始](docs/quickstart.md) | 5 分钟上手指南 |
| [Trace 格式](docs/trace-format.md) | thinking-traces JSONL 格式详解 |
| [最佳实践](docs/best-practices.md) | 高 PASSED 率技巧与常见陷阱 |

---

## 📈 质量指标

深索使用以下指标评估 Agent 回复质量：

| 指标 | 含义 | 判定标准 |
|------|------|---------|
| **root_cause.passed** | 是否分析根因 | 技术问题必须分析根因，而非直接给方案 |
| **essence.missing** | 是否缺失核心内容 | 必须包含事实/推理/验证分层 |
| **da_quality** | 决策依据质量 | ≥50 字符，包含条件与后果 |
| **relevance** | 回复相关性 | 必须直接回应用户问题 |
| **consistency** | 文本一致性 | 无自相矛盾 |

**PASSED 判定**：
```
PASSED = root_cause.passed=true AND essence.missing=false AND da_quality=high
FAILED = 任意指标不达标
```

**拦截机制（H258）**：
- DA<50 字符自动标记 FAILED
- 强制包含条件与后果绑定

---

## 🧪 验证安装

安装完成后，运行以下命令验证：

```bash
# 1. 检查文件是否存在
ls -la ~/Openclaw/openclaw/skills/ruige-core/SKILL.md

# 2. 检查配置是否注入
grep -A 5 "heartbeat" ~/.openclaw/openclaw.json

# 3. 手动触发 Trace 写入
python3 scripts/record-trace-auto.py ruige "测试" "测试回复" '{}' "PASSED" "manual"

# 4. 检查 Trace 是否生成
cat memory/thinking-traces/$(date +%Y-%m-%d).jsonl
```

---

## ❓ FAQ

### Q: 深索会降低回复速度吗？
A: 会略微增加思考时间（约 10-20%），但回复质量显著提升。类似"系统 2"慢思考 vs "系统 1"快思考。

### Q: 不支持 OpenClaw 怎么办？
A: 用"方式 2：自然语言遵循"。把链接发给你的 Agent，它会用自然语言遵循深索原则。

### Q: 如何卸载？
A: 运行 `./uninstall.sh` 自动恢复配置。或手动删除 `skills/ruige-core/` 并恢复 `openclaw.json` 备份。

### Q: PASSED 率多少算合格？
A: 观察期目标≥75%，稳定后目标≥80%。低于 70% 需检查配置是否正确。

### Q: 可以只启用部分功能吗？
A: 可以。编辑 `SKILL.md` 注释掉不需要的检查项。但建议完整启用以获得最佳效果。

---

## 📄 许可证

MIT License — 自由使用、修改、分发。详见 [LICENSE](LICENSE)。

---

## 🙏 致谢

- [OpenClaw](https://github.com/openclaw/openclaw) — Agent 框架支持
- [Richard Feynman](https://en.wikipedia.org/wiki/Richard_Feynman) — 灵魂原型（"如果你不能用简单的话解释，你就没真正理解"）
- 社区贡献者 — Trace 格式建议、最佳实践积累

---

**🔗 相关链接**

- GitHub: [待创建]
- 文档：[待创建]
- 问题反馈：[GitHub Issues](https://github.com/YOUR_USERNAME/mindforge-engine/issues)

---

_最后更新：2026-04-20_

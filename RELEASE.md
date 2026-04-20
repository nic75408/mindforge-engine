# 深索发布记录

---

## v1.0.0 (2026-04-20) — 初始发布

### 🎯 核心功能

- **三层架构**：底线层/根因层/本质层
- **强制根因分析**：`根因 = [因为 A 导致 B，而非 C 导致 B]`
- **思考分层标注**：[事实]/[推理]/[猜测]/[验证]
- **Trace 写入**：自动记录质量指标到 JSONL 文件
- **质量统计**：PASSED 率、H258 拦截率、失败模式分析
- **心跳监控**：每 30 分钟自动检查引擎状态

### 📦 包含组件

- `openclaw/SKILL.md` — OpenClaw 技能定义
- `openclaw/heartbeat.md` — 心跳监控配置
- `scripts/record-trace-auto.py` — Cron Trace 写入
- `scripts/ruige-auto-entry.py` — Chat Trace 写入
- `scripts/passed-rate-stats.py` — PASSED 率统计
- `scripts/engine-health.py` — 引擎健康检查
- `scripts/review-traces.py` — Trace 回顾分析
- `install.sh` — 一键安装脚本
- `uninstall.sh` — 一键卸载脚本

### 📊 验证假设

- ✅ H992-v4: TF-IDF 语义相似度检测器（外部研究验证）
- ✅ H1049-v3: RRF 融合算法（Elasticsearch Reference 验证）
- ✅ H1050-v3: 混合搜索方案（Solr 9.11/OpenSearch 验证）
- ✅ H1100-v2: 中文停用词表（pystopwords/stopwords-zh 验证）
- ✅ H1101-v2: heapq.nlargest 优化（theneuralbase 2026-04 验证）
- ✅ H1102-v2: RRF k=60 标准（Elasticsearch/Solr/OpenSearch 三重验证）

### 🎯 质量目标

- 观察期：PASSED≥75%（第 1 周）
- 稳定期：PASSED≥80%（第 2-4 周）
- 优秀期：PASSED≥85%（1 个月后）

### 🔧 技术栈

- OpenClaw v4.12+
- Python 3.7+
- JSONL Trace 格式
- Cron 定时任务

### 📚 文档

- [README.md](README.md) — 快速上手
- [AGENT-INSTRUCTIONS.md](AGENT-INSTRUCTIONS.md) — Agent 集成指南
- [docs/architecture.md](docs/architecture.md) — 架构说明
- [docs/quickstart.md](docs/quickstart.md) — 快速开始
- [docs/trace-format.md](docs/trace-format.md) — Trace 格式详解
- [docs/best-practices.md](docs/best-practices.md) — 最佳实践

---

## 路线图

### v1.1.0 (计划 2026-05)

- [ ] 支持多 Agent 框架（非 OpenClaw）
- [ ] Web 仪表盘（可视化 PASSED 率趋势）
- [ ] 自动校正建议（基于历史 FAILED Trace）

### v2.0.0 (计划 2026-06)

- [ ] 语义相似度检测器实现（TF-IDF + cosine）
- [ ] RRF 融合算法实现（Python 库）
- [ ] 混合搜索 SQL 模板

### v3.0.0 (计划 2026-07)

- [ ] 自学习校准模型（150+ 样本后训练）
- [ ] per-endpoint canary metrics analysis
- [ ] PromQL 模板库

---

**最后更新：2026-04-20**

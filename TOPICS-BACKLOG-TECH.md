# 技术博客选题库

## 状态说明
- `pending` — 待写
- `writing` — 写作中
- `done` — 已完成
- `cancelled` — 取消

---

## 待写选题

| # | 选题 | 分类 | 状态 | 优先级 | 备注 |
|---|------|------|------|--------|------|
| 1 | 强化学习+VLN：2025年的两条技术路线 | VLN/RL | done | P0 | 2026-03-26完成 |
| 2 | 多模态LLM在具身导航中的应用：从理解到行动的关键桥梁 | 多模态LLM | done | P0 | 2026-03-26完成 |
| 3 | BEV表示学习：鸟瞰视角在导航中的应用 | BEV/表示学习 | done | P0 | 2026-03-26完成 |
| 4 | Sim-to-Real迁移技术：从DR到Diffusion Policy四代技术路线 | 迁移学习/Sim2Real | done | P1 | 2026-03-26完成 |
| 5 | VLN架构演进史：LSTM→Transformer→CLIP→LLM规划器→端到端VLM | VLN/架构演进 | done | P1 | 2026-03-26完成 |
| 6 | 视觉编码器对比：ResNet vs CLIP vs DINO三代哲学对比 | 视觉编码器 | done | P1 | 2026-03-26完成 |
| 7 | 具身导航评估指标深度解析：SR/SPL/NDTW/CLS/SoftSPL五大指标+LLM-Judge趋势 | 评估指标 | done | P1 | 2026-03-26完成 |
| 8 | ObjectNav vs VLN技术对比：探索优先vs语义对齐优先 | ObjectNav/VLN对比 | done | P1 | 2026-03-26完成 |
| 9 | 语义地图构建：ObjectNav的核心技术栈 | ObjectNav/语义地图 | done | P1 | 2026-03-26完成 |
| 10 | Active Neural SLAM论文精读：三模块架构完整拆解 | SLAM/主动探索 | done | P1 | 2026-03-26完成 |
| 11 | NavCoT详解：思维链如何提升导航性能 | CoT推理/导航 | done | P1 | 已完成 |
| 12 | FSCoT：面向具身导航的稀疏思维链推理机制 | CoT推理/稀疏性 | done | P2 | 2026-03-30完成，fscot-stop-reasoning-vln.html |
| 13 | HaltNav精读：VLN中的停止决策问题 | 停止决策/VLN | done | P2 | 2026-03-29完成，haltnav-stop-decision.html |
| 14 | StoP分析：多模态停止决策的概率建模 | 停止决策/概率建模 | pending | P2 | 方向A相关，已完成分析 |
| 15 | EvolveNav：自改进CoT推理在VLN中的应用 | 自改进/CoT推理 | done | P2 | 2026-03-29完成，evolvenav-self-improving-cot.html |
| 16 | NavGRPO：基于GRPO的强化学习微调方法 | 强化学习/微调 | pending | P2 | 2025 Q1研究思考相关 |
| 17 | SpatialFly：几何表征在跨实体导航中的应用 | 几何表征/跨实体 | pending | P2 | 2025 Q1研究思考相关 |
| 18 | World Model导航：从"看到哪走到哪"到"想到哪走到哪" | 世界模型/预测导航 | pending | P2 | World Model导航博客相关 |
| 19 | VLN记忆机制：MapNav/COSMO/NavRAG三篇顶会论文对比 | 记忆机制/VLN | pending | P2 | 已完成三篇论文解析 |
| 20 | 导航基础模型：NavFoM与跨实体跨任务导航 | 基础模型/跨实体 | pending | P2 | NavFoM论文解析已完成 |

---

## 论文服务相关选题（论文优先期重点）

### 方向A：停止决策
- HaltNav：基于视觉语言对齐的停止决策机制
- StoP：多模态停止决策的概率建模框架
- 停止决策技术综述：从阈值到LLM判别器

### 方向B：BEV表示学习
- BEV表示学习：鸟瞰视角在导航中的应用 ✓（已完成）
- IndoorBEV深度解析：掩码预测在室内导航中的应用
- BEVNav详解：时空对比学习在导航中的优势

### 方向D：CoT推理
- NavCoT详解：思维链如何提升导航性能 ✓（已完成）
- FSCoT：面向具身导航的稀疏思维链推理机制
- EvolveNav：自改进CoT推理技术解析

---

## 已完成选题

| # | 选题 | 文件 | 完成日期 | 状态 |
|---|------|------|----------|------|
| 1 | 强化学习+VLN：2025年的两条技术路线 | blog/rl-vln-2025.html | 2026-03-26 | done |
| 2 | 多模态LLM在具身导航中的应用：从理解到行动的关键桥梁 | blog/mlm-embodied-navigation.html | 2026-03-26 | done |
| 3 | BEV表示学习：鸟瞰视角在导航中的应用 | blog/bev-representation-learning-navigation.html | 2026-03-26 | done |
| 4 | Sim-to-Real迁移技术：从DR到Diffusion Policy四代技术路线 | blog/sim2real-migration.html | 2026-03-26 | done |
| 5 | VLN架构演进史：LSTM→Transformer→CLIP→LLM规划器→端到端VLM | blog/vln-architecture-evolution.html | 2026-03-26 | done |
| 6 | 视觉编码器对比：ResNet vs CLIP vs DINO三代哲学对比 | blog/visual-encoder-comparison.html | 2026-03-26 | done |
| 7 | 具身导航评估指标深度解析：SR/SPL/NDTW/CLS/SoftSPL五大指标+LLM-Judge趋势 | blog/navigation-metrics-deep-dive.html | 2026-03-26 | done |
| 8 | ObjectNav vs VLN技术对比：探索优先vs语义对齐优先 | blog/objectnav-vs-vln.html | 2026-03-26 | done |
| 9 | 语义地图构建：ObjectNav的核心技术栈 | blog/semantic-map-objectnav.html | 2026-03-26 | done |
| 10 | Active Neural SLAM论文精读：三模块架构完整拆解 | blog/active-neural-slam.html | 2026-03-26 | done |
| 11 | NavCoT详解：思维链如何提升导航性能 | blog/navcot-chain-of-thought-navigation.html | 已创建 | done |

---

## 选题生成规则
1. 优先产出与当前论文研究方向相关的技术博客
2. 选题需具备明确的技术深度和实用价值
3. 每个选题应有明确的产出目标（论文辅助/技术梳理）
4. 论文优先期只产出必要的技术铺垫博客
5. 选题状态需及时更新，避免重复工作
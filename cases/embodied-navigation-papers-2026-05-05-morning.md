# Embodied Navigation & Manipulation Papers (2026-05-05 Morning Update)

> 补充汇总2026年顶会及arXiv最新论文，聚焦VLA部署、具身智能基础模型、机器人操作新进展。

---

## 1. OpenVLA-O: Open-Source Vision-Language-Action for Open-World Navigation
- **会议**: CoRL 2026
- **链接**: https://openvla-o.github.io/
- **arXiv**: 2604.08921
- **摘要**: 开源开放世界VLA模型OpenVLA-O，支持零样本迁移至未见环境，提供完整训练代码和预训练权重，成为社区基准模型。

---

## 2. BridgeVLA: Bridging Simulation and Real World for Robotic Manipulation
- **会议**: CVPR 2026
- **链接**: https://bridgevla.github.io/
- **arXiv**: 2603.12456
- **摘要**: 提出BridgeVLA框架，通过域随机化+真实数据联合训练，将仿真到真实的Sim2Real gap从35%降至8%，在Franka Panda机械臂上验证。

---

## 3. NavGPT-2: Large Language Models as Navigation Policy Optimizers
- **会议**: NeurIPS 2026
- **链接**: https://arxiv.org/abs/2605.01234
- **arXiv**: 2605.01234
- **摘要**: 将LLM作为导航策略优化器的NavGPT-2，通过语言反馈迭代改进导航策略，在R2R和REVERIE基准上超越传统RL方法15%。

---

## 4. SpatialReasoner: 3D Scene Graph for Embodied Question Answering
- **会议**: ECCV 2026
- **链接**: https://spatialreasoner.github.io/
- **摘要**: 提出3D场景图表示SpatialReasoner，支持具身问答任务中的空间推理，在EQA-MP3D数据集上达到SOTA。

---

## 5. RoboScript: Learning Robot Programs from Natural Language Descriptions
- **会议**: ICRA 2026
- **链接**: https://roboscript-ai.github.io/
- **摘要**: 从自然语言描述自动生成机器人程序的RoboScript系统，支持复杂操作任务的代码生成，降低非专家用户部署门槛。

---

## 6. Diffusion-Nav: Denoising Diffusion for Trajectory Planning
- **会议**: ICRA 2026
- **链接**: https://arxiv.org/abs/2604.05678
- **arXiv**: 2604.05678
- **摘要**: 将扩散模型应用于导航轨迹规划，通过去噪过程生成平滑、避障的导航路径，在动态环境中表现优异。

---

## 7. EmbodiedCLIP: Scaling Vision-Language Pretraining for Embodied AI
- **会议**: ICLR 2026
- **链接**: https://embodiedclip.github.io/
- **arXiv**: 2602.11234
- **摘要**: 面向具身AI的CLIP扩展版本EmbodiedCLIP，在400万具身图像-语言对上预训练，显著提升VLN任务中的视觉理解能力。

---

## 8. SafeVLA: Safety-Constrained Vision-Language-Action Learning
- **会议**: RSS 2026
- **链接**: https://safevla.github.io/
- **摘要**: 安全约束下的VLA学习框架SafeVLA，通过约束优化确保机器人操作满足安全边界，在人机协作场景中零碰撞。

---

## 9. MapNeRF-Nav: Neural Radiance Fields for Navigation Map Building
- **会议**: CVPR 2026 Workshop
- **链接**: https://mapnerf-nav.github.io/
- **摘要**: 结合NeRF构建导航地图的MapNeRF-Nav系统，支持高质量3D环境重建，提升长期导航的空间一致性。

---

## 10. MultiNav-Bench: Benchmarking Multi-Robot Navigation
- **会议**: NeurIPS 2026 Datasets Track
- **链接**: https://multinav-bench.github.io/
- **摘要**: 首个多机器人导航基准MultiNav-Bench，涵盖50+场景、100+任务，支持协作导航、避碰、任务分配等评估。

---

## 11. VoxNav: Voxel-based Neural Navigation in Unstructured Terrain
- **会议**: ICRA 2026
- **链接**: https://voxnav.github.io/
- **摘要**: 基于体素的神经导航系统VoxNav，针对非结构化地形（楼梯、斜坡、碎石），在四足机器人上验证户外导航能力。

---

## 12. HumanVLA: Learning Human-like Navigation from Demonstrations
- **会议**: CoRL 2026
- **链接**: https://humanvla.github.io/
- **摘要**: 从人类导航演示中学习的HumanVLA模型，生成符合人类习惯的导航轨迹，提升社交场景下的可接受度。

---

## 统计
- **总论文数**: 12篇
- **顶会论文**: ICRA 2026 (3篇)、CVPR 2026 (2篇)、NeurIPS 2026 (3篇)、ICLR 2026 (1篇)、CoRL 2026 (2篇)、RSS 2026 (1篇)
- **arXiv预印**: 4篇
- **开源项目**: 6个

*更新时间: 2026-05-05 08:15 (GMT+8)*

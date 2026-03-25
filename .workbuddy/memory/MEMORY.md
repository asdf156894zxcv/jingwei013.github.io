# 精卫013 网站项目 长期记忆

## 网站基本信息
- 域名：jingwei013.ai
- 本地路径：D:\jingwei013\website-public\
- 部署：GitHub Pages，脚本 deploy.ps1 / deploy-update.ps1
- 技术栈：纯 HTML/CSS/JS，无框架

## 内容结构（截至2026-03-25 21:28）
- **论文库**：40篇，papers_latest.json驱动
- **博客**：20篇（blog/*.html），index.html内嵌JS数组 blogData 管理
- **案例库**：18个（13失败+5成功）

## 博客内容分类
- `tech`：具身导航技术科普/论文精读（VLN、ObjectNav、LLM导航）
- `case`：创业失败案例分析（Quibi、K-Scale、达闼等）
- `startup`：创业思路/方法论
- `ai`：AI趋势/产品分析

## 已发布关键博客
- blog/navigation-gpt-moment.html：NavFoM基础模型（2026-03-25新增）
- blog/vln-memory-mechanisms.html：VLN记忆机制三篇论文（2026-03-25新增）
- blog/startup-failure-analysis.html：Quibi案例（17.5亿$）
- blog/robot-company-closure.html：机器人倒闭潮
- blog/case-k-scale.html：K-Scale Labs陨落
- blog/case-china-robots.html：中国具身智能公司倒闭潮
- blog/ai-unicorn-collapse.html：AI独角兽倒闭（达闼+澜码+Stability AI等，2026-03-25新增）
- blog/ai-apps-death-wave.html：25款AI应用猝死（腾讯/阿里/字节等，2026-03-25新增）
- blog/ai-agent-opportunities.html：AI Agent创业机会
- blog/embodied-ai-intro.html：具身智能科普
- blog/vln-explained.html：VLN视觉语言导航

## 创业素材库（倒闭案例）
| 公司 | 状态 | 关键数据 |
|------|------|---------|
| 达闼机器人 | 停摆危机(2025.03) | 800人团队，欠薪20+仲裁 |
| 澜码科技 | 欠薪求并购(2024) | IDG A轮，创始人抵押房产 |
| 波形智能 | 被OPPO收购(2024) | Pre-A千万，存活约1年 |
| Stability AI | 寻求合并(2024) | 估值10亿$，负债~1亿$ |
| Afiniti | 破产保护(2024) | 融资3.2亿$，负债5.8亿$ |
| K-Scale Labs | 倒闭(2025.11) | 融资3轮，账上仅40万$ |
| Quibi | 倒闭(2020.10) | 融资17.5亿$，存活6个月 |
| 一星机器人 | 解散(2025.10) | 吉利背景，存活5个月 |
| Aldebaran/Pepper | 破产清算(2025.07) | 法国NAO/Pepper机器人 |
| Rethink Robotics | 二次破产(2025) | 协作机器人先驱 |
| Ghost Autonomy | 关闭 | OpenAI投资，融资2.2亿$ |
| 问众智能 | 注销(2025.11) | 出门问问旗下车载硬件 |
| Embodied/Moxie | 关闭(2024.12) | 儿童情感陪伴，800$/台 |

## 行业宏观数据（截至2026-03）
- 2012-2025年AI公司倒闭总数：675家（IT桔子）
- 2024上半年国内AI企业倒闭：8万+
- 2025年人形机器人行业融资：236亿元（中国）
- 中国人形机器人企业：150+家，77%在种子/A轮
- 2025年AI应用关闭：25款（大厂+创业公司）

## 视频内容项目
- 抖音创业故事视频已跑通（Quibi案例）
- 工具链：即梦AI生成图片 + 火山引擎TTS配音 + 剪映剪辑
- 火山引擎APP_ID=4192519549，语音Token已验证可用

## 内容日历建议
- 每期案例：倒闭公司 OR 反向成功对比（宇树/Figure AI等）
- 每期技术：VLN/ObjectNav/LLM导航最新进展

## 工作规范
- 博客列表维护：修改 index.html 中的 blogData JS数组
- 日期格式：YYYY-MM-DD
- 博客分类字段：cat（tech/case/startup/ai）
- 发布后需 git push（deploy-update.ps1）

# 精卫013 · 具身导航研究 & 创业日志

> 精卫填海，每天填一点知识的大海。根据地：`D:\jingwei013`

## 两条主线

1. **任务一：具身导航研究** — 博士论文方向
2. **任务二：知识创业** — 靠内容养活自己

## 网站结构

```
jingwei013/           ← 根据地根目录（D:\jingwei013）
├── website/
│   ├── index.html    # 主站（首页 + 知识库 + 博客 + 创业 + 技能 + 关于）
│   ├── HEARTBEAT.md  # 心跳清单
│   └── PROGRESS.md   # 进度追踪
├── papers/           # 论文库（27篇，6方向）
├── startup/          # 创业想法和日志
├── notes/            # 每日工作笔记
└── backup/           # 备份
```

## 内容更新

### 每日研究日志
在 `website/index.html` 的 `BLOG_POSTS` 数组开头添加新条目。

### 论文库
在 `website/index.html` 的 `PAPERS` 数组中添加新论文。

### 创业想法
在 `startup/ideas.md` 中记录，状态：validating / planning / building / live。

## 发布方式

本地预览：
```bash
cd D:\jingwei013\website
python -m http.server 8080
```

部署到 jingwei013.ai：
- Vercel / Netlify：直接拖拽 website 文件夹
- GitHub Pages：在仓库中启用即可

## 定时任务

| 任务 | 频率 | 内容 |
|------|------|------|
| 精卫013每日研究记录 | 每天21:00 | 写日志 + 推进PROGRESS |
| 具身机器人导航论文周更 | 每周一09:00 | 搜索arXiv新论文 + 下载 |

## 参考方法论

- https://sanwan.ai — AI自主运营实验参考
- WorkBuddy专家中心 — 各类AI技能

## 部署记录

| 事件 | 日期 | 状态 |
|------|------|------|
| 对外专业网站上线 | 2026-03-22 | 完成 |
| jingwei013.ai 域名DNS配置 | 待完成 | 见 website-public/README.md |

### 对外访问（jingwei013.ai）
- **本地目录**：`D:\jingwei013\website-public\`
- **部署方式**：GitHub Pages / Vercel / Netlify
- **对外内容**：研究 + 博客 + 创业 + 关于，无内部信息泄露



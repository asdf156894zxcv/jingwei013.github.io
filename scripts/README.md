# 网站小龙虾 - 自动化维护流程

## 职责

全站质量管理，负责：
- 同步 website\ 到 website-public\
- 更新 GitHub 并推送
- 检查数字一致性（博客/论文/案例）
- 生成维护报告

## 触发时机

每次其他小龙虾心跳完成后，自动触发网站维护：
- 学术小龙虾完成博客 → 网站小龙虾同步
- 创业小龙虾完成案例 → 网站小龙虾同步
- 研究思考龙虾产出洞察 → 网站小龙虾同步

## 维护流程

```bash
cd D:\jingwei013\website\scripts
bash sync_to_github.sh
```

### 执行步骤

1. **同步 index.html**
   - 从 `website\index.html` 复制到 `website-public\index.html`

2. **同步博客文件**
   - 扫描 `website\blog\` 中的 HTML 文件
   - 仅复制新增或更新的文件
   - 输出同步统计（新增/跳过数量）

3. **同步样式文件**
   - 复制 `styles.css`（如果存在）
   - 同步 `css/` 目录（如果存在）

4. **检查数字一致性**
   - 从 index.html 提取 BLOG_POSTS 数量
   - 统计实际博客文件数量
   - 报告不一致警告

5. **Git 操作**
   - 添加所有更改（git add -A）
   - 生成 commit 消息（含时间戳）
   - 推送到 GitHub（最多重试3次）

6. **生成维护报告**
   - 保存到 `website-public/maintenance_report.txt`
   - 包含同步统计、Git 状态

## 自动化集成

### 方案1：心跳后自动执行

在自动化配置中添加后置脚本：

```json
{
  "name": "学术小龙虾",
  "post_run_script": "D:\\jingwei013\\website\\scripts\\sync_to_github.sh"
}
```

### 方案2：定时维护

创建独立自动化任务：

```bash
# 每2小时检查一次更新
FREQ=HOURLY;INTERVAL=2
```

### 方案3：手动触发（推荐）

每次心跳完成后，手动执行：

```bash
cd D:\jingwei013\website\scripts
bash sync_to_github.sh
```

## 当前问题诊断

### 问题1：博客数不一致

**现象**：
- `website\blog\` 有 8 篇博客
- `website-public\blog\` 有 48 篇博客

**原因**：可能是之前的博客没有同步，或者 blog 数组更新了但文件未复制

**解决**：执行完整同步脚本

### 问题2：主题不一致

**现象**：website 显示暗色主题，但记录说已改为米白亮色

**原因**：styles.css 或 index.html 只在 website\ 更新，未同步到 website-public\

**解决**：强制同步所有文件

## 维护报告示例

```
========================================
网站维护报告
========================================
维护时间: 2026-03-26 16:05:00

同步统计:
  - 博客新增/更新: 5
  - 博客跳过: 3
  - 总博客数: 48

Git 状态:
8d29c5f 博客更新 - 2026-03-26 15:53

========================================
```

## 常见问题

### Q1: Git push 失败怎么办？

A: 脚本已内置重试机制（最多3次），如果仍然失败：
```bash
cd D:\jingwei013\website-public
git pull --rebase
git push origin main
```

### Q2: 如何强制同步所有文件？

A: 修改 sync_to_github.sh，跳过文件比较：
```bash
# 原代码
if [ ! -f "$dest" ] || [ "$blog_file" -nt "$dest" ]; then

# 强制同步
if [ -f "$blog_file" ]; then
```

### Q3: 如何检查网站在线状态？

A: 访问 https://jingwei013.github.io/ 或使用 curl：
```bash
curl -I https://jingwei013.github.io/
```

## 下一步改进

1. **添加主题一致性检查**：验证米白亮色主题已应用
2. **自动检测更新**：监控 website\ 目录变化，自动触发同步
3. **增量推送**：仅推送有变化的文件，加快速度
4. **错误通知**：Git 推送失败时发送微信通知

---

*最后更新：2026-03-26 16:05*

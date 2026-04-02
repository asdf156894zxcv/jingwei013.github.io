#!/bin/bash
# ==========================================
# 网站维护脚本 - 自动同步到 GitHub
# ==========================================
# 功能：将 website\ 的更新同步到 website-public\ 并推送到 GitHub
# 用途：每次其他小龙虾心跳完成后，自动维护网站
# ==========================================

set -e

echo "=========================================="
echo "网站维护自动化 - 开始同步"
echo "时间：$(date '+%Y-%m-%d %H:%M:%S')"
echo "=========================================="

# ==========================================
# 配置路径
# ==========================================
WEBSITE_SRC="D:/jingwei013/website"
WEBSITE_PUBLIC="D:/jingwei013/website-public"

echo ""
echo "📁 源目录: $WEBSITE_SRC"
echo "📁 公共目录: $WEBSITE_PUBLIC"

# ==========================================
# 1. 同步 index.html
# ==========================================
echo ""
echo "[1/6] 同步 index.html..."
if [ -f "$WEBSITE_SRC/index.html" ]; then
    cp "$WEBSITE_SRC/index.html" "$WEBSITE_PUBLIC/index.html"
    echo "✅ index.html 已复制"
else
    echo "⚠️  index.html 不存在，跳过"
fi

# ==========================================
# 2. 同步博客 HTML
# ==========================================
echo ""
echo "[2/6] 同步博客文件..."

# 统计同步数量
synced_count=0
skipped_count=0

for blog_file in "$WEBSITE_SRC/blog"/*.html; do
    if [ -f "$blog_file" ]; then
        filename=$(basename "$blog_file")
        dest="$WEBSITE_PUBLIC/blog/$filename"

        # 比较文件差异（避免重复复制）
        if [ ! -f "$dest" ] || [ "$blog_file" -nt "$dest" ]; then
            cp "$blog_file" "$dest"
            echo "  ✅ $filename"
            ((synced_count++))
        else
            ((skipped_count++))
        fi
    fi
done

echo "博客同步完成：新增/更新 $synced_count 个，跳过 $skipped_count 个"

# ==========================================
# 3. 同步样式文件（如果存在）
# ==========================================
echo ""
echo "[3/6] 同步样式文件..."

if [ -f "$WEBSITE_SRC/styles.css" ]; then
    cp "$WEBSITE_SRC/styles.css" "$WEBSITE_PUBLIC/styles.css"
    echo "✅ styles.css 已复制"
fi

if [ -d "$WEBSITE_SRC/css" ]; then
    cp -r "$WEBSITE_SRC/css"/* "$WEBSITE_PUBLIC/css/" 2>/dev/null || true
    echo "✅ css/ 目录已同步"
fi

# ==========================================
# 4. 统计网站数字一致性
# ==========================================
echo ""
echo "[4/6] 检查数字一致性..."

# 从 index.html 提取博客数
if grep -q "BLOG_POSTS" "$WEBSITE_PUBLIC/index.html"; then
    blog_count=$(grep -o '"title":' "$WEBSITE_PUBLIC/index.html" | wc -l)
    echo "  博客数: $blog_count"
fi

# 统计实际博客文件数
actual_blog_count=$(ls -1 "$WEBSITE_PUBLIC/blog"/*.html 2>/dev/null | wc -l)
echo "  实际博客文件: $actual_blog_count"

# 检查不一致
if [ "$blog_count" != "$actual_blog_count" ]; then
    echo "  ⚠️  警告：博客数不一致！"
else
    echo "  ✅ 博客数一致"
fi

# ==========================================
# 5. Git 操作
# ==========================================
echo ""
echo "[5/6] Git 操作..."

cd "$WEBSITE_PUBLIC"

# 检查是否有未提交的更改
if git diff --quiet && git diff --cached --quiet; then
    echo "⚠️  没有检测到更改，跳过 Git 提交"
else
    # 添加所有更改
    git add -A

    # 生成 commit 消息
    commit_time=$(date '+%Y-%m-%d %H:%M')
    commit_msg="网站更新 - $commit_time"
    if [ $synced_count -gt 0 ]; then
        commit_msg="$commit_msg (博客: +$synced_count)"
    fi

    # 提交
    git commit -m "$commit_msg"
    echo "✅ Git commit 完成: $commit_msg"

    # 推送到 GitHub
    echo "正在推送到 GitHub..."
    max_retries=3
    retry_count=0

    while [ $retry_count -lt $max_retries ]; do
        if git push origin main; then
            echo "✅ GitHub push 成功！"
            break
        else
            retry_count=$((retry_count + 1))
            echo "⚠️  GitHub push 失败，重试 $retry_count/$max_retries..."
            sleep 2
        fi
    done

    if [ $retry_count -eq $max_retries ]; then
        echo "❌ GitHub push 失败，已达到最大重试次数"
        echo "   请稍后手动执行: cd $WEBSITE_PUBLIC && git push origin main"
        exit 1
    fi
fi

# ==========================================
# 6. 生成维护报告
# ==========================================
echo ""
echo "[6/6] 生成维护报告..."

report_file="$WEBSITE_PUBLIC/maintenance_report.txt"

{
    echo "========================================"
    echo "网站维护报告"
    echo "========================================"
    echo "维护时间: $(date '+%Y-%m-%d %H:%M:%S')"
    echo ""
    echo "同步统计:"
    echo "  - 博客新增/更新: $synced_count"
    echo "  - 博客跳过: $skipped_count"
    echo "  - 总博客数: $actual_blog_count"
    echo ""
    echo "Git 状态:"
    git log -1 --oneline
    echo ""
    echo "========================================"
} > "$report_file"

echo "✅ 维护报告已生成: $report_file"

# ==========================================
# 完成
# ==========================================
echo ""
echo "=========================================="
echo "✅ 网站维护完成"
echo "=========================================="
echo ""
echo "📊 维护摘要:"
echo "  博客同步: $synced_count 个"
echo "  Git 推送: 成功"
echo "  在线地址: https://jingwei013.github.io/"
echo ""

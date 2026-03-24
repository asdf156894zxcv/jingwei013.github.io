# ============================================
# jingwei013.ai 自动更新 + 部署脚本
# 每天定时：检查论文更新 + 生成博客 + 推送网站
# ============================================

param(
    [string]$ArxivQuery = "embodied navigation OR vision language navigation OR robot navigation LLM",
    [int]$ArxivMaxResults = 5,
    [string]$BlogDate = ""
)

$ErrorActionPreference = "Continue"
$repo_dir = "D:\jingwei013\website-public"

# 时间设置
if (-not $BlogDate) {
    $BlogDate = Get-Date -Format "yyyy-MM-dd"
}

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "jingwei013.ai 自动更新脚本" -ForegroundColor Cyan
Write-Host "执行时间: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# ============================================
# 步骤1：进入工作目录
# ============================================
Set-Location $repo_dir

# 初始化 git（首次运行）
if (-not (Test-Path ".git")) {
    Write-Host "[步骤1] 初始化 Git 仓库..." -ForegroundColor Yellow
    git init
    git remote add origin https://github.com/Jingwei013/jingwei013.github.io.git
}

# 确保 remote 正确
$current_remote = git remote get-url origin 2>$null
if ($current_remote -ne "https://github.com/Jingwei013/jingwei013.github.io.git") {
    git remote set-url origin https://github.com/Jingwei013/jingwei013.github.io.git
}

# 拉取最新代码
Write-Host "[步骤1] 同步远程最新代码..." -ForegroundColor Yellow
git pull origin main --rebase 2>&1 | Out-Null

# ============================================
# 步骤2：读取当前网站内容
# ============================================
Write-Host "[步骤2] 读取当前网站数据..." -ForegroundColor Yellow
$html = Get-Content "$repo_dir\index.html" -Raw -Encoding UTF8

# ============================================
# 步骤3：检查 ArXiv 更新
# ============================================
Write-Host "[步骤3] 检查 ArXiv 最新论文..." -ForegroundColor Yellow
$arxiv_updated = $false
$new_papers_found = $false

try {
    # 调用 ArXiv API 搜索具身导航相关论文
    $search_query = $ArxivQuery -replace " ", "+"
    $arxiv_url = "https://export.arxiv.org/api/query?search_query=all:$search_query&start=0&max_results=$ArxivMaxResults&sortBy=submittedDate&sortOrder=descending"

    $response = Invoke-WebRequest -Uri $arxiv_url -TimeoutSec 30 -UseBasicParsing
    [xml]$xml = $response.Content

    $papers = @()
    foreach ($entry in $xml.feed.entry) {
        $title = $entry.title -replace "\s+", " "
        $summary = $entry.summary -replace "\s+", " "
        $authors = ($entry.author | Select-Object -First 3).name -join ", "
        $published = [datetime]$entry.published
        $arxiv_id = $entry.id -replace "http://arxiv.org/abs/", ""
        $pdf_url = "https://arxiv.org/pdf/$arxiv_id.pdf"
        $abs_url = "https://arxiv.org/abs/$arxiv_id"

        $papers += @{
            Title = $title.Trim()
            Summary = $summary.Trim()
            Authors = $authors
            Date = $published.ToString("yyyy-MM-dd")
            ArxivId = $arxiv_id
            PdfUrl = $pdf_url
            AbsUrl = $abs_url
        }
    }

    Write-Host "  发现 $($papers.Count) 篇最新论文" -ForegroundColor Green

    # 检查是否有今天或近3天内的新论文
    $recent_papers = $papers | Where-Object {
        $days_ago = ((Get-Date) - [datetime]$_.Date).Days
        $days_ago -le 3
    }

    if ($recent_papers.Count -gt 0) {
        Write-Host "  有 $($recent_papers.Count) 篇新论文（3天内）" -ForegroundColor Green
        $new_papers_found = $true
        $arxiv_updated = $true
    } else {
        Write-Host "  近3天无新论文，跳过更新" -ForegroundColor Gray
    }

} catch {
    Write-Host "  ArXiv 检查失败: $_" -ForegroundColor Red
    Write-Host "  继续执行其他更新步骤..." -ForegroundColor Gray
}

# ============================================
# 步骤4：生成今日研究日志
# ============================================
Write-Host "[步骤4] 生成今日研究日志..." -ForegroundColor Yellow
$blog_html = ""

if ($new_papers_found -and $recent_papers) {
    # 生成论文更新日志
    $paper_titles = ($recent_papers | Select-Object -First 3).Title -join "、"
    $blog_html = @"
        <div class="blog-card" onclick="this.classList.toggle('expanded')">
            <div class="blog-meta">$BlogDate · 论文追踪</div>
            <h3>具身导航论文更新｜今日发现 $($recent_papers.Count) 篇</h3>
            <p>今日追踪到近期具身导航领域新论文，主要涉及：$paper_titles。</p>
            <div class="blog-tags"><span>论文</span><span>ArXiv</span><span>具身导航</span></div>
        </div>
"@
}

if (-not $blog_html) {
    # 生成常规日志
    $day_of_week = (Get-Date).DayOfWeek
    $week_note = switch ($day_of_week) {
        'Monday'    { "新的一周，开始系统性论文阅读" }
        'Tuesday'   { "继续深入研究方向" }
        'Wednesday' { "研究进展梳理，本周重点推进" }
        'Thursday'  { "论文复现与实验设计" }
        'Friday'    { "周末前整理本周成果" }
        'Saturday'  { "独立研究与深度思考时间" }
        'Sunday'    { "知识沉淀与下周规划" }
    }

    $blog_html = @"
        <div class="blog-card" onclick="this.classList.toggle('expanded')">
            <div class="blog-meta">$BlogDate · 研究日志</div>
            <h3>每日研究记录</h3>
            <p>$week_note。持续聚焦 VLN 视觉语言导航与 LLM 赋能导航方向，关注近期 ArXiv 动态。</p>
            <div class="blog-tags"><span>日常</span><span>研究</span></div>
        </div>
"@
}

# 更新 index.html 中的博客部分
if ($html -match '<!-- 博客开始 -->[\s\S]*?<!-- 博客结束 -->') {
    $pattern = '<!-- 博客开始 -->[\s\S]*?<!-- 博客结束 -->'
    $replacement = "<!-- 博客开始 -->" + $blog_html + "`n        <!-- 博客结束 -->"
    $html = $html -replace $pattern, $replacement
    $arxiv_updated = $true
    Write-Host "  博客更新完成" -ForegroundColor Green
}

# ============================================
# 步骤5：保存更新
# ============================================
$change_made = $false
if ($arxiv_updated) {
    Write-Host "[步骤5] 保存网站更新..." -ForegroundColor Yellow
    # 使用 UTF-8 BOM 保存（兼容更多编辑器）
    $utf8_bom = New-Object System.Text.UTF8Encoding $true
    [System.IO.File]::WriteAllText("$repo_dir\index.html", $html, $utf8_bom)
    $change_made = $true
} else {
    Write-Host "[步骤5] 无新内容，跳过保存" -ForegroundColor Gray
}

# ============================================
# 步骤6：推送到 GitHub
# ============================================
Write-Host "[步骤6] 推送到 GitHub..." -ForegroundColor Yellow
git add .

$status = git status --porcelain
if ($status) {
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm"
    $commit_msg = "Auto-update: $timestamp"

    git commit -m $commit_msg

    try {
        git push origin main 2>&1
        Write-Host ""
        Write-Host "========================================" -ForegroundColor Green
        Write-Host "[完成] 网站已更新并推送！" -ForegroundColor Green
        Write-Host "在线地址: https://jingwei013.github.io/jingwei013.github.io/" -ForegroundColor Green
        Write-Host "生效时间: 约 1-2 分钟后" -ForegroundColor Gray
        Write-Host "========================================" -ForegroundColor Green
    } catch {
        Write-Host "[错误] 推送失败: $_" -ForegroundColor Red
        Write-Host "请检查网络连接和 GitHub 认证状态" -ForegroundColor Yellow
    }
} else {
    Write-Host "[检查] 今日无新内容，无需推送。" -ForegroundColor Green
}

# ==========================================
# 网站维护脚本 - PowerShell 版本
# ==========================================
# 功能：将 website\ 的更新同步到 website-public\ 并推送到 GitHub
# 用途：每次其他小龙虾心跳完成后，自动维护网站
# ==========================================

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "网站维护自动化 - 开始同步" -ForegroundColor Cyan
Write-Host "时间：$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')" -ForegroundColor Gray
Write-Host "==========================================" -ForegroundColor Cyan

# ==========================================
# 配置路径
# ==========================================
$WEBSITE_SRC = "D:\jingwei013\website"
$WEBSITE_PUBLIC = "D:\jingwei013\website-public"

Write-Host ""
Write-Host "📁 源目录: $WEBSITE_SRC" -ForegroundColor Yellow
Write-Host "📁 公共目录: $WEBSITE_PUBLIC" -ForegroundColor Yellow

# ==========================================
# 1. 同步 index.html
# ==========================================
Write-Host ""
Write-Host "[1/6] 同步 index.html..." -ForegroundColor Cyan

$srcIndex = "$WEBSITE_SRC\index.html"
$destIndex = "$WEBSITE_PUBLIC\index.html"

if (Test-Path $srcIndex) {
    Copy-Item -Path $srcIndex -Destination $destIndex -Force
    Write-Host "✅ index.html 已复制" -ForegroundColor Green
} else {
    Write-Host "⚠️  index.html 不存在，跳过" -ForegroundColor Yellow
}

# ==========================================
# 2. 同步博客 HTML
# ==========================================
Write-Host ""
Write-Host "[2/6] 同步博客文件..." -ForegroundColor Cyan

$srcBlogDir = "$WEBSITE_SRC\blog"
$destBlogDir = "$WEBSITE_PUBLIC\blog"

$syncedCount = 0
$skippedCount = 0

if (Test-Path $srcBlogDir) {
    if (-not (Test-Path $destBlogDir)) {
        New-Item -ItemType Directory -Path $destBlogDir -Force | Out-Null
    }

    $blogFiles = Get-ChildItem -Path $srcBlogDir -Filter "*.html"

    foreach ($blogFile in $blogFiles) {
        $destFile = Join-Path $destBlogDir $blogFile.Name

        # 检查是否需要复制（文件不存在或源文件更新）
        if (-not (Test-Path $destFile) -or ($blogFile.LastWriteTime -gt (Get-Item $destFile).LastWriteTime)) {
            Copy-Item -Path $blogFile.FullName -Destination $destFile -Force
            Write-Host "  ✅ $($blogFile.Name)" -ForegroundColor Green
            $syncedCount++
        } else {
            $skippedCount++
        }
    }

    Write-Host "博客同步完成：新增/更新 $syncedCount 个，跳过 $skippedCount 个" -ForegroundColor Cyan
} else {
    Write-Host "⚠️  blog 目录不存在" -ForegroundColor Yellow
}

# ==========================================
# 3. 同步样式文件
# ==========================================
Write-Host ""
Write-Host "[3/6] 同步样式文件..." -ForegroundColor Cyan

$stylesSrc = "$WEBSITE_SRC\styles.css"
$stylesDest = "$WEBSITE_PUBLIC\styles.css"

if (Test-Path $stylesSrc) {
    Copy-Item -Path $stylesSrc -Destination $stylesDest -Force
    Write-Host "✅ styles.css 已复制" -ForegroundColor Green
}

$cssSrcDir = "$WEBSITE_SRC\css"
$cssDestDir = "$WEBSITE_PUBLIC\css"

if (Test-Path $cssSrcDir) {
    if (-not (Test-Path $cssDestDir)) {
        New-Item -ItemType Directory -Path $cssDestDir -Force | Out-Null
    }
    Copy-Item -Path "$cssSrcDir\*" -Destination $cssDestDir -Recurse -Force
    Write-Host "✅ css/ 目录已同步" -ForegroundColor Green
}

# ==========================================
# 4. 统计网站数字一致性
# ==========================================
Write-Host ""
Write-Host "[4/6] 检查数字一致性..." -ForegroundColor Cyan

# 从 index.html 提取博客数
$indexContent = Get-Content $destIndex -Raw -Encoding UTF8
$blogMatches = [regex]::Matches($indexContent, '"title":')
$blogCount = $blogMatches.Count
Write-Host "  博客数: $blogCount" -ForegroundColor White

# 统计实际博客文件数
$actualBlogFiles = Get-ChildItem -Path $destBlogDir -Filter "*.html" -ErrorAction SilentlyContinue
$actualBlogCount = $actualBlogFiles.Count
Write-Host "  实际博客文件: $actualBlogCount" -ForegroundColor White

if ($blogCount -ne $actualBlogCount) {
    Write-Host "  ⚠️  警告：博客数不一致！" -ForegroundColor Red
} else {
    Write-Host "  ✅ 博客数一致" -ForegroundColor Green
}

# ==========================================
# 5. Git 操作
# ==========================================
Write-Host ""
Write-Host "[5/6] Git 操作..." -ForegroundColor Cyan

Set-Location $WEBSITE_PUBLIC

# 检查是否有未提交的更改
$gitStatus = git status --porcelain

if ([string]::IsNullOrWhiteSpace($gitStatus)) {
    Write-Host "⚠️  没有检测到更改，跳过 Git 提交" -ForegroundColor Yellow
} else {
    # 添加所有更改
    git add -A

    # 生成 commit 消息
    $commitTime = Get-Date -Format "yyyy-MM-dd HH:mm"
    $commitMsg = "网站更新 - $commitTime"
    if ($syncedCount -gt 0) {
        $commitMsg = "$commitMsg (博客: +$syncedCount)"
    }

    # 提交
    git commit -m $commitMsg
    Write-Host "✅ Git commit 完成: $commitMsg" -ForegroundColor Green

    # 推送到 GitHub
    Write-Host "正在推送到 GitHub..." -ForegroundColor Cyan

    $maxRetries = 3
    $retryCount = 0
    $pushSuccess = $false

    while ($retryCount -lt $maxRetries -and -not $pushSuccess) {
        try {
            $result = git push origin main 2>&1
            if ($LASTEXITCODE -eq 0) {
                Write-Host "✅ GitHub push 成功！" -ForegroundColor Green
                $pushSuccess = $true
            } else {
                throw "Git push failed"
            }
        } catch {
            $retryCount++
            Write-Host "⚠️  GitHub push 失败，重试 $retryCount/$maxRetries..." -ForegroundColor Yellow
            Start-Sleep -Seconds 2
        }
    }

    if (-not $pushSuccess) {
        Write-Host "❌ GitHub push 失败，已达到最大重试次数" -ForegroundColor Red
        Write-Host "   请稍后手动执行: cd $WEBSITE_PUBLIC && git push origin main" -ForegroundColor Yellow
        exit 1
    }
}

# ==========================================
# 6. 生成维护报告
# ==========================================
Write-Host ""
Write-Host "[6/6] 生成维护报告..." -ForegroundColor Cyan

$reportFile = "$WEBSITE_PUBLIC\maintenance_report.txt"

$reportContent = @"
========================================
网站维护报告
========================================
维护时间: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')

同步统计:
  - 博客新增/更新: $syncedCount
  - 博客跳过: $skippedCount
  - 总博客数: $actualBlogCount

Git 状态:
$(git log -1 --oneline)

========================================
"@

Set-Content -Path $reportFile -Value $reportContent -Encoding UTF8

Write-Host "✅ 维护报告已生成: $reportFile" -ForegroundColor Green

# ==========================================
# 完成
# ==========================================
Write-Host ""
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "✅ 网站维护完成" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "📊 维护摘要:" -ForegroundColor Cyan
Write-Host "  博客同步: $syncedCount 个" -ForegroundColor White
Write-Host "  Git 推送: 成功" -ForegroundColor Green
Write-Host "  在线地址: https://jingwei013.github.io/" -ForegroundColor Cyan
Write-Host ""

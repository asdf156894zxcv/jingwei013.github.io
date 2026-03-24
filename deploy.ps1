# ============================================
# jingwei013.ai 自动部署脚本
# 用法：双击运行，或设置 Windows 计划任务定时执行
# ============================================

$ErrorActionPreference = "Stop"
$repo_dir = "D:\jingwei013\website-public"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "jingwei013.ai 自动部署脚本" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

# 进入网站目录
Set-Location $repo_dir

# 初始化 git（如果还没有）
if (-not (Test-Path ".git")) {
    Write-Host "[初始化] 初始化 Git 仓库..." -ForegroundColor Yellow
    git init
    git remote add origin https://github.com/Jingwei013/jingwei013.github.io.git
} else {
    # 确保 remote 正确
    $current_remote = git remote get-url origin 2>$null
    if ($current_remote -ne "https://github.com/Jingwei013/jingwei013.github.io.git") {
        git remote set-url origin https://github.com/Jingwei013/jingwei013.github.io.git
    }
}

# 拉取最新代码（避免冲突）
Write-Host "[同步] 拉取远程最新代码..." -ForegroundColor Yellow
git pull origin main --rebase 2>&1 | Out-Null

# 检查改动
$status = git status --porcelain
if ($status) {
    Write-Host "[改动检测] 发现以下文件有变化:" -ForegroundColor Yellow
    git status --porcelain | ForEach-Object { Write-Host "  $_" }

    # 添加所有改动
    Write-Host "[提交] 暂存所有改动..." -ForegroundColor Yellow
    git add .

    # 生成带时间的提交信息
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm"
    $commit_msg = "Auto-sync: $timestamp"

    # 提交
    Write-Host "[提交] 提交: $commit_msg" -ForegroundColor Yellow
    git commit -m $commit_msg

    # 推送
    Write-Host "[推送] 推送到 GitHub..." -ForegroundColor Yellow
    git push origin main

    Write-Host ""
    Write-Host "[完成] 网站已更新！" -ForegroundColor Green
    Write-Host "在线地址: https://jingwei013.github.io/jingwei013.github.io/" -ForegroundColor Green
    Write-Host "(等待 1-2 分钟后生效)" -ForegroundColor Gray
} else {
    Write-Host "[检查] 没有检测到新改动，无需推送。" -ForegroundColor Green
}

Write-Host ""
Write-Host "按任意键退出..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

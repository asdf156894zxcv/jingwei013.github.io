#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ==========================================
# 网站维护脚本 - Python 版本
# ==========================================
# 功能：将 website\ 的更新同步到 website-public\ 并推送到 GitHub
# 用途：每次其他小龙虾心跳完成后，自动维护网站
# ==========================================

import os
import shutil
import subprocess
import json
from datetime import datetime
from pathlib import Path

print("=" * 50)
print("网站维护自动化 - 开始同步")
print(f"时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("=" * 50)

# ==========================================
# 配置路径
# ==========================================
WEBSITE_SRC = r"D:\jingwei013\website"
WEBSITE_PUBLIC = r"D:\jingwei013\website-public"

print(f"\n📁 源目录: {WEBSITE_SRC}")
print(f"📁 公共目录: {WEBSITE_PUBLIC}")

# ==========================================
# 1. 同步 index.html
# ==========================================
print("\n[1/6] 同步 index.html...")

src_index = os.path.join(WEBSITE_SRC, "index.html")
dest_index = os.path.join(WEBSITE_PUBLIC, "index.html")

if os.path.exists(src_index):
    shutil.copy2(src_index, dest_index)
    print("✅ index.html 已复制")
else:
    print("⚠️  index.html 不存在，跳过")

# ==========================================
# 2. 同步博客 HTML
# ==========================================
print("\n[2/6] 同步博客文件...")

src_blog_dir = os.path.join(WEBSITE_SRC, "blog")
dest_blog_dir = os.path.join(WEBSITE_PUBLIC, "blog")

synced_count = 0
skipped_count = 0

if os.path.exists(src_blog_dir):
    os.makedirs(dest_blog_dir, exist_ok=True)

    for blog_file in os.listdir(src_blog_dir):
        if blog_file.endswith('.html'):
            src_file = os.path.join(src_blog_dir, blog_file)
            dest_file = os.path.join(dest_blog_dir, blog_file)

            # 检查是否需要复制
            should_copy = False
            if not os.path.exists(dest_file):
                should_copy = True
            else:
                src_time = os.path.getmtime(src_file)
                dest_time = os.path.getmtime(dest_file)
                if src_time > dest_time:
                    should_copy = True

            if should_copy:
                shutil.copy2(src_file, dest_file)
                print(f"  ✅ {blog_file}")
                synced_count += 1
            else:
                skipped_count += 1

    print(f"博客同步完成：新增/更新 {synced_count} 个，跳过 {skipped_count} 个")
else:
    print("⚠️  blog 目录不存在")

# ==========================================
# 3. 同步样式文件
# ==========================================
print("\n[3/6] 同步样式文件...")

styles_src = os.path.join(WEBSITE_SRC, "styles.css")
styles_dest = os.path.join(WEBSITE_PUBLIC, "styles.css")

if os.path.exists(styles_src):
    shutil.copy2(styles_src, styles_dest)
    print("✅ styles.css 已复制")

css_src_dir = os.path.join(WEBSITE_SRC, "css")
css_dest_dir = os.path.join(WEBSITE_PUBLIC, "css")

if os.path.exists(css_src_dir):
    os.makedirs(css_dest_dir, exist_ok=True)
    for item in os.listdir(css_src_dir):
        src_item = os.path.join(css_src_dir, item)
        dest_item = os.path.join(css_dest_dir, item)

        if os.path.isfile(src_item):
            shutil.copy2(src_item, dest_item)
        else:
            if os.path.exists(dest_item):
                shutil.rmtree(dest_item)
            shutil.copytree(src_item, dest_item)

    print("✅ css/ 目录已同步")

# ==========================================
# 4. 统计网站数字一致性
# ==========================================
print("\n[4/6] 检查数字一致性...")

# 从 index.html 提取博客数
with open(dest_index, 'r', encoding='utf-8') as f:
    content = f.read()
    blog_count = content.count('"title":')

print(f"  博客数: {blog_count}")

# 统计实际博客文件数
actual_blog_files = [f for f in os.listdir(dest_blog_dir) if f.endswith('.html')]
actual_blog_count = len(actual_blog_files)

print(f"  实际博客文件: {actual_blog_count}")

if blog_count != actual_blog_count:
    print("  ⚠️  警告：博客数不一致！")
else:
    print("  ✅ 博客数一致")

# ==========================================
# 5. Git 操作
# ==========================================
print("\n[5/6] Git 操作...")

os.chdir(WEBSITE_PUBLIC)

# 检查是否有未提交的更改
result = subprocess.run(['git', 'status', '--porcelain'],
                      capture_output=True, text=True)

if not result.stdout.strip():
    print("⚠️  没有检测到更改，跳过 Git 提交")
else:
    # 添加所有更改
    subprocess.run(['git', 'add', '-A'], check=True)

    # 生成 commit 消息
    commit_time = datetime.now().strftime('%Y-%m-%d %H:%M')
    commit_msg = f"网站更新 - {commit_time}"
    if synced_count > 0:
        commit_msg += f" (博客: +{synced_count})"

    # 提交
    subprocess.run(['git', 'commit', '-m', commit_msg], check=True)
    print(f"✅ Git commit 完成: {commit_msg}")

    # 推送到 GitHub
    print("正在推送到 GitHub...")

    max_retries = 3
    retry_count = 0
    push_success = False

    while retry_count < max_retries and not push_success:
        try:
            result = subprocess.run(['git', 'push', 'origin', 'main'],
                                  capture_output=True, text=True, check=True)
            print("✅ GitHub push 成功！")
            push_success = True
        except subprocess.CalledProcessError:
            retry_count += 1
            print(f"⚠️  GitHub push 失败，重试 {retry_count}/{max_retries}...")
            import time
            time.sleep(2)

    if not push_success:
        print("❌ GitHub push 失败，已达到最大重试次数")
        print(f"   请稍后手动执行: cd {WEBSITE_PUBLIC} && git push origin main")
        exit(1)

# ==========================================
# 6. 生成维护报告
# ==========================================
print("\n[6/6] 生成维护报告...")

report_file = os.path.join(WEBSITE_PUBLIC, "maintenance_report.txt")

# 获取最新的 commit 信息
result = subprocess.run(['git', 'log', '-1', '--oneline'],
                      capture_output=True, text=True)
latest_commit = result.stdout.strip()

report_content = f"""========================================
网站维护报告
========================================
维护时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

同步统计:
  - 博客新增/更新: {synced_count}
  - 博客跳过: {skipped_count}
  - 总博客数: {actual_blog_count}

Git 状态:
{latest_commit}

========================================
"""

with open(report_file, 'w', encoding='utf-8') as f:
    f.write(report_content)

print(f"[OK] 维护报告已生成: {report_file}")

# ==========================================
# 完成
# ==========================================
print("\n" + "=" * 50)
print("[OK] 网站维护完成")
print("=" * 50)
print("\n[SUMMARY] 维护摘要:")
print(f"  博客同步: {synced_count} 个")
print("  Git 推送: 成功")
print("  在线地址: https://jingwei013.github.io/")
print()

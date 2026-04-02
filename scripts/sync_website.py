#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ==========================================
# Website Maintenance Script - Python Version
# ==========================================
# Function: Sync website\ to website-public\ and push to GitHub
# Usage: Run after each heartbeat completion
# ==========================================

import os
import shutil
import subprocess
from datetime import datetime
import sys

# Set UTF-8 encoding for output
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

print("=" * 50)
print("Website Maintenance - Starting Sync")
print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("=" * 50)

# ==========================================
# Configuration
# ==========================================
WEBSITE_SRC = r"D:\jingwei013\website"
WEBSITE_PUBLIC = r"D:\jingwei013\website-public"

print(f"\n[SRC] Source: {WEBSITE_SRC}")
print(f"[PUB] Public: {WEBSITE_PUBLIC}")

# ==========================================
# 1. Sync index.html
# ==========================================
print("\n[1/6] Syncing index.html...")

src_index = os.path.join(WEBSITE_SRC, "index.html")
dest_index = os.path.join(WEBSITE_PUBLIC, "index.html")

if os.path.exists(src_index):
    shutil.copy2(src_index, dest_index)
    print("[OK] index.html copied")
else:
    print("[SKIP] index.html not found")

# ==========================================
# 2. Sync blog HTML files
# ==========================================
print("\n[2/6] Syncing blog files...")

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
                print(f"  [SYNC] {blog_file}")
                synced_count += 1
            else:
                skipped_count += 1

    print(f"Blog sync: +{synced_count} new/updated, {skipped_count} skipped")
else:
    print("[SKIP] blog directory not found")

# ==========================================
# 3. Sync style files
# ==========================================
print("\n[3/6] Syncing style files...")

styles_src = os.path.join(WEBSITE_SRC, "styles.css")
styles_dest = os.path.join(WEBSITE_PUBLIC, "styles.css")

if os.path.exists(styles_src):
    shutil.copy2(styles_src, styles_dest)
    print("[OK] styles.css copied")

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

    print("[OK] css/ directory synced")

# ==========================================
# 4. Check number consistency
# ==========================================
print("\n[4/6] Checking number consistency...")

with open(dest_index, 'r', encoding='utf-8') as f:
    content = f.read()
    blog_count = content.count('"title":')

print(f"  Blog count: {blog_count}")

actual_blog_files = [f for f in os.listdir(dest_blog_dir) if f.endswith('.html')]
actual_blog_count = len(actual_blog_files)

print(f"  Actual blog files: {actual_blog_count}")

if blog_count != actual_blog_count:
    print("  [WARN] Blog count mismatch!")
else:
    print("  [OK] Blog count matches")

# ==========================================
# 5. Git operations
# ==========================================
print("\n[5/6] Git operations...")

os.chdir(WEBSITE_PUBLIC)

# Check for uncommitted changes
result = subprocess.run(['git', 'status', '--porcelain'],
                      capture_output=True, text=True)

if not result.stdout.strip():
    print("[SKIP] No changes detected")
else:
    # Stage all changes
    subprocess.run(['git', 'add', '-A'], check=True)

    # Generate commit message
    commit_time = datetime.now().strftime('%Y-%m-%d %H:%M')
    commit_msg = f"Website update - {commit_time}"
    if synced_count > 0:
        commit_msg += f" (blogs: +{synced_count})"

    # Commit
    subprocess.run(['git', 'commit', '-m', commit_msg], check=True)
    print(f"[OK] Git commit: {commit_msg}")

    # Push to GitHub
    print("Pushing to GitHub...")

    max_retries = 3
    retry_count = 0
    push_success = False

    while retry_count < max_retries and not push_success:
        try:
            result = subprocess.run(['git', 'push', 'origin', 'main'],
                                  capture_output=True, text=True, check=True)
            print("[OK] GitHub push successful!")
            push_success = True
        except subprocess.CalledProcessError:
            retry_count += 1
            print(f"[RETRY] Push failed, retry {retry_count}/{max_retries}...")
            import time
            time.sleep(2)

    if not push_success:
        print("[ERROR] GitHub push failed after max retries")
        print(f"   Manual: cd {WEBSITE_PUBLIC} && git push origin main")
        exit(1)

# ==========================================
# 6. Generate maintenance report
# ==========================================
print("\n[6/6] Generating report...")

report_file = os.path.join(WEBSITE_PUBLIC, "maintenance_report.txt")

result = subprocess.run(['git', 'log', '-1', '--oneline'],
                      capture_output=True, text=True)
latest_commit = result.stdout.strip()

report_content = f"""========================================
Maintenance Report
========================================
Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Sync stats:
  - Blogs synced: {synced_count}
  - Blogs skipped: {skipped_count}
  - Total blogs: {actual_blog_count}

Git status:
{latest_commit}

========================================
"""

with open(report_file, 'w', encoding='utf-8') as f:
    f.write(report_content)

print(f"[OK] Report generated: {report_file}")

# ==========================================
# Done
# ==========================================
print("\n" + "=" * 50)
print("[OK] Website maintenance complete")
print("=" * 50)
print("\n[SUMMARY]")
print(f"  Blogs synced: {synced_count}")
print("  Git push: successful")
print("  Live: https://jingwei013.github.io/")
print()

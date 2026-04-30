# -*- coding: utf-8 -*-
"""
网站索引生成器 v2.0
- 扫描博客和案例目录
- 生成完整的新index.html
- 修复所有链接问题
"""
import os
import re
from datetime import datetime

# 配置
BLOG_DIR = "blog"
CASES_DIR = "cases"
OUTPUT_FILE = "index_new.html"

# 读取博客文件
blogs = []
if os.path.exists(BLOG_DIR):
    for f in sorted(os.listdir(BLOG_DIR), reverse=True):
        if f.endswith('.html'):
            # 解析标题和分类
            filepath = os.path.join(BLOG_DIR, f)
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as file:
                content = file.read(2000)
            
            # 提取标题
            title_match = re.search(r'<title>(.*?)</title>', content, re.I)
            title = title_match.group(1) if title_match else f.replace('.html', '')
            
            # 提取分类标签
            tags = []
            if 'vln' in title.lower() or 'vision-language' in title.lower(): 
                tags.append('VLN')
            if 'slam' in title.lower(): 
                tags.append('SLAM')
            if 'startup' in title.lower() or '创业' in title:
                tags.append('创业')
            if 'ai' in title.lower() and ('startup' in title.lower() or '创业' in title):
                tags.append('AI创业')
            if 'vla' in title.lower():
                tags.append('VLA')
            if 'world-model' in title.lower() or '世界模型' in title:
                tags.append('世界模型')
            if 'embodied' in title.lower() or '具身' in title:
                tags.append('具身智能')
            if 'robot' in title.lower() or '机器人' in title:
                tags.append('机器人')
            if not tags:
                if 'case' in f.lower() or '案例' in title:
                    tags.append('案例分析')
                else:
                    tags.append('技术深度')
            
            # 提取日期
            date_match = re.search(r'(\d{4}-\d{2}-\d{2})', f)
            date = date_match.group(1) if date_match else '2026-01-01'
            
            blogs.append({
                'title': title[:80],
                'url': f'./blog/{f}',
                'date': date,
                'tags': tags[:3],
                'name': f
            })

# 读取案例文件
cases = []
if os.path.exists(CASES_DIR):
    for f in sorted(os.listdir(CASES_DIR), reverse=True):
        if f.endswith('.md'):
            filepath = os.path.join(CASES_DIR, f)
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as file:
                content = file.read(3000)
            
            # 提取标题
            lines = content.split('\n')
            title = f.replace('.md', '').replace('-', ' ')
            for line in lines[:10]:
                if line.startswith('#'):
                    title = line.lstrip('#* ').strip()
                    break
            
            # 提取分类
            tags = []
            if any(x in title.lower() for x in ['failure', 'bankruptcy', 'collapse', 'death', '倒闭', '破产', '失败']):
                tags.append('失败')
            elif any(x in title.lower() for x in ['billion', 'funding', 'series', '独角兽', '融资', '成功']):
                tags.append('成功')
            else:
                tags.append('分析')
            
            if 'robot' in title.lower() or '机器人' in title:
                tags.append('机器人')
            if 'embodied' in title.lower() or '具身' in title:
                tags.append('具身智能')
            if 'ai' in title.lower():
                tags.append('AI')
            
            # 提取日期
            date_match = re.search(r'(\d{4}-\d{2}-\d{2})', content[:500])
            date = date_match.group(1) if date_match else '2026-01-01'
            
            # 提取摘要
            excerpt = ''
            for line in lines[10:30]:
                if line and len(line) > 20 and not line.startswith('#'):
                    excerpt = line.strip()[:100]
                    break
            
            cases.append({
                'title': title[:80],
                'url': f'./cases/{f}',
                'date': date,
                'tags': tags[:3],
                'excerpt': excerpt
            })

print(f"扫描完成: {len(blogs)} 博客, {len(cases)} 案例")
print(f"博客示例: {blogs[0]['title'] if blogs else 'N/A'}")
print(f"案例示例: {cases[0]['title'] if cases else 'N/A'}")

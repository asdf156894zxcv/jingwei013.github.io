# -*- coding: utf-8 -*-
import urllib.request
import os

def check_and_fix_blog(url, local_path):
    """Download, check encoding, fix, and save"""
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        resp = urllib.request.urlopen(req, timeout=15)
        data = resp.read()
        ct = resp.headers.get("Content-Type", "")

        # Check if contains GBK Chinese
        gbk_chinese = b'\xbe\xab'  # First byte of GBK '精'
        is_gbk = gbk_chinese in data[:500]

        if is_gbk:
            print(f'FIXING: {url}')
            text = data.decode('gbk', errors='replace')
            fixed = text.encode('utf-8', errors='replace')
            with open(local_path, 'wb') as f:
                f.write(fixed)
            print(f'  -> Saved as UTF-8 ({len(fixed)} bytes)')
        else:
            print(f'OK: {url} (already UTF-8 or ASCII, {len(data)} bytes)')
    except Exception as e:
        print(f'ERROR: {url} -> {e}')

# Fix all blog files
blog_files = [
    ('embodied-slam-basics.html', 'blog/embodied-slam-basics.html'),
    ('vision-language-geometry-fusion.html', 'blog/vision-language-geometry-fusion.html'),
    ('spatiotemporal-memory-map.html', 'blog/spatiotemporal-memory-map.html'),
]

base_url = 'https://jingwei013.github.io/'
base_dir = r'D:\jingwei013\website-public'

for slug, rel_path in blog_files:
    url = base_url + slug
    local = os.path.join(base_dir, rel_path)
    check_and_fix_blog(url, local)

print('\nDone!')

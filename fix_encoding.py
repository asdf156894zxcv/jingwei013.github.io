# -*- coding: utf-8 -*-
import urllib.request

# Download raw bytes
req = urllib.request.Request('https://jingwei013.github.io/', headers={'User-Agent': 'Mozilla/5.0'})
resp = urllib.request.urlopen(req, timeout=15)
data = resp.read()
print(f'Downloaded {len(data)} bytes')
print(f'Content-Type: {resp.headers.get("Content-Type")}')

# Title area bytes (around pos 155)
title_bytes = data[155:200]
print(f'Title area hex: {title_bytes.hex()}')

# The content claims charset=utf-8 but is actually GBK
# Let's verify by checking the title
# In GBK: 精卫导航 = be ab ce c0 b5 bc ba bd
# In UTF-8: 精卫导航 = e7 b2 be e5 8d ab e5 af bc e6 8e a5

# If the bytes match GBK but not UTF-8 → confirm it's GBK
test_gbk = bytes.fromhex('beabcec0b5bcbabd')
test_utf8 = '精卫导航'.encode('utf-8')
print(f'Expected GBK bytes: {test_gbk.hex()}')
print(f'Expected UTF-8 bytes: {test_utf8.hex()}')

# Check if GBK title exists in data
if test_gbk in data:
    print('CONFIRMED: File contains GBK-encoded Chinese (not UTF-8)')
    # Convert: interpret as GBK, output as UTF-8
    text = data.decode('gbk', errors='replace')
    fixed = text.encode('utf-8', errors='replace')
    print(f'Fixed size: {len(fixed)} bytes')

    # Verify
    for line in fixed.decode('utf-8').split('\n'):
        if b'<title>' in line.encode('utf-8'):
            print(f'Fixed title: {line.strip()[:80]}')
            break

    # Save
    with open(r'D:\jingwei013\website-public\index.html', 'wb') as f:
        f.write(fixed)
    print('Saved!')

    # Also download and fix blog files
    fix_blog(r'https://jingwei013.github.io/blog/embodied-slam-basics.html',
             r'D:\jingwei013\website-public\blog\embodied-slam-basics.html')
else:
    print('Not found as GBK in data')

def fix_blog(url, local_path):
    """Check and fix a blog file if needed"""
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        resp = urllib.request.urlopen(req, timeout=10)
        data = resp.read()
        print(f'\nBlog: {url}')
        print(f'  Content-Type: {resp.headers.get("Content-Type")}')
        print(f'  Size: {len(data)} bytes')

        # Check title area
        if len(data) > 200:
            title_area = data[155:200]
            test_gbk = '精卫'.encode('gbk')
            if test_gbk in title_area:
                print(f'  -> GBK encoding detected, fixing...')
                text = data.decode('gbk', errors='replace')
                fixed = text.encode('utf-8', errors='replace')
                with open(local_path, 'wb') as f:
                    f.write(fixed)
                print(f'  -> Fixed and saved')
            else:
                print(f'  -> Looks OK (not GBK)')
    except Exception as e:
        print(f'  -> Error: {e}')

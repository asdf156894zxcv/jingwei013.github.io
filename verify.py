with open('index.html', 'r', encoding='utf-8') as f:
    c = f.read()
checks = ['section-title', 'papersTimeline', 'blogList', 'research-grid', 'timeline', 'paper-filters', 'blog-filters']
for ch in checks:
    found = ch in c
    status = 'OK' if found else 'MISSING'
    print(f'  {ch}: {status}')
print(f'Total size: {len(c)} chars')
fffd = c.count('\ufffd')
print(f'U+FFFD count: {fffd}')

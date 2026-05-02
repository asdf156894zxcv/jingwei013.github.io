import os, glob, chardet

# 先检测所有问题文件的实际编码
problem_files = [
    '404.html',
    'blog\\ai-hardware-startup-crisis-2026.html',
    'blog\\embodied-ai-april-27-funding-earthquake-day.html',
    'blog\\embodied-intelligence-q1-2026-funding-boom-analysis.html',
    'blog\\fscot-vs-fantasyvln-vln-cot-2026.html',
    'blog\\sim2real-gap-vln-2026.html',
    'blog\\vln-startup-ai-navigation-market-2026.html',
    'blog\\wmpo-meets-cow-nav-world-model-stop-decision-2026.html',
    'blog\\wmpo-world-model-vln-stop-decision-2026.html',
    'blog\\case-38-unitree-robotics.html',
    'styles.css',
    'PROGRESS.md',
    'README.md',
]

print("=== 检测编码 ===")
for f in problem_files:
    if not os.path.exists(f):
        print(f'SKIP: {f}')
        continue
    with open(f, 'rb') as file:
        raw = file.read()
    result = chardet.detect(raw)
    conf = result.get('confidence', 0)
    encoding = result.get('encoding', 'unknown')
    print(f'{encoding} ({conf:.2f}): {f}')
    
    # 如果是GBK且置信度高，尝试转换
    if encoding in ('GB2312', 'GB18030', 'windows-1252') and conf > 0.7:
        try:
            content = raw.decode('gbk')
            # 验证是否有合理的中文内容
            chinese_count = sum(1 for c in content if '\u4e00' <= c <= '\u9fff')
            latin_count = sum(1 for c in content if c.isalpha() and not '\u4e00' <= c <= '\u9fff')
            if chinese_count > 10:
                print(f'  -> {chinese_count} Chinese, {latin_count} Latin -> converting to UTF-8')
                with open(f, 'w', encoding='utf-8') as file:
                    file.write(content)
                print(f'  FIXED: {f}')
        except Exception as e:
            print(f'  GBK decode failed: {e}')
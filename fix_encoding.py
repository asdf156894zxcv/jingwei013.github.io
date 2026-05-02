import os, glob, re

# 文件路径
files = [
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
]

def detect_and_fix_gbk_utf8(raw):
    """检测GBK编码的中文并修复为UTF-8"""
    # 常见GBK中文模式（在错误位置出现）
    gbk_pairs = [
        # GBK字节 -> UTF-8编码
        (b'\xb8\x8d\xe5\xad\x98', '存'),  # 存
        (b'\xe5\x9c\xb0', '址'),  # 址
        (b'\xe7\xbe\x8e', '美'),  # 美
        (b'\xe5\x85\xb3', '关'),  # 关
        (b'\xe6\x97\xa0', '无'),  # 无
        (b'\xe4\xba\xbf', '亿'),  # 亿
        (b'\xe5\xae\x8c', '完'),  # 完
        (b'\xe4\xb8\x96', '世'),  # 世
        (b'\xe7\x95\x8c', '界'),  # 界
        (b'\xe5\x88\xb0', '到'),  # 到
        (b'\xe5\xa4\x9a', '多'),  # 多
        (b'\xe6\x96\x87', '文'),  # 文
        (b'\xe7\x8c\x81', '献'),  # 献
        (b'\xa0\xb7', '经'),  # 经
        (b'\xe7\xb1\xbb', '类'),  # 类
    ]
    
    result = bytearray(raw)
    fixed = 0
    
    # 检测GBK模式：如果看到 0x80-0xFF 的字节，可能GBK编码
    i = 0
    while i < len(result) - 1:
        b1, b2 = result[i], result[i+1]
        
        # 检查是否是GBK范围的高字节（0x81-0xFE）
        if b1 >= 0x81 and b1 <= 0xFE and b2 >= 0x40 and b2 <= 0xFE and b2 != 0x7F:
            # 这是GBK编码！尝试解码
            try:
                gbk_char = bytes([b1, b2]).decode('gbk')
                # 转为UTF-8
                utf8_bytes = gbk_char.encode('utf-8')
                # 替换
                result[i:i+2] = utf8_bytes
                fixed += 1
                i += len(utf8_bytes)
                continue
            except:
                pass
        
        # 检查是否是单字节UTF-8破损（通常0xD0-0xD9是拉丁扩展或GBK高字节）
        if b1 >= 0xC0 and b1 <= 0xDF:
            # 可能是一个损坏的UTF-8两字节序列
            # 检查后续字节
            if i + 2 < len(result) and 0x80 <= result[i+1] <= 0xBF:
                # 完整的UTF-8两字节，但可能内容是GBK
                # 保持原样，交给后续处理
                pass
        
        i += 1
    
    return bytes(result), fixed

# 先用Python chardet检测编码
try:
    import chardet
    HAS_CHARDET = True
except:
    HAS_CHARDET = False

for f in files:
    if not os.path.exists(f):
        print(f'SKIP: {f}')
        continue
    
    with open(f, 'rb') as file:
        raw = file.read()
    
    if HAS_CHARDET:
        detected = chardet.detect(raw)
        print(f'{f}: {detected}')
    
    # 尝试用GBK解码整个文件
    try:
        content_gbk = raw.decode('gbk')
        # 检查是否包含中文
        has_chinese = any('\u4e00' <= c <= '\u9fff' for c in content_gbk)
        if has_chinese:
            # 用UTF-8重新编码
            fixed_content = content_gbk.encode('utf-8')
            with open(f, 'wb') as file:
                file.write(fixed_content)
            print(f'FIXED (GBK->UTF8): {f}')
    except:
        # 不是GBK，用另一种方法
        fixed, n = detect_and_fix_gbk_utf8(raw)
        if n > 0:
            with open(f, 'wb') as file:
                file.write(fixed)
            print(f'FIXED ({n} GBK pairs): {f}')
        else:
            print(f'STILL ISSUE: {f}')
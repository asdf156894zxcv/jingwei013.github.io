import os, re

# 修复单个文件：移除无效的UTF-8字符，用?替换
def fix_utf8_file(filepath):
    with open(filepath, 'rb') as f:
        raw = f.read()
    
    # 检查是否有无效字符
    has_issue = False
    for i in range(len(raw)):
        b = raw[i]
        if b >= 0x80:
            # 检查是否是有效的UTF-8起始字节
            if b >= 0xF0:
                seq_len = 4
            elif b >= 0xE0:
                seq_len = 3
            elif b >= 0xC0:
                seq_len = 2
            else:
                # 单字节高字符，可能是Latin-1补充
                # 检查是否在损坏的GBK范围内（0x80-0xBF在第二个字节位置）
                # 尝试解码
                try:
                    raw[i:i+1].decode('utf-8')
                except:
                    has_issue = True
                    break
                continue
            
            if i + seq_len > len(raw):
                has_issue = True
                break
            
            seq = raw[i:i+seq_len]
            try:
                seq.decode('utf-8')
            except:
                has_issue = True
                break
    
    if not has_issue:
        return False, "No issues"
    
    # 修复：用errors='ignore'解码，再用UTF-8编码
    # 但更精确的方法是逐字节处理
    result = bytearray()
    i = 0
    while i < len(raw):
        b = raw[i]
        if b < 0x80:
            # ASCII: 直接保留
            result.append(b)
            i += 1
        else:
            # 尝试找到UTF-8序列
            found = False
            for seq_len in [4, 3, 2]:
                if i + seq_len <= len(raw):
                    seq = raw[i:i+seq_len]
                    try:
                        seq.decode('utf-8')
                        result.extend(seq)
                        i += seq_len
                        found = True
                        break
                    except:
                        pass
            
            if not found:
                # 无效字节：跳过或用?替换
                # 检查是否是GBK双字节
                if i + 1 < len(raw):
                    b1, b2 = raw[i], raw[i+1]
                    # GBK高字节范围: 0x81-0xFE，第二个字节: 0x40-0xFE (非0x7F)
                    if (0x81 <= b1 <= 0xFE and 0x40 <= b2 <= 0xFE and b2 != 0x7F):
                        try:
                            gbk_char = bytes([b1, b2]).decode('gbk')
                            utf8_bytes = gbk_char.encode('utf-8')
                            result.extend(utf8_bytes)
                            i += 2
                            continue
                        except:
                            pass
                
                # 无法修复，跳过该字节
                result.append(ord('?'))
                i += 1
    
    with open(filepath, 'wb') as f:
        f.write(bytes(result))
    
    original_size = len(raw)
    new_size = len(result)
    return True, f"Fixed: {original_size} -> {new_size}"

# 修复所有问题文件
files = [
    '404.html',
    'blog\\ai-hardware-startup-crisis-2026.html',
    'blog\\embodied-ai-april-27-funding-earthquake-day.html',
    'blog\\embodied-intelligence-q1-2026-funding-boom-analysis.html',
    'blog\\fscot-vs-fantasyvln-vln-cot-2026.html',
    'blog\\sim2real-gap-vln-2026.html',
    'blog\\vln-startup-ai-navigation-market-2026.html',
    'blog\\wmpo-world-model-vln-stop-decision-2026.html',
    'blog\\case-38-unitree-robotics.html',
    'styles.css',
    'PROGRESS.md',
    'README.md',
]

for f in files:
    if not os.path.exists(f):
        print(f'SKIP: {f}')
        continue
    fixed, msg = fix_utf8_file(f)
    print(f'{"FIXED" if fixed else "OK"}: {f} - {msg}')
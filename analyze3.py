f = 'blog\\ai-hardware-startup-crisis-2026.html'
with open(f, 'rb') as file:
    raw = file.read()

# 找到UTF-8有效的起始位置
print('Finding valid UTF-8 start...')
valid_start = 0
for i in range(len(raw)):
    try:
        raw[i:].decode('utf-8')
        valid_start = i
        print(f'Valid UTF-8 from position {i}')
        # 显示前后内容
        print(f'Before {i}: {raw[:i].hex()}')
        print(f'At {i}: {raw[i:i+30].hex()}')
        
        # 显示开头的文本（跳过前250字节损坏区域）
        # 先修复，然后显示250字节处的内容
        break
    except:
        pass

# 显示250字节处是什么
print(f'\nAt position 250:')
print(f'Bytes: {raw[250:280].hex()}')
try:
    print(f'Decoded (UTF-8): {raw[250:280].decode("utf-8")}')
except:
    pass

# 看看文件开头是什么
print(f'\nFirst 250 bytes hex:')
print(raw[:250].hex())

# 尝试用errors='ignore'读取
with open(f, 'rb') as file:
    raw = file.read()
content = raw.decode('utf-8', errors='ignore')
print(f'\nWith errors=ignore, len={len(content)}')
print(f'First 200 chars: {content[:200]}')
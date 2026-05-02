import chardet

f = 'blog\\ai-hardware-startup-crisis-2026.html'
with open(f, 'rb') as file:
    raw = file.read()

# 找具体哪里UTF-8失败
print('Testing UTF-8 decode...')
error_pos = None
try:
    raw.decode('utf-8')
    print('Full UTF-8 decode OK')
except UnicodeDecodeError as e:
    error_pos = e.start
    print(f'UTF-8 error at pos {error_pos}: {e.reason}')
    print(f'  Bytes around error: {raw[max(0,error_pos-10):error_pos+15].hex()}')

# 尝试部分解码，看看哪部分是GBK
print('\nTrying partial decode...')
for start in range(0, 500, 50):
    end = min(start + 200, len(raw))
    try:
        raw[start:end].decode('utf-8')
        print(f'  {start}-{end}: UTF-8 OK')
    except UnicodeDecodeError as e:
        print(f'  {start}-{end}: UTF-8 FAIL at +{e.start}')

# 检查是否是GBK开头的混合编码
print('\nTrying GBK decode...')
try:
    content_gbk = raw.decode('gbk')
    print(f'GBK OK, len={len(content_gbk)}')
    # 找包含"静"的位置
    for i, c in enumerate(content_gbk[:500]):
        if c == '静':
            print(f'  Found 静 at pos {i}')
            print(f'  Context: {content_gbk[max(0,i-5):i+5]}')
            break
except Exception as e:
    print(f'GBK error: {e}')
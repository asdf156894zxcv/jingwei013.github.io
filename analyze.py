import chardet

f = 'blog\\ai-hardware-startup-crisis-2026.html'
with open(f, 'rb') as file:
    raw = file.read()

# 检查字节200-230附近
print('Around pos 200-230:')
for i in range(195, 235):
    byte_val = raw[i]
    if 32 <= byte_val < 127:
        char_repr = chr(byte_val)
    else:
        char_repr = 'non-printable'
    print(f'  {i}: 0x{byte_val:02x} = {byte_val} = {char_repr}')

# 尝试定位损坏的中文字符
print('\nLooking for GBK-like bytes in first 500:')
for i in range(len(raw[:500]) - 1):
    b1, b2 = raw[i], raw[i+1]
    # GBK高字节范围
    if b1 >= 0x81 and b1 <= 0xFE and b2 >= 0x40 and b2 <= 0xFE and b2 != 0x7F:
        try:
            gbk_char = bytes([b1, b2]).decode('gbk')
            print(f'  GBK pair at {i}: 0x{b1:02x} 0x{b2:02x} = {gbk_char}')
        except:
            pass
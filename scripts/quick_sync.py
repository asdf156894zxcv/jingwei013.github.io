import os
import shutil

src = r"D:\jingwei013\website"
dst = r"D:\jingwei013\website-public"

# Copy index.html
shutil.copy2(os.path.join(src, "index.html"), os.path.join(dst, "index.html"))
print("index.html copied")

# Copy all blogs
src_blog = os.path.join(src, "blog")
dst_blog = os.path.join(dst, "blog")

for f in os.listdir(src_blog):
    if f.endswith('.html'):
        src_file = os.path.join(src_blog, f)
        dst_file = os.path.join(dst_blog, f)
        shutil.copy2(src_file, dst_file)
        print(f"Blog copied: {f}")

print("All files synced!")

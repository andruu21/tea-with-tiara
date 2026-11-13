"""ai-happy-01: copy entry.png (beside this file) into $MAKEFUN_OUTPUT_DIR."""
import os
import shutil

src = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
os.makedirs(out_dir, exist_ok=True)
dst = os.path.join(out_dir, "entry.png")
shutil.copyfile(src, dst)
print(f"copied {src} -> {dst} ({os.path.getsize(dst)} bytes)")

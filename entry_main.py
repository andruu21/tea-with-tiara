"""Entry runtime: copy the pre-rendered entry.png to the output dir.

The final image is generated offline in the build session by gen_entry.py
(PIL) and committed as entry.png; the graded runtime (Python 3.13 stdlib
only) just copies it to $MAKEFUN_OUTPUT_DIR (default /output).
"""
import os
import shutil

src = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
out = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
os.makedirs(out, exist_ok=True)
shutil.copyfile(src, os.path.join(out, "entry.png"))
print("entry.png ->", out)

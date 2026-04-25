#To use this tool, you need to make sure your Python version is
#greater than 3.7, and you have libraries like Pyinstaller and tqdm.
import os
import sys
import base64
import json
import subprocess
import shutil
from tqdm import tqdm

print("==================================================")
print("       Self extracting Creator")
print("==================================================")

source = input("\nFolder: ").strip()
save = input("Save EXE: ").strip()

source = os.path.abspath(source)
if not os.path.isdir(source):
    print("Error: Folder not found")
    os.system("pause")
    sys.exit()

out_dir = os.path.dirname(save)
exe_name = os.path.basename(save)
os.makedirs(out_dir, exist_ok=True)

print("\nLoading files...")
file_list = []
for r, _, f in os.walk(source):
    for name in f:
        file_list.append(os.path.join(r, name))

data = {}
for fp in tqdm(file_list, desc="Packing"):
    try:
        rel = os.path.relpath(fp, source)
        with open(fp, "rb") as f:
            data[rel] = base64.b64encode(f.read()).decode()
    except:
        continue

tmp_py = os.path.join(out_dir, "run.py")
code = f'''
import os,base64,json,time
import tkinter as tk
from tkinter import ttk

def go():
    out = "{os.path.basename(source)}"
    os.makedirs(out, exist_ok=True)
    data = {json.dumps(data)}
    for k,v in data.items():
        p = os.path.join(out,k)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p,"wb") as f:
            f.write(base64.b64decode(v))

if __name__ == "__main__":
    go()
'''

with open(tmp_py, "w", encoding="utf-8") as f:
    f.write(code)

print("\nBuilding EXE...")
os.system(f'cd /d "{out_dir}" && pyinstaller -F -w -i NONE run.py')

final_exe = os.path.join(out_dir, exe_name)
if os.path.exists(os.path.join(out_dir, "dist", "run.exe")):
    shutil.move(os.path.join(out_dir, "dist", "run.exe"), final_exe)

try:
    os.remove(tmp_py)
    os.remove(os.path.join(out_dir, "run.spec"))
    shutil.rmtree(os.path.join(out_dir, "build"), ignore_errors=True)
    shutil.rmtree(os.path.join(out_dir, "dist"), ignore_errors=True)
except:
    pass

print(f"\nDone. {final_exe}")
os.system("pause")

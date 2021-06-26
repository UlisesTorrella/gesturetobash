import sys


if len(sys.argv)<2:
  print("You need to tell me the name of the gesture to remove")
  exit()
import os

_, name = sys.argv

fname = "gestures/__init__.py"

f = open(fname)
output = []
for line in f:
    if not f"from .{name} import {name}" in line:
        output.append(line)
f.close()
f = open(fname, 'w')
f.writelines(output)
f.close()

os.remove(f"gestures/{name}.py")

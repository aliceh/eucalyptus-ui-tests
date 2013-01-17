import os

files = os.listdir(".")
files.sort()

for fname in files:
  if not fname.startswith("test") or not fname.endswith(".py"):
    continue
  try:
    os.system("python " + fname)
  except:
   pass 

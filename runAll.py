import os

files = os.listdir(".")
files.sort()

for fname in files:
  if not fname.startswith("test-") or not (fname.endswith(".py") or fname.endswith(".sh")):
    continue
  try:
    if fname.endswith(".py"):
      os.system("python " + fname)
    else:
      os.system("bash " + fname)
  except:
   pass 

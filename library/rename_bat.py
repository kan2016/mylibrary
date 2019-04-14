# -*- coding: utf-8 -*-
import os, re

def get_files(path):
  fs = []
  for root, dirs, files in os.walk(path):
    for f in files:
      fs.append(os.path.join(root, f))
  return fs

def rename_bat(s):
  # flip .bat <-> _bat
  ss = s
  if re.search(r'\.bat$', s): 
    ss = re.sub(r'\.bat$', '_bat', s)
  if re.search(r'_bat$' , s):
    ss = re.sub(r'_bat$', '.bat', s)
  return ss

path = '.'
fs = get_files(path)
gs = [rename_bat(f) for f in fs]

for (f,g) in zip(fs, gs):
  os.rename(f,g)


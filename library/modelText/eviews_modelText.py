# written by Kazutoshi KAN, 2018
# -*- coding: utf-8 -*-
import re
from modelText.eviews_clean import clean_args, clean

class Equation():
  @clean_args
  def __init__(self, streq):
    try:
      [self.idx, self.eq] = streq.split(':')
    except:
      raise ValueError('\n\n *** INVALID EQUATION '+streq+' ***\n')

  def __str__(self):
    return self.idx+':'+self.eq


class modelText():
  def __init__(self, s=None):
    self.eList = []
    if s:
      self.append(s)

  def find(self, idx):
    for e in self.eList:
      if e.idx == idx: return e
  
  def append_elem(self, s):
    sList = clean(s.split('\n'))
    for streq in sList:
      e = Equation(streq)
      position = len(self.eList)
      target = self.find(e.idx)
      if target:
        position = self.eList.index(target)
        self.eList.remove(target)
      self.eList.insert(position, e)
    return

  def append(self, *s):
    if len(s) == 1:
      s = s[0]       # (e1)->e1 ([e1,e2])->[e1,e2]
      if isinstance(s, str):
        self.append_elem(s)
        return
    for ss in s:     # (e1,e2), [e1,e2]
      self.append(ss)

  @clean_args
  def insert(self, streq, after=None, before=None):
    e = Equation(streq)
    if self.find(e.idx):
      raise Exception('\n\n *** DUPLICATE '+e.idx+' EQUATION! ***\n')
    idx = after if after else before
    target = self.find(idx)
    try:
      position = self.eList.index(target)
      if after is not None: position += 1 
      self.eList.insert(position, e)
    except:
      raise ValueError('\n\n *** NO INSERT LOCATION '+idx+'! ***\n')

  def remove_elem(self, idx):
    try:
      target = self.find(clean(idx))
      self.eList.remove(target)
    except:
      raise ValueError('\n\n *** NO REMOVAL TARGET '+idx+' ***\n')
    return

  def remove(self, *idxs):
    if len(idxs) == 1:
      idxs = idxs[0]   # ('a')->'a', (['a','b'])->['a','b']
      if isinstance(idxs, str):
        self.remove_elem(idxs)
        return
    for idx in idxs:   # ('a','b'), ['a','b']
      self.remove(idx)

  def findall(self, pattern):
    return [str(e) for e in self.eList if re.search(pattern, e.idx, re.I)]

  def __str__(self):
    return '\n'.join([str(e) for e in self.eList])


# -*- sample code -*-  
if __name__ == '__main__':
  mt = modelText()

  e1 = 'x:x=x(-1)+v_x'
  e2 = 'y:y=y(-1)+v_y'
  e3 = 'z:z=z(-1)+v_z'

  e123 = ''' x:x=x(-1)+v_x
             y:y=y(-1)+v_y
             z:z=z(-1)+v_z
         '''
  mt.append(e1, e2, e3)        # multi args
  mt.append(e123)              # multi-line text
  mt.append(['x:x=x(-1)+v_x']) # list
  mt.append(('x:x=x(-1)+v_x')) # tuple
  mt.append({'x:x=x(-1)+v_x'}) # set

  e4 = 'a:a=a(-1)+v_a'
  e5 = 'b:b=b(-1)+v_b'
  mt.insert(e4, after ='y')
  mt.insert(e5, before='y')

  print(str(mt))
  # X:X=X(-1)+V_X
  # B:B=B(-1)+V_B
  # Y:Y=Y(-1)+V_Y
  # A:A=A(-1)+V_A
  # Z:Z=Z(-1)+V_Z

  print(mt.findall('[z|b]'))
  #-> ['B:B=B(-1)+V_B', 'Z:Z=Z(-1)+V_Z']

  mt.remove('a', 'b')          # multi args
  mt.remove(['x'])             # list
  mt.remove(('y'))             # tuple
  mt.remove({'z'})             # set

  print(str(mt))
  #-> empty string




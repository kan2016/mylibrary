# written by Kazutoshi KAN, 2018
# -*- coding: utf-8 -*-
from algorithm.graph import Edge
from algorithm.getDst import getDst, getSrc
from algorithm.DulmageMendelsohnDecomposition import DulmageMendelsohnDecomposition

class modelStructure():
  def __init__(self, allvss, vall, vendo, lines):
    # set exogenous and endogenous vars in equations
    self.allvss = allvss
    self.vall   = vall
    self.vendo  = vendo
    self.lines  = lines
    self.analyze_structure()

  def change_sym(self, exog2endo, endo2exog):
    # name originates from nostalgic TROLL
    exog2endo = set(exog2endo)
    endo2exog = set(endo2exog)
    # validation of input
    df1 = exog2endo - self.vexog
    df2 = endo2exog - self.vendo
    if df1 and exog2endo:
      raise ValueError("\n*** ERROR: "+str(df1)+" NOT IN EXOG ***\n")
    if df2 and endo2exog:
      raise ValueError("\n*** ERROR: "+str(df2)+" NOT IN ENDO ***\n")
    if len(exog2endo) != len(endo2exog):
      raise ValueError("\n*** ERROR: LEN(exog2endo)!=LEN(exog2endo) ***\n")
    # exchange var type i.e. exog <-> endo 
    self.vendo = (self.vendo-endo2exog)|exog2endo
    self.analyze_structure()

  def analyze_structure(self):
    self.setup()
    self.construct_g()
    self.dm_decomp()
    self.construct_gb()            # optional
    self.construct_blocked_model() # optional

  def setup(self):
    # generate endo exog vars' lists and dictionaries
    self.vexog  = self.vall - self.vendo
    self.endoss = [vs - self.vexog for vs in self.allvss]
    self.exogss = [vs - self.vendo for vs in self.allvss]
    self.d  = {v: i for i, v in enumerate(sorted(self.vendo))}
    self.dr = {i: v for i, v in enumerate(sorted(self.vendo))}

  def construct_g(self):
    # construct graph of endogenous vars' dependency
    self.g = [[] for n in range(len(self.d))]
    for e in range(len(self.endoss)):
      for v in sorted(self.endoss[e]):
        self.g[e].append(Edge(e, self.d[v]))

  def dm_decomp(self):
    # detect finest block structure (core routine)
    self.rss = []
    self.css = []
    DulmageMendelsohnDecomposition(self.g, self.rss, self.css)

  def find_css_block(self, v):
    # find css_block in which variable v joins
    for k in range(len(self.rss)):
      if v in self.css[k]: return k

  def construct_gb(self):
    # construct graph of dm-decomped blocks' dependency
    nb = len(self.rss)
    self.endossb = [set() for n in range(nb)]
    for k in range(nb):
      for e in self.rss[k]:
        self.endossb[k] |= {self.find_css_block(v.dst) for v in self.g[e]}

    self.gb = [[] for n in range(nb)]
    for k in range(nb):
      for v in self.endossb[k]:
        self.gb[k].append(Edge(k, v))

  def construct_blocked_model(self):
    # each block's endos set, exogs set, equation list, determined vars set
    self.endobss = [{v for r in rs for v in self.endoss[r]} for rs in self.rss]
    self.exogbss = [{v for r in rs for v in self.exogss[r]} for rs in self.rss]
    self.linebss = [[self.lines[r] for r in rs] for rs in self.rss]
    self.determined = [{self.dr[c] for c in cs} for cs in self.css]

  def classify_vars(self, var):
    # pre = v joins predetermined blocks before var
    # sim = v joins simutaneously determined block with var
    # pos = v joins postdetermined blocks after var ('burasagari' in Japanese)
    # iso = v joins isolated block from var block
    v    = self.d[var]
    simb = self.find_css_block(v)
    preb = getDst(self.gb, [simb])
    posb = getSrc(self.gb, [simb])
    preb.remove(simb)
    posb.remove(simb)
    pre = {self.dr[v] for b in preb for v in self.css[b]}
    pos = {self.dr[v] for b in posb for v in self.css[b]}
    sim = {self.dr[v] for v in self.css[simb]}
    iso = self.vendo - pre - pos - sim
    return [pre, sim, pos, iso]


if __name__ == '__main__':
  lines = ['X:LOG(X/Y)=C_X(1)*Y(-1)+C_X(2)*Z(-1)+E_X',
           'E_X:E_X=C_E_X(1)*E_X(-1)+V_X'            ,
           'Y:LOG(Y)=C_Y(1)*Y+C_Y(2)*Z+W+E_Y+A'      ,
           'E_Y:E_Y=C_E_Y(1)*E_Y(-1)+V_Y+Z'          ,
           'Z:LOG(Z/Y)=C_Z(1)*Y+C_Z(2)*Z+E_Z'        ,
           'E_Z:E_Z=C_E_Z(1)*E_Z(-1)+V_Z'            ,
           'W:W=W(-1)+A+E_W'                         ,
           'E_W:E_W=E_W(-1)+V_W'                     ,
           'A:A=A(-1)+W(1)+E_A'                      ,
           'E_A:E_A=E_A(-1)+V_A'                     ]


  allvss = [{'Z', 'X', 'E_X', 'Y'}     ,
            {'E_X', 'V_X'}             ,
            {'Z', 'E_Y', 'W', 'Y', 'A'},
            {'Z', 'E_Y', 'V_Y'}        ,
            {'Z', 'Y', 'E_Z'}          ,
            {'E_Z', 'V_Z'}             ,
            {'E_W', 'W', 'A'}          ,
            {'E_W', 'V_W'}             ,
            {'E_A', 'W', 'A'}          ,
            {'E_A', 'V_A'}             ]


  vall  = {'X'  , 'Y'  , 'Z'  , 'W'  , 'A'  ,
           'E_X', 'E_Y', 'E_Z', 'E_W', 'E_A',
           'V_X', 'V_Y', 'V_Z', 'V_W', 'V_A' }

  vendo = {'X'  , 'Y'  , 'Z'  , 'W'  , 'A'  ,
           'E_X', 'E_Y', 'E_Z', 'E_W', 'E_A' }

  ms = modelStructure(allvss, vall, vendo, lines)
  print('rss  = '+str(ms.rss))
  print('css  = '+str(ms.css))

  [pre, sim, pos, iso] = ms.classify_vars('E_Y')
  print('sim= '+str(sorted(sim)))
  print('pre= '+str(sorted(pre)))
  print('pos= '+str(sorted(pos)))
  print('iso= '+str(sorted(iso)))

  ms.change_sym(exog2endo=['V_A', 'V_W'], endo2exog=['A', 'W'])
  print('rss  = '+str(ms.rss))
  print('css  = '+str(ms.css))




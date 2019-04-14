# written by Kazutoshi KAN, 2018
# -*- coding: utf-8 -*-
import os

def build_modeltext_blocked(ms):
  # EVIEWS RECOGNISION of endo and exog variables in model object
  endobss_eviews = [{l.split(':')[0] for l in ls} for ls in ms.linebss]
  vendo_eviews  = {v for vs in endobss_eviews for v in vs}
  vexog_eviews  = ms.vall - vendo_eviews

  # calc exog2endo and endo2exog in each finest block
  nb = len(ms.rss)
  solved     = set()
  determined = [set() for n in range(nb)]
  exog2endo  = [set() for n in range(nb)]
  endo2exog  = [set() for n in range(nb)]
  for b in range(nb):
    determined[-b-1] = ms.endobss[-b-1] - solved
    # exog for EViews, mathematically endo detemined in the block
    exog2endo[-b-1] = determined[-b-1] - endobss_eviews[-b-1]
    # endo for EViews, mathematically not endo determined in the block
    endo2exog[-b-1] = endobss_eviews[-b-1] - determined[-b-1]
    solved |= ms.endobss[-b-1]

  # merge until exdo2exog and exog2endo are empty
  exog2endo_mg = [[] for n in range(nb)]
  endo2exog_mg = [[] for n in range(nb)]
  rs_mg        = [[] for n in range(nb)]
  n_mg, prev = 0, False
  for b in range(nb):
    # split at non empty exog2endo and V0 and Vinf
    if exog2endo[-b-1] or prev or b==1 or b==nb-1: n_mg +=1
    exog2endo_mg[n_mg] = exog2endo[-b-1]
    endo2exog_mg[n_mg] = endo2exog[-b-1]
    rs_mg[n_mg] += ms.rss[-b-1][::-1] # reverse
    prev = True if exog2endo[-b-1] else False
  exog2endo_mg = exog2endo_mg[0:n_mg+1]
  endo2exog_mg = endo2exog_mg[0:n_mg+1]
  rs_mg        = rs_mg[0:n_mg+1]

  # merged blocked model for writing modeltext file
  fs = []
  fs.append(str(len(rs_mg)))
  for n in range(len(rs_mg)):
    fs.append(str(len(rs_mg[n])))
    fs.append('exog2endo ='+' '.join(sorted(exog2endo_mg[n])))
    fs.append('endo2exog ='+' '.join(sorted(endo2exog_mg[n])))
    for r in range(len(rs_mg[n])):
      fs.append(ms.lines[rs_mg[n][r]])

  # (optional) finest blocked model for writing modeltext file
  fsf = []
  fsf.append(str(len(ms.rss)))
  for b in range(len(ms.rss)):
    rs = ms.rss[-b-1]
    fsf.append(str(len(rs)))
    fsf.append('exog2endo ='+' '.join(sorted(exog2endo[-b-1])))
    fsf.append('endo2exog ='+' '.join(sorted(endo2exog[-b-1])))
    for r in range(len(rs)):
      fsf.append(ms.lines[rs[-r-1]])

  return [fs, fsf]


def write_modeltext_blocked(ms, modelFilePath, getFinest=False):

  [fs, fsf] = build_modeltext_blocked(ms)

  # write blocked modeltext file
  with open(modelFilePath, 'w') as f:
    f.write('\n'.join(fs))

  if not getFinest: return

  # (optional) write finest blocked modeltext file
  base = os.path.basename(modelFilePath).replace('.','_finest.')
  path = os.path.join(os.path.dirname(modelFilePath), base)
  with open(path, 'w') as f:
    f.write('\n'.join(fsf))


# -*- sample code -*-
if __name__ == '__main__':
  from modelStructure.modelStructure import modelStructure

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

  ms.change_sym(exog2endo=['V_A'], endo2exog=['A'])

  [fs, fsf] = build_modeltext_blocked(ms)

  print('\n'.join(fs))
  print('\n'.join(fsf))

  #->
  #5
  #0
  #exog2endo =
  #endo2exog =
  #8
  #exog2endo =
  #endo2exog =
  #E_X:E_X=C_E_X(1)*E_X(-1)+V_X
  #E_Z:E_Z=C_E_Z(1)*E_Z(-1)+V_Z
  #E_W:E_W=E_W(-1)+V_W
  #W:W=W(-1)+A+E_W
  #Y:LOG(Y)=C_Y(1)*Y+C_Y(2)*Z+W+E_Y+A
  #E_Y:E_Y=C_E_Y(1)*E_Y(-1)+V_Y+Z
  #Z:LOG(Z/Y)=C_Z(1)*Y+C_Z(2)*Z+E_Z
  #X:LOG(X/Y)=C_X(1)*Y(-1)+C_X(2)*Z(-1)+E_X
  #1
  #exog2endo =E_A
  #endo2exog =A
  #A:A=A(-1)+W(1)+E_A
  #1
  #exog2endo =V_A
  #endo2exog =E_A
  #E_A:E_A=E_A(-1)+V_A
  #0
  #exog2endo =
  #endo2exog =
  #
  #->
  #10
  #0
  #exog2endo =
  #endo2exog =
  #1
  #exog2endo =
  #endo2exog =
  #E_X:E_X=C_E_X(1)*E_X(-1)+V_X
  #1
  #exog2endo =
  #endo2exog =
  #E_Z:E_Z=C_E_Z(1)*E_Z(-1)+V_Z
  #1
  #exog2endo =
  #endo2exog =
  #E_W:E_W=E_W(-1)+V_W
  #1
  #exog2endo =
  #endo2exog =
  #W:W=W(-1)+A+E_W
  #3
  #exog2endo =
  #endo2exog =
  #Y:LOG(Y)=C_Y(1)*Y+C_Y(2)*Z+W+E_Y+A
  #E_Y:E_Y=C_E_Y(1)*E_Y(-1)+V_Y+Z
  #Z:LOG(Z/Y)=C_Z(1)*Y+C_Z(2)*Z+E_Z
  #1
  #exog2endo =
  #endo2exog =
  #X:LOG(X/Y)=C_X(1)*Y(-1)+C_X(2)*Z(-1)+E_X
  #1
  #exog2endo =E_A
  #endo2exog =A
  #A:A=A(-1)+W(1)+E_A
  #1
  #exog2endo =V_A
  #endo2exog =E_A
  #E_A:E_A=E_A(-1)+V_A
  #0
  #exog2endo =
  #endo2exog =

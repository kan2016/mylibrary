# written by Kazutoshi KAN, 2018
# -*- coding: utf-8 -*-
from algorithm.graph import adj_matrix
import matplotlib.pyplot as plt

def write_for_debug(ms, DIR):
  write_blocked_model(ms, DIR)
  write_endo_exog_in_equation(ms, DIR)
  write_figures(ms, DIR)

def write_blocked_model(ms, DIR): # for debug
  with open(DIR + 'model_blocked.txt', 'w') as f:
    for b in range(len(ms.rss)):
      rs = ms.rss[-b-1]
      f.write('\n')
      f.write('determined='+str(ms.determined[-b-1])+'\n')
      for r in range(len(rs)):
        f.write(ms.lines[rs[-r-1]])
        f.write('\n')

def write_endo_exog_in_equation(ms, DIR):
  with open(DIR+'endos_exog_in_equation.txt', 'w') as f:
    for i in range(len(ms.lines)):
      f.write(ms.lines[i])
      f.write('\n endog: ')
      f.write(str(ms.endoss[i]))
      f.write('\n exogg:')
      f.write(str(ms.exogss[i]))
      f.write('\n\n')

# plot non-zero elements of matrix
def plot_mat_nonzero(image, title='non zero elements', figname='fig.png'):
  for i in range(len(image)):
    for j in range(len(image[0])):
      if not image[i][j] == 0:
        image[i][j] = 0
      else:
        image[i][j] = 1
  fig, ax = plt.subplots()
  ax.imshow(image, cmap=plt.cm.gray, interpolation='none')
  ax.set_title(title)
  plt.savefig(figname)

def write_figures(ms, DIR): # for display
  # make adjacenct matrix of org and decomped graph
  gm = adj_matrix(ms.g)
  rs = [n for rs in ms.rss for n in rs]
  cs = [n for cs in ms.css for n in cs]
  n = len(ms.g)
  gm_dm = [[0]*n for i in range(n)]
  for i in range(n):
    for j in range(n):
      gm_dm[i][j] = gm[rs[i]][cs[j]]
  plot_mat_nonzero(gm   , title='before', figname=DIR+'before.png')
  plot_mat_nonzero(gm_dm, title='after' , figname=DIR+'after.png' )


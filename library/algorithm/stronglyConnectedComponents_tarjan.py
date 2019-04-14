# written by Kazutoshi KAN, 2018
# -*- coding: utf-8 -*-
from algorithm.graph import Edge

def visit(g, v, scc, S, inS, low, num, time):
  time += 1
  low[v] = num[v] = time
  S.append(v)
  inS[v] = True

  for e in g[v]:
    w = e.dst 
    if num[w] == 0:
      visit(g, w, scc, S, inS, low, num, time)
      low[v] = min(low[v], low[w])
    elif inS[w]:
      low[v] = min(low[v], num[w])

  if low[v] == num[v]:
    scc.append([])
    while True:
      w      = S.pop()
      inS[w] = False
      scc[len(scc)-1].append(w)
      if v == w: break

# Tarjan's algorithm
def stronglyConnectedComponents(g, scc):
  n = len(g)
  num = [0]*n
  low = [0]*n
  inS = [False]*n
  S   = []
  del scc[:]
  time = 0
  for u in range(n):
    if num[u] == 0:
      visit(g, u, scc, S, inS, low, num, time)


# -*- sample code -*-
if __name__=='__main__':
  scc = []

  g = [[Edge(0,6)],
       [Edge(1,0)],
       [Edge(2,6)],
       [Edge(3,4)],
       [Edge(4,3)],
       [Edge(5,0), Edge(5,4)],
       [Edge(6,1), Edge(6,3), Edge(6,4), Edge(6,5)]
      ]

  stronglyConnectedComponents(g, scc)

  print(scc)
  #-> [[4, 3], [5, 1, 6, 0], [2]]


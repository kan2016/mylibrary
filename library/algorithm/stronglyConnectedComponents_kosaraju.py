# written by Kazutoshi KAN, 2018
# -*- coding: utf-8 -*-
from algorithm.graph import Edge, reverse

def visit1(g, v, visited, order, k):
  visited[v] = True
  for e in g[v]:
    if not visited[e.dst]:
      visit1(g, e.dst, visited, order, k)
  order[k[0]] = v
  k[0] += 1

def visit2(g, v, visited, scc, k):
  visited[v] = True
  for e in g[v]:
    if not visited[e.dst]:
      visit2(g, e.dst, visited, scc, k)
  scc[k].append(v) 

# Kosaraju's algorithm
def stronglyConnectedComponents(g, scc):
  scc[:]  = []
  n       = len(g)

  visited = [False]*n
  order   = [-1]*n
  k = [0]
  for v in range(n):
    if not visited[v]:
      visit1(g, v, visited, order, k)

  g = reverse(g)
  k = -1
  visited = [False]*n
  for u in range(n):
    if not visited[order[n-1-u]]:
      k += 1
      scc.append([])
      visit2(g, order[n-1-u], visited, scc, k)

  return scc


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
  #-> [[2], [6, 1, 5, 0], [4, 3]]


# written by Kazutoshi KAN, 2018
# -*- coding: utf-8 -*-
from algorithm.graph import Edge

# Ford-Fulkerson algorithm
def augment(g, u, matchTo, visited):
  if u < 0: return True
  for e in g[u]:
    if not visited[e.dst]:
      visited[e.dst] = True
      if augment(g, matchTo[e.dst], matchTo, visited):
        matchTo[e.src] = e.dst
        matchTo[e.dst] = e.src
        return True
  return False

# g: bipartite graph
# L: size of the left side
def bipartiteMatching(g, L, matching):
  n = len(g)
  matchTo = [-1 for n in range(n)]
  match = 0
  for u in range(L):
    visited = [False]*n
    if augment(g, u, matchTo, visited):
      match+=1
  for u in range(L):
    if matchTo[u] >= 0:
      matching.append(Edge(u, matchTo[u]))
  return match

# -*- sample code -*-
if __name__=='__main__':
  from algorithm.graph import Edge
  matching = []
  L = 3
  g = [[Edge(0,3), Edge(0,4)],
       [Edge(1,4), Edge(1,5)],
       [Edge(2,5)],
       [Edge(3,0)],
       [Edge(4,0), Edge(4,1)],
       [Edge(5,1), Edge(5,2)]
      ]
  bipartiteMatching(g, L, matching)
  for e in matching: print(e)



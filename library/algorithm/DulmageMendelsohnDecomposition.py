# written by Kazutoshi KAN, 2018
# -*- coding: utf-8 -*-
from algorithm.graph import Edge, reverse
from algorithm.bipartiteMatching import bipartiteMatching
from algorithm.stronglyConnectedComponents_kosaraju import stronglyConnectedComponents

# return reachable nodes from src
def getDst(g, src):
  def visit(g, u, visited):
    visited[u] = True
    for e in g[u]:
      if not visited[e.dst]:
        visit(g, e.dst, visited)

  visited = [False]*len(g)
  for u in src:
    if not visited[u]:
      visit(g, u, visited)
  dst = [v for v in range(len(g)) if visited[v]]
  return dst


# generate bipartite graph
def bipartiteGraph(g, rL, cL):
  gb = [[] for n in range(rL+cL)]
  for edges in g:
    for e in edges:
      gb[e.src   ].append(Edge(e.src   , e.dst+rL))
      gb[e.dst+rL].append(Edge(e.dst+rL, e.src   ))
  return gb


def DulmageMendelsohnDecomposition(g, rs, cs):
  rL = len(g)
  cL = max([e.dst for edges in g for e in edges])+1

  # step0: generate bipartite graph
  gb = bipartiteGraph(g, rL, cL)

  # step1: find bipartiteMatching
  matching = []
  bipartiteMatching(gb, rL, matching)

  # step2: modify graph i.e. birateral M and R -> C edges
  gb[rL:] = [[] for n in range(cL)]
  for m in matching:
    r = min(m.src, m.dst)
    c = max(m.src, m.dst)
    gb[c].append(Edge(c, r))

  # step3: find V0 and Vinf
  matched =  [m.src for m in matching]
  matched += [m.dst for m in matching]
  rsrc = [n for n in range(rL)        if not n in matched]
  cdst = [n for n in range(rL, rL+cL) if not n in matched]
  Vinf = getDst(gb, rsrc)
  V0   = getDst(reverse(gb), cdst)

  # step4: find scc of g without V0 and Vinf 
  # Kosaraju's algorithm to preserve topological order of scc
  V     = V0 + Vinf
  gb[:] = [[e for e in edges if not (e.dst in V or e.src in V)] for edges in gb]
  scc   = []
  stronglyConnectedComponents(gb, scc)
  scc[:] = [c for c in scc if not c[0] in V] # remove V0 and Vinf
  scc[:] = [V0] + scc + [Vinf]

  rs[:] = [[n    for n in c if n <  rL] for c in scc]
  cs[:] = [[n-rL for n in c if n >= rL] for c in scc]


# -*- sample code -*- 
if __name__=='__main__':
  from algorithm.graph import adj_list, reverse

  # example 1
  gm = [[0, 1, 0, 1, 2, 0, 0],
        [0, 0, 2, 1, 0, 5, 0],
        [0, 0, 0, 4, 0, 0, 1],
        [1, 0, 0, 1, 0, 0, 0],
        [3, 1, 0, 0, 1, 1, 0],
        [0, 0, 0, 3, 0, 0, 1],
        [0, 0, 1, 0, 0, 3, 4]
        ]
  g = adj_list(gm)
  rs = []
  cs = []
  DulmageMendelsohnDecomposition(g, rs, cs)
  print(rs)
  print(cs)
  #-> rs = [[], [4, 0], [1, 6], [3], [5, 2], []]
  #-> cs = [[], [1, 4], [2, 5], [0], [6, 3], []]

  # example 2
  gm = [[0, 0, 0, 0, 0, 1, 1],
        [0, 1, 0, 0, 0, 0, 0],
        [1, 1, 1, 0, 1, 0, 0],
        [0, 0, 1, 0, 0, 1, 0],
        [0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 1, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 1]
        ]
  g = adj_list(gm)
  rs = []
  cs = []
  DulmageMendelsohnDecomposition(g, rs, cs)
  print(rs)
  print(cs)
  #-> rs = [[2, 5], [3], [1], [0], [4, 6]]
  #-> cs = [[0, 3, 4], [2], [1], [5], [6]]


  # display
  rs = [n for r in rs for n in r]
  cs = [n for c in cs for n in c]

  n = len(g)
  gm2 = [[0]*n for i in range(n)]
  for i in range(n):
    for j in range(n):
      gm2[i][j] = gm[rs[i]][cs[j]]

  from pprint import pprint
  print("")
  pprint(gm)
  print("->")
  pprint(gm2)

  #gm  = 
  #  [[0, 0, 0, 0, 0, 1, 1],
  #   [0, 1, 0, 0, 0, 0, 0],
  #   [1, 1, 1, 0, 1, 0, 0],
  #   [0, 0, 1, 0, 0, 1, 0],
  #   [0, 0, 0, 0, 0, 0, 1],
  #   [1, 0, 0, 1, 1, 0, 0],
  #   [0, 0, 0, 0, 0, 0, 1]]
  #  ->
  #gm2 =
  #  [[1, 0, 1, 1, 1, 0, 0],
  #   [1, 1, 1, 0, 0, 0, 0],
  #   [0, 0, 0, 1, 0, 1, 0],
  #   [0, 0, 0, 0, 1, 0, 0],
  #   [0, 0, 0, 0, 0, 1, 1],
  #   [0, 0, 0, 0, 0, 0, 1],
  #   [0, 0, 0, 0, 0, 0, 1]]

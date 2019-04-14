# written by Kazutoshi KAN, 2018
# -*- coding: utf-8 -*-
# define basic element of graphs

# graph is an adjacency list 
# i.e. graph g = [node] = [[edge]]
class Edge():
  def __init__(self, src, dst, weight=0):
    self.src = src
    self.dst = dst
    self.weight = weight
  def __str__(self):
    return str("("+str(self.src)+","+str(self.dst)+")")

# return adj_matrix 
def adj_matrix(g):
  gm = [[0]*len(g) for n in range(len(g))] 
  for edges in g:
    for e in edges:
      gm[e.src][e.dst] = 1
  return gm

# return adj_list
def adj_list(gm):
  g = [[] for n in range(len(gm))]
  for u in range(len(gm)):
    for v in range(len(gm)):
      if gm[u][v]: g[u].append(Edge(u,v))
  return g

# return reversed graph
def reverse(g):
  gr = [[] for n in range(len(g))]
  for edges in g:
    for e in edges:
      gr[e.dst].append(Edge(e.dst, e.src))
  return gr
  
# print graph
def debug_print_graph(g):
  s = []
  for edges in g:
    for e in edges:
      s.append('('+str(e.src)+','+str(e.dst)+')')
    s.append('\n')
  print(''.join(s))


# -*- sample code -*- 
if __name__ == '__main__':
  g = [[Edge(0,3), Edge(0,4)],
       [Edge(1,4), Edge(1,5)],
       [Edge(2,5)],
       [Edge(3,0)],
       [Edge(4,0)],
       [Edge(5,1), Edge(5,2)]]

  gm = adj_matrix(g)
  g  = adj_list(gm)
  gr = reverse(g)

  from pprint import pprint
  pprint(gm)
  #-> [[0, 0, 0, 1, 1, 0],
  #    [0, 0, 0, 0, 1, 1],
  #    [0, 0, 0, 0, 0, 1],
  #    [1, 0, 0, 0, 0, 0],
  #    [1, 0, 0, 0, 0, 0],
  #    [0, 1, 1, 0, 0, 0]]

  debug_print_graph(gr)
  #-> (0,3)(0,4)
  #   (1,5)
  #   (2,5)
  #   (3,0)
  #   (4,0)(4,1)
  #   (5,1)(5,2)


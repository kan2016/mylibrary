# written by Kazutoshi KAN
# -*- coding: utf-8 -*-

def flatten(xss):
  return [x for xs in xss for x in xs]

def rotate(xs, n):
  return xs[n:] + xs[:n]


if __name__ == '__main__':
  xs = [1,2,3,4,5]

  rotate(xs,  3)
  #-> [4, 5, 1, 2, 3]

  rotate(xs, -3)
  #-> [3, 4, 5, 1, 2]

  xss = [[1,2,3],[4,5]]

  flatten(xss)
  #-> [1, 2, 3, 4, 5]

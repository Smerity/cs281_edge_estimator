import sys
##
import numpy as np
##


class Node(object):
  def __init__(self, n, edges=None):
    self.n = n
    self.count = 0
    self.edges = edges if edges else {}

  def visits(self):
    return np.random.uniform(0, 1000)

  def reset(self):
    self.count = 0

  def __repr__(self):
    return 'Node(n={}, edges={})'.format(self.n, self.edges)


def read_input(data):
  nodes = {}
  for line in data:
    a, b = map(int, line.split(' -> '))
    if a not in nodes:
      nodes[a] = Node(a)
    if b not in nodes:
      nodes[b] = Node(b)
    ##
    nodes[a].edges[b] = 1
  return nodes


if __name__ == '__main__':
  print read_input(sys.stdin)

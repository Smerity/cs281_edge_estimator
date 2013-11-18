from __future__ import division
import sys
##
import networkx as nx
##


def read_input(data):
  G = nx.DiGraph()
  for line in data:
    a, b = map(int, line.strip().split(' -> '))
    G.add_node(a)
    G.add_node(a)
    # DiGraph doesn't allow duplicate edges
    G.add_edge(a, b, weight=1)
  return G


def normalize_outgoing(G):
  for n in G.nodes_iter():
    edges = G.out_edges(n, data=True)
    z = sum(data['weight'] for u, v, data in edges)
    for u, v, data in edges:
      data['weight'] /= z


if __name__ == '__main__':
  G = read_input(sys.stdin)
  normalize_outgoing(G)
  for n in G.nodes():
    print 'n = {} has\n {}\n'.format(n, G.out_edges(n, data=True))

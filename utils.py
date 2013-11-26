from __future__ import division
import sys
##
import networkx as nx
import numpy as np
##
from collections import defaultdict
from scipy.stats import powerlaw


def read_input(data):
  G = nx.DiGraph()
  for line in data:
    a, b = map(int, line.strip().split(' -> '))
    G.add_node(a)
    G.add_node(a)
    # DiGraph doesn't allow duplicate edges
    G.add_edge(a, b)
  return G


def set_edge_weights(G, f=lambda: 1):
  for u, v, data in G.edges_iter(data=True):
    data['weight'] = f()


def normalize_outgoing(G):
  for n in G.nodes_iter():
    edges = G.out_edges(n, data=True)
    z = sum(data['weight'] for u, v, data in edges)
    for u, v, data in edges:
      data['weight'] /= z


def powerlaw_visits(a=0.2, size=100, scalar=10000):
  # This is a bad approximation but is meant for temporary testing
  return map(int, map(round, sorted(powerlaw.rvs(a, size=size) * scalar)))


def create_sample(G, shuffled=False):
  n = G.number_of_nodes()
  powers = powerlaw_visits(size=n)
  if shuffled:
    np.random.shuffle(powers)
  for n, incoming in zip(G.nodes(), powers):
    G.node[n]['enter'] = incoming
    G.node[n]['pageviews'] = incoming


def generate_pageviews(G, loops=30):
  # Initialize the 'on page' count with the node's 'enter'
  for n in G.nodes():
    G.node[n]['on_page'] = G.node[n]['enter']
    G.node[n]['pageviews'] = G.node[n]['enter']
  # 'Walk' the users through the graph
  for loop in xrange(loops):
    new_pv = defaultdict(int)
    # If there are no more active users, we may exit
    if loop and sum(G.node[n]['on_page'] for n in G.nodes()) == 0:
      break
    for n in G.nodes():
      # Collect all the visitors from parent nodes
      for u, v, data in G.in_edges(n, data=True):
        new_pv[v] += int(data['weight'] * (G.node[u]['on_page'] * 0.85))
    # Place the new page views onto the graph
    for n in G.nodes():
      pv = new_pv[n]
      G.node[n]['on_page'] = pv
      G.node[n]['pageviews'] += pv


def copy_graph_attrs(X, Y, node_attrs=[], edge_attrs=[]):
  for u, v, data in X.edges_iter(data=True):
    for attr in edge_attrs:
      Y[u][v][attr] = data[attr]
  for n, data in X.nodes_iter(data=True):
    for attr in node_attrs:
      Y.node[n][attr] = data[attr]


def reset_graph_attrs(G, node_attrs=[], edge_attrs=[]):
  for u, v, data in G.edges_iter(data=True):
    for attr in edge_attrs:
      del G[u][v][attr]
  for n, data in G.nodes_iter(data=True):
    for attr in node_attrs:
      del G.node[n][attr]


def display_graph(G):
  for n, data in G.nodes(data=True):
    print 'n = {} ({}) has edges {}'.format(n, data, G.in_edges(n, data=True))


if __name__ == '__main__':
  # This is the definitive graph with definitive edge weights
  G = read_input(sys.stdin)
  set_edge_weights(G, lambda: np.random.randint(1, 1000))
  normalize_outgoing(G)

  # Let's create a copy cat and set the edges to all evenly distributed
  approxG = G.copy()
  set_edge_weights(approxG)
  normalize_outgoing(approxG)

  # Create a correct sample of 'enter' and 'pageviews' from G
  create_sample(G)
  generate_pageviews(G)

  copy_graph_attrs(G, approxG, ['enter'])

  generate_pageviews(approxG)

  print 'Pageviews from "real" edge weights'
  print '-=-=-=-=-'
  display_graph(G)
  print
  print 'Pageviews from evenly distributed edge weights'
  print '-=-=-=-=-'
  display_graph(approxG)

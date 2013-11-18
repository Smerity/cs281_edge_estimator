from __future__ import division
import sys
##
import networkx as nx
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
    G.add_edge(a, b, weight=1)
  return G


def normalize_outgoing(G):
  for n in G.nodes_iter():
    edges = G.out_edges(n, data=True)
    z = sum(data['weight'] for u, v, data in edges)
    for u, v, data in edges:
      data['weight'] /= z


def powerlaw_visits(a=0.2, size=100, scalar=10000):
  # This is a bad approximation but is meant for temporary testing
  return map(int, map(round, sorted(powerlaw.rvs(a, size=size) * scalar)))


def create_sample(G):
  n = G.number_of_nodes()
  for n, incoming in zip(G.nodes(), powerlaw_visits(size=n)):
    G.node[n]['iter_pageviews'] = incoming
    G.node[n]['pageviews'] = incoming


def generate_pageviews(G, loops=30):
  for loop in xrange(loops):
    new_pv = defaultdict(int)
    # If there are no more active users, we may exit
    if loop and sum(G.node[n]['iter_pageviews'] for n in G.nodes()) == 0:
      break
    for n in G.nodes():
      # Collect all the visitors from parent nodes
      for u, v, data in G.in_edges(n, data=True):
        new_pv[v] += int(data['weight'] * (G.node[u]['iter_pageviews'] * 0.85))
    # Place the new page views onto the graph
    for n in G.nodes():
      pv = new_pv[n]
      G.node[n]['iter_pageviews'] = pv
      G.node[n]['pageviews'] += pv


if __name__ == '__main__':
  G = read_input(sys.stdin)
  normalize_outgoing(G)
  create_sample(G)
  print 'Before visitors walk around graph (i.e. only incoming visitors)...'
  for n, data in G.nodes(data=True):
    print 'n = {} ({}) has edges {}'.format(n, data, G.in_edges(n, data=True))
  print '---'
  generate_pageviews(G)
  print 'After visitors walk around graph...'
  for n, data in G.nodes(data=True):
    print 'n = {} ({}) has edges {}'.format(n, data, G.in_edges(n, data=True))

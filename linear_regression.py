from __future__ import division
from utils import *
import prettyplotlib as ppl
from prettyplotlib import plt


if __name__ == '__main__':
  shuffled = False
  # This is the definitive graph with definitive edge weights
  G = read_input(sys.stdin)
  set_edge_weights(G, lambda: np.random.randint(1, 1000))
  normalize_outgoing(G)

  # Let's create a copy cat and set the edges to all evenly distributed
  approxG = G.copy()
  set_edge_weights(approxG)
  normalize_outgoing(approxG)

  # Create a correct sample of 'enter' and 'pageviews' from G
  create_sample(G, shuffled=shuffled)
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

  fig, ax = plt.subplots(1)
  orig_weight_data = np.arange(0, G.number_of_edges()), [abs(G[u][v]['weight'] - approxG[u][v]['weight']) for u, v in G.edges()]
  ppl.bar(ax, *orig_weight_data, grid='y')
  #plt.ylim(-1, 1)
  #plt.show(block=True)

  # Let's try to reduce the error
  nodes = sorted(G.nodes())
  total_loops = 100
  rerrs = []
  werrs = []
  for i in xrange(total_loops):
    if i % 5 == 0:
      print '{} of {}'.format(i, total_loops)
    for mod_node in nodes:
      # Create a correct sample of 'enter' and 'pageviews' from G
      create_sample(G, shuffled=shuffled)
      generate_pageviews(G)

      copy_graph_attrs(G, approxG, ['enter'])
      generate_pageviews(approxG)

      rerr = sum(abs(approxG.node[n]['pageviews'] - G.node[n]['pageviews']) / (G.node[n]['pageviews'] + 1) for n in G.nodes()) / G.number_of_nodes()
      rerrs.append(rerr)
      #
      werr = sum(abs(G[u][v]['weight'] - approxG[u][v]['weight']) for u, v in G.edges()) / G.number_of_edges()
      werrs.append(werr)
      #
      if i % 5 == 0 and mod_node == 1:
        print 'RErr:', rerr
        print 'WErr:', werr

      delta = 0.0005
      #delta = 0.01
      if False:
        # Shift a node more towards the correct solution
        err = -1 if G.node[mod_node]['pageviews'] - approxG.node[mod_node]['pageviews'] > 0 else 1
        #sign = 1 if err > 0 else -1
        # For each of the parents of the node, request more or less weight
        for u, v, data in approxG.in_edges(mod_node, data=True):
          data['weight'] = max(0, data['weight'] - err * delta)
      else:
        prev_rerr = None
        while prev_rerr is None or rerr < prev_rerr:
          # Shift a node more towards the correct solution
          err = -1 if G.node[mod_node]['pageviews'] - approxG.node[mod_node]['pageviews'] > 0 else 1
          #sign = 1 if err > 0 else -1
          # For each of the parents of the node, request more or less weight
          for u, v, data in approxG.in_edges(mod_node, data=True):
            data['weight'] = max(0, data['weight'] - err * delta)
          normalize_outgoing(approxG)
          ##
          #copy_graph_attrs(G, approxG, ['enter'])
          generate_pageviews(approxG)
          prev_rerr = rerr
          rerr = sum(abs(approxG.node[n]['pageviews'] - G.node[n]['pageviews']) / (G.node[n]['pageviews'] + 1) for n in G.nodes()) / G.number_of_nodes()

    np.random.shuffle(nodes)

  print 'Pageviews from "real" edge weights'
  print '-=-=-=-=-'
  display_graph(G)
  print
  print 'Pageviews from evenly distributed edge weights'
  print '-=-=-=-=-'
  display_graph(approxG)

  plt.plot(np.arange(0, len(rerrs)), rerrs, label='Relative error over time')
  plt.xlabel('Iteration')
  plt.ylabel('Average pageview relative error per node')
  plt.legend()
  plt.savefig('error_over_time.pdf')
  plt.show(block=True)

  plt.plot(np.arange(0, len(werrs)), werrs, label='Weight error over time')
  plt.xlabel('Iteration')
  plt.ylabel('Average weight error per edge')
  plt.legend()
  plt.savefig('weight_over_time.pdf')
  plt.show(block=True)

  fig, ax = plt.subplots(1)
  ppl.bar(ax, *orig_weight_data, alpha=0.5, color='black', label='Weight error before')
  ppl.bar(ax, np.arange(0, G.number_of_edges()), [abs(G[u][v]['weight'] - approxG[u][v]['weight']) for u, v in G.edges()], alpha=0.8, label='Weight error after')
  #plt.ylim(-1, 1)
  plt.legend(loc='best')
  plt.show(block=True)

from prettyplotlib import plt
##
import sys

if __name__ == '__main__':
  # Accumulate the counts fed into standard in (stdin)
  counts = []
  for line in sys.stdin:
    topic, count = line.split()
    # Shift the ones up by a tiny amount to allow them to be visible on the graph
    counts.append(int(count) + 0.05)

  print 'Total page view counts: {}'.format(len(counts))

  # Display the hourly page view distribution on a log-log plot
  # This matches our friendly and well understood Zipf distribution
  fig = plt.figure(figsize=(9, 5))
  ax = fig.add_subplot(1, 1, 1)
  plt.plot(xrange(len(counts)), counts, linewidth=3, label='Pageviews per page')
  #
  ax.set_xscale('log')
  ax.set_yscale('log')
  #
  plt.title('Log-log plot of hourly Wikipedia page view distribution')
  plt.xlabel('Rank order')
  plt.ylabel('Frequency')
  plt.grid(color='black')
  plt.legend()
  #
  plt.savefig('hourly_wikipedia_zipf.pdf')
  plt.show(block=True)

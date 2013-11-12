from prettyplotlib import plt
##
import sys

if __name__ == '__main__':
  # Accumulate the counts fed into standard in (stdin)
  counts = []
  for line in sys.stdin:
    topic, count = line.split()
    counts.append(int(count))

  print 'Total page view counts: {}'.format(len(counts))

  # Display the hourly page view distribution on a log-log plot
  # This matches our friendly and well understood Zipf distribution
  fig = plt.figure()
  ax = fig.add_subplot(1, 1, 1)
  plt.plot(range(len(counts)), counts)
  #
  ax.set_xscale('log')
  ax.set_yscale('log')
  #
  plt.title('Plot of hourly Wikipedia page view distribution')
  plt.xlabel('Rank order')
  plt.ylabel('Frequency')
  #
  plt.savefig('hourly_wikipedia_zipf.pdf')
  plt.show(block=True)

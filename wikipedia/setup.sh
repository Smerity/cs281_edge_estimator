#!/bin/bash
wget http://dumps.wikimedia.org/other/pagecounts-raw/2013/2013-09/pagecounts-20130916-000000.gz
zcat pagecounts-20130916-000000.gz | grep '^en ' | pv | cut -d ' ' -f 3,2 | sort -rnk 2 > pagecounts-20130916-000000_sorted.txt
python graph_pageviews.py < pagecounts-20130916-000000_sorted.txt

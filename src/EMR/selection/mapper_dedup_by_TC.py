#!/usr/bin/env python

import sys
import datetime as dt

NEWS_TIMEFORMAT = "%Y-%m-%d %H:%M:%S"

def main(separator='\t'):
        
    # input comes from STDIN (standard input)
    for line in sys.stdin:
        line = line.strip()
        if len(line)==0:
            continue
        ID, url, date, title, content=line.split('\t')
        print "%s\t%s\t%s\t%s" % (title+':+:'+content, ID, url, date)
if __name__ == "__main__":
    main()

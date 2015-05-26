#!/usr/bin/env python

import sys
import datetime as dt

NEWS_TIMEFORMAT = "%Y-%m-%d %H:%M:%S"

def main(separator='\t'):
    cur_TC=''
    # input comes from STDIN (standard input)
    for line in sys.stdin:
        line = line.strip()
        TC, ID, url, date=line.split('\t')
        if TC==cur_TC:
            continue
        else:
            cur_TC=TC
            title, content=TC.split(':+:')
            print "%s\t%s\t%s\t%s\t%s" % (ID, url, date, title, content)
if __name__ == "__main__":
    main()

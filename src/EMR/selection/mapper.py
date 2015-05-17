#!/usr/bin/env python

import sys

counter = 0
flag = False

# input comes from STDIN (standard input)
for line in sys.stdin:
    # remove leading and trailing whitespace
    line = line.strip()
    # split the line into words
    fields = line.split('\t')
    if len(fields)==0:
        continue
    key = fields[0].strip()
    value=fields[-1].strip()
    if key=='I':
        counter+=1
        flag=True
    
    if key=='S':
        if value!='en':
            flag=False
            continue
    if key=='U' or key=='D' or key=='T' or key=='C':
        if flag==False:
            continue
    if key!='Q' and key!='C':
        print '%s\t%s' % (str(counter), key+':'+value)
    
    # increase counters
    # write the results to STDOUT (standard output);
    # what we output here will be the input for the
    # Reduce step, i.e. the input for reducer.py
    #
    # tab-delimited; the trivial word count is 1

        

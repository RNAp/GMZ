import sys

for line in sys.stdin:
    
    # remove leading and trailing whitespace
    line = line.strip()

    # parse the input we got from mapper.py
    key, ar = line.split('\t', 1)

    print '%s\t%s' % (key, ar)

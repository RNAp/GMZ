from findSeed import findSeed
import datetime as dt

date = "2013-02-01 00:00:00"
NEWS_TIMEFORMAT = "%Y-%m-%d %H:%M:%S"

timestamp = dt.datetime.strptime(date.strip(), NEWS_TIMEFORMAT)

filename = "articles_qdotsNanoPhoto_all_no_dup.txt"
key  = ["mit", "jean"]


seed = findSeed(filename, key, timestamp )

if seed is not None:
    print seed.get('id', None)
else:
    print "seed not found!"

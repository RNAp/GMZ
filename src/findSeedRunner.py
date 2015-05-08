from findSeed import findSeed
import datetime as dt
import tfidf
NEWS_TIMEFORMAT = "%Y-%m-%d %H:%M:%S"

date = "2011-12-01 00:00:00"
pubTitle = "Nanowire-based single-cell endoscopy"
institution = 'lawrence berkeley'
author = 'peidong yang'
filename = "qdots_all_nono_dup.txt"

idfFileName = "40NoDupNoPunc_idf.txt"
stopwordFileName = "mysql_stop.txt"
print "initializing corpus idf"
ti = tfidf.TfIdf(idfFileName,stopwordFileName)
print "finding topwords in publication title"
wordTfIdf = ti.get_doc_keywords(pubTitle)
for topWords, topTfIdf in wordTfIdf:
    print ('%s\t%f\n' % (topWords,round(topTfIdf,5)))

print "searching for seed news"
timestamp = dt.datetime.strptime(date.strip(), NEWS_TIMEFORMAT)
topWordsInPubTitle = [x[0] for x in wordTfIdf]
startI = 0
stepI = 1
endI = 1

print "1. use institution and/or author as the keywords"
key = [institution, author]
for x in key:
    print x
seed1 = findSeed(filename, key, timestamp)

if seed1 is not None:
    print seed1.get('id', None)

print "2. search again by adding top words"
key = [institution, author] + topWordsInPubTitle[startI:endI:stepI]
for x in key:
    print x
seed2 = findSeed(filename, key, timestamp)
if seed2 is not None:
    print ('Use top %d word, seed id is %s') % (endI, seed2.get('id', None))

if seed1 is None or seed2 is None:
    print "3. seed not found yet, try just top words"
    key = topWordsInPubTitle[startI:endI:stepI]
    for x in key:
        print x
    seed3 = findSeed(filename, key, timestamp)
    if seed3 is not None:
        print ('Use top %d word, seed id is %s') % (endI, seed3.get('id', None))
    else:
        print "seed not found!"

from findSeed import findSeed
import datetime as dt
import tfidf
NEWS_TIMEFORMAT = "%Y-%m-%d %H:%M:%S"

date = "2012-06-28 00:00:00"
pubTitle = "A Programmable Dual-RNA-Guided DNA Endonuclease in Adaptive Bacterial Immunity"
institution = 'berkeley'
author = 'jinek'
filename = "CRISPR_all_nono_dup.txt"

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
startI = 1
stepI = 1
endI = 2

print "first use institution as the keywords"
key = [institution]
seed = findSeed(filename, key, timestamp)

if seed is not None:
    print seed.get('id', None)
else:
    print "seed not found using institution and/or author, try top words"
    key = topWordsInPubTitle[startI:endI:stepI]
    seed = findSeed(filename, key, timestamp)
    if seed is not None:
        print ('Use top %d word, seed id is %s') % (endI, seed.get('id', None))
    else:
        print "seed not found!"

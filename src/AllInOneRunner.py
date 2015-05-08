__author__ = 'Yangye_Zhu'

from writeFile import ArticleWriter
from readFile import ArticleReader
from selectedArticle import SelectedArticle
from selection import select_by_date
import datetime as dt
import shingleSim as shsim
import tfidf
import math
NEWS_TIMEFORMAT = "%Y-%m-%d %H:%M:%S"

topic = 'qdots'
seedID = '2011122022_00034712_W'
seedNewsDate = "2011-12-15 07:00:00"

sourceFileName = topic + '_all_nono_dup.txt'
allForSimFileName = topic + '_all_nono_dup_closedate_noKey_' + seedID + '.txt'
idDateForSimFileName = topic + '_id_date_nono_dup_closedate_noKey_' + seedID + '.txt'
seedNewsWordTfidfFileName = topic + '_nono_dup_seed_top_words_tfidf_' + seedID + '.txt'
shingleFileName = topic + '_closedate_noKey_shingleSim_' + seedID + '.txt'
vsmFileName = topic + '_from40_closedate_noKey_vsmSim_' + seedID + '.txt'

print "reading source file"
ar = ArticleReader()
ar.readFile(sourceFileName)

print "select by date"
sr = SelectedArticle()
timestamp = dt.datetime.strptime(seedNewsDate.strip(), NEWS_TIMEFORMAT)
date_before = dt.timedelta(days=7)
date_after = dt.timedelta(days=31)
sr = select_by_date(ar, sr, timestamp - date_before, date_after)

print 'writing date filtered files for similarity calculations'
aw = ArticleWriter(sr.getArticleList())
aw.writeFile(allForSimFileName)
aw.writeIDDate(idDateForSimFileName)
print ('find %d articles' % len(sr.getArticleList()))

print "reading date filtered file"
ar = ArticleReader()
ar.readFile(allForSimFileName)    # readFile or readFileMoreFiltering

print "initializing corpus idf"
idfFileName = "40NoDupNoPunc_idf.txt"
stopwordFileName = "mysql_stop.txt"
ti = tfidf.TfIdf(idfFileName,stopwordFileName)

print "writing seed word tfidf file"
tol = 1e-6
seedTopWordTfIdf = []
seedNorm = 0.0
with open(seedNewsWordTfidfFileName,'w') as f:
    for a in ar.getArticleList():
        if seedID == a['id'].strip():
            wordTfIdf = ti.get_doc_keywords(a['content'])
            for topWords, topTfIdf in wordTfIdf:
                f.write('%s\t%f\n' % (topWords,round(topTfIdf,5)))
                seedNorm += topTfIdf**2
            seedTopWordTfIdf = [(w,tff) for w, tff in wordTfIdf if tff > tol]
            break
f.close()

print "get seed set"
seedSet = shsim.getSeedSet(seedID, ar)

print "write shingling similarity score"
shsim.writeSimScores(seedID, seedSet, ar, shingleFileName)

print "writing vsm similarity score"
with open(vsmFileName,'w') as f:
    for a in ar.getArticleList():
        wordTfIdf = ti.get_doc_keywords(a['content'])

        f.write('%s\t' % a['id'].strip())
        f.write('%s\t' % a['date'].strftime(NEWS_TIMEFORMAT))
        f.write('%s\t' % a['url'].strip())
        aNorm = 0.0
        vsmSim = 0.0
        wordTfIdf = [(w,tff) for w, tff in wordTfIdf if tff > tol]
        for w, tff in wordTfIdf:
            aNorm += tff**2
            for sw, stff in seedTopWordTfIdf:
                if sw.strip() == w.strip():
                    vsmSim += stff * tff
        vsmSim /= (math.sqrt(aNorm) * math.sqrt(seedNorm))
        f.write('%f\n' % round(vsmSim, 5))
f.close()
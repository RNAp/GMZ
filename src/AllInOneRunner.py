__author__ = 'Yangye_Zhu'

from writeFile import ArticleWriter
from readFile import ArticleReader
from selectedArticle import SelectedArticle
from selection import select_by_date
from lsh import *
import datetime as dt
import shingleSim as shsim
import FormatArticles as fa
import tfidf
import math
NEWS_TIMEFORMAT = "%Y-%m-%d %H:%M:%S"

topic = '2015Q1_hedgehog4KeyWords'
seedID = '2015020123_00030147_W'
seedNewsDate = "2015-02-02 01:02:38"

sourceFileName = topic + '.txt'
allForSimFileName = topic + '_all_nodup_closedate_' + seedID + '.txt'
idDateForSimFileName = topic + '_id_date_nodup_closedate_' + seedID + '.txt'
seedNewsWordTfidfFileName = topic + '_nodup_seed_top_words_tfidf_' + seedID + '.txt'
closedateNewsFile = topic + '_closedate_id_date_url_vsm_shingle_' + seedID + '.txt'
# shingleFileName = topic + '_closedate_noKey_shingleSim_' + seedID + '.txt'
# vsmFileName = topic + '_from40_closedate_noKey_vsmSim_' + seedID + '.txt'

print "reading source file"
ar = ArticleReader()
ar.readFileFast(sourceFileName)

print "select by date"
sr = SelectedArticle()
timestamp = dt.datetime.strptime(seedNewsDate.strip(), NEWS_TIMEFORMAT)
date_before = dt.timedelta(days=3)
date_after = dt.timedelta(days=14)
sr = select_by_date(ar, sr, timestamp - date_before, date_after)

print "writing non-deduplicated date filtered file first"
aw = ArticleWriter(sr.getArticleList())
aw.writeFile(allForSimFileName)

print "reading non-deduplicated date filtered file and deduplicate it"
ar = ArticleReader()
ar.readFileFastMoreFiltering(allForSimFileName)    # readFile or readFileMoreFiltering

print 'writing deduplicated date filtered files for similarity calculations'
aw = ArticleWriter(ar.getArticleList())
aw.writeFile(allForSimFileName)
aw.writeIDDate(idDateForSimFileName)
print ('find %d articles' % len(ar.getArticleList()))

# print "uncomment this to avoid the MemoryError"
# ar = ArticleReader()
# ar.readFileFast(allForSimFileName)

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

# print "write shingling similarity score"
# shsim.writeSimScores(seedID, seedSet, ar, shingleFileName)

print "writing two similarity scores"
K_WORD = 3
with open(closedateNewsFile,'w') as f:
    for a in ar.getArticleList():
        wordTfIdf = ti.get_doc_keywords(a['content'])
        cur_c = fa.convert_to_match_array(a['content'])

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
        f.write('%f\t' % round(vsmSim, 5))
        f.write('%f\n' % shsim.calSignatureSimilarity(seedSet, set(hmultiWshingle(cur_c, K_WORD, fa.load_stopword_set()))))

f.close()
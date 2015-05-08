__author__ = 'Yangye_Zhu'

from readFile import ArticleReader
import math
import tfidf

NEWS_TIMEFORMAT = "%Y-%m-%d %H:%M:%S"

# Prepare the file names:
inputFileName = "CRISPR_all_nono_dup_closeMITdate_noKey.txt"
outputIdDateFileName = "CRISPR_id_date_nono_dup_from40_closeMITdate_noKey_vsmSim.txt"
idfFileName = "40NoDupNoPunc_idf.txt"
seedNewsWordTfidfFileName = "CRISPRCas9_nono_dup_seed_top_words_tfidf.txt"
seedID = "2013121303_00036748_W"

stopwordFileName = "mysql_stop.txt"
# topNumber = 107
tol = 1e-6

print "reading input file"
ar = ArticleReader()
ar.readFile(inputFileName)    # readFile or readFileMoreFiltering

print "reading words and tfidf of seed news"
seedWordTfIdf = []
seedNorm = 0.0
# count = 0
with open(seedNewsWordTfidfFileName) as f:
    for line in f:
        wtff = []
        fields = line.split('\t')
        w = fields[0].strip()
        wtff.append(w)
        tff = float(fields[1])
        wtff.append(tff)
        seedWordTfIdf.append(tuple(wtff))
        # count += 1
        # if count <= topNumber:
        seedNorm += tff**2
f.close()
seedTopWordTfIdf = [(w,tff) for w, tff in seedWordTfIdf if tff > tol]

print "initializing corpus idf"
ti = tfidf.TfIdf(idfFileName,stopwordFileName) # idfFile is None at the beginning

print "writing files"
with open(outputIdDateFileName,'w') as f:
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

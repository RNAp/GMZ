__author__ = 'Yangye_Zhu'

from readFile import ArticleReader
from writeFile import ArticleWriter
import tfidf
import pickle

NEWS_TIMEFORMAT = "%Y-%m-%d %H:%M:%S"

# Prepare the file names
#  articles_CRISPR_all_without_duplicates 4760, no dup number
# articles_higgs_all 102952, no dup number
# articles_qdots_all_without_duplicates 37460, no dup number
#  articles_deepL_all_with_duplicates 15697, no dup number

inputFileName = "CRISPR_all_nono_dup_closeMITdate_Cas9.txt"
outputIdDateFileName = "qdotsNRL_id_date_nono_dup_numSeedWords_withWords_By50.txt"
idfFileName = "40NoDupNoPunc_idf.txt"
savedWordTfidfFileName = "CRISPRCas9_nono_dup_seed_top_words_tfidf.txt"
seedNewsWordTfidfFileName = "CRISPRCas9_nono_dup_seed_top_words_tfidf.txt"
seedID = "2013121303_00036748_W"

stopwordFileName = "mysql_stop.txt"
topNumber = 50

print "reading input file"
ar = ArticleReader()
ar.readFile(inputFileName)    # readFile or readFileMoreFiltering
articleList = ar.getArticleList()

# print "reading top words of seed news"
# seedTopWords = []
# with open(seedNewsWordTfidfFileName) as f:
#     for line in f:
#         fields = line.split('\t')
#         seedTopWords.append(fields[0].strip())
# f.close()
# seedTopWordsSet = set(seedTopWords[:topNumber])

print "initializing corpus idf"
ti = tfidf.TfIdf(idfFileName,stopwordFileName) # idfFile is None at the beginning

# print "saving idf and stopword to files"
# ti.save_corpus_to_file(idfFileName,savedStopwordFileName) # after this, you can call "ti = tfidf.TfIdf(idfFileName,stopwordFileName)" when initializing

print "writing files"
with open(savedWordTfidfFileName,'w') as f:
    for a in articleList:
        if seedID == a['id'].strip():
            wordTfIdf = ti.get_doc_keywords(a['content'])
        # topWordsSet = set([x[0] for x in wordTfIdf[:topNumber]])

            for topWords, topTfIdf in wordTfIdf:
                f.write('%s\t%f\n' % (topWords,round(topTfIdf,5)))
            break

        # f.write('%s\t' % a['id'].strip())
        # f.write('%s\t' % a['date'].strftime(NEWS_TIMEFORMAT))
        # f.write('%s\t' % a['url'].strip())
        # overlapSet = seedTopWordsSet & topWordsSet
        # f.write('%f\t' % round(len(overlapSet)/float(topNumber), 5))
        # f.write('%s\n' % '_'.join(overlapSet))

f.close()

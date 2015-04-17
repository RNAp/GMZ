__author__ = 'Yangye_Zhu'

from readFile import ArticleReader
from writeFile import ArticleWriter
import tfidf
import pickle

NEWS_TIMEFORMAT = "%Y-%m-%d %H:%M:%S"

inputFileName = "articles_higgs_all_without_duplicates_part1.txt"
pickleName = "higgs_no_dup_part1.pickle"
outputIdDateFileName = "articles_higgs_id_date_no_dup_topK_part1.txt"
outputAllFileName = "articles_higgs_all_no_dup_topK_part1.txt"
idfFileName = "higgs_no_dup_part1_idf.txt"
savedStopwordFileName = "higgs_no_dup_part1_stop_word.txt"
savedWordTfidfFileName = "higgs_no_dup_part1_seed_top_words_tfidf.txt"
keywords = ['higgs','boson']
seedID = "2012070412_00058390_W"

stopwordFileName = "mysql_stop.txt"
topNumber = 50

print "reading input file"
# ar = ArticleReader()
# ar.readFileNoFilter(inputFileName)    # readFile or readFileNoFilter
# print "saving pickle"
# with open(pickleName,'w') as f:
#     pickle.dump(ar.getArticleList(),f)
# articleList = ar.getArticleList()


with open(pickleName) as f:
    articleList = pickle.load(f)


print "initializing corpus idf"
ti = tfidf.TfIdf(idfFileName,stopwordFileName)

# for a in articleList:
#     if a.get('content',None) is not None:
#         ti.add_input_document(a['content'])
# print "saving corpus and stopword to files"
# ti.save_corpus_to_file(idfFileName,savedStopwordFileName)

print "writing files"
# importantAL = []
with open(savedWordTfidfFileName,'w') as f:
    for a in articleList:
        if seedID == a['id'].strip():
            wordTfIdf = ti.get_doc_keywords(a['content'])
            # topWords = [x[0] for x in wordTfIdf[:topNumber]]
            # topTfIdf = [x[1] for x in wordTfIdf[:topNumber]]
            # for k in keywords:
            #     if k.lower() in topWords:
            #         importantAL.append(a)
            #         f.write('%s\t' % a['id'].strip())
            #         f.write('%s\t' % a['date'].strftime(NEWS_TIMEFORMAT))
            #         f.write('%s\n' % '-'.join(topKeywords))
            #         break
            for topWords, topTfIdf in wordTfIdf:
                f.write('%s\t%f\n' % (topWords,round(topTfIdf,5)))
            break

    f.close()

# aw = ArticleWriter(importantAL)
# aw.writeFile(outputAllFileName)
__author__ = 'Yangye_Zhu'

from readFile import ArticleReader
import tfidf

NEWS_TIMEFORMAT = "%Y-%m-%d %H:%M:%S"

# Prepare the file names
inputFileName = "articles_higgsPhyCern_all_no_dup.txt"

pickleName = "higgs_no_dup_part1.pickle"
outputIdDateFileName = "articles_higgs_id_date_no_dup_topK_part1.txt"
outputAllFileName = "articles_higgs_all_no_dup_topK_part1.txt"
idfFileName = "40withdup_idf.txt"
savedStopwordFileName = "higgs_no_dup_part1_stop_word.txt"
savedWordTfidfFileName = "higgs_no_dup_part1_newseed_top_words_tfidf.txt"
keywords = ['higgs','boson']
seedID = "2012070411_00030420_W"

stopwordFileName = "mysql_stop.txt"
topNumber = 50

print "reading input file"
ar = ArticleReader()
ar.readFile(inputFileName)    # readFile or readFileMoreFiltering
articleList = ar.getArticleList()

print "initializing corpus idf"
ti = tfidf.TfIdf(None,stopwordFileName) # idfFile is None at the beginning

for a in articleList:
    if a.get('content',None) is not None:
        ti.add_input_document(a['content'])
print "saving idf and stopword to files"
ti.save_corpus_to_file(idfFileName,savedStopwordFileName) # after this, you can call "ti = tfidf.TfIdf(idfFileName,stopwordFileName)" when initializing

print "writing files"
with open(savedWordTfidfFileName,'w') as f:
    for a in articleList:
        if seedID == a['id'].strip():
            wordTfIdf = ti.get_doc_keywords(a['content'])
            for topWords, topTfIdf in wordTfIdf:
                f.write('%s\t%f\n' % (topWords,round(topTfIdf,5)))
            break

    f.close()

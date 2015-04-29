from readFile import ArticleReader
import tfidf
import selection

NEWS_TIMEFORMAT = "%Y-%m-%d %H:%M:%S"

# Prepare the file names
inputFileName = "articles_qdots_all_without_duplicates.txt"
idfFileName = "40withdup_idf.txt"
#savedStopwordFileName = "stopwordfile.txt"
savedWordTfidfFileName = "qdot_test.txt"
seedID = "2013032709_00001367_W"

stopwordFileName = "mysql_stop.txt"
topNumber = 20
threshold=10.0

print "reading input file"
ar = ArticleReader()
ar.readFile(inputFileName)    # readFile or readFileMoreFiltering
articleList = ar.getArticleList()
#
# print "initializing corpus idf"
# ti = tfidf.TfIdf(None,stopwordFileName) # idfFile is None at the beginning
#
# for a in articleList:
#     if a.get('content',None) is not None:
#         ti.add_input_document(a['content'])
# print "saving idf and stopword to files"
# ti.save_corpus_to_file(idfFileName,savedStopwordFileName) # after this, you can call "ti = tfidf.TfIdf(idfFileName,stopwordFileName)" when initializing

ti = tfidf.TfIdf(idfFileName,stopwordFileName)
print "writing files"
with open(savedWordTfidfFileName,'w') as f:
    for a in articleList:
        if seedID == a['id'].strip():
            print seedID
            f.write('ID:%s' % a['id'])
            f.write('Date:%s' % a['date'])
            wordTfIdf = ti.get_doc_keywords(a['content'])
            count=0
            for topWords, topTfIdf in wordTfIdf:
                cur_loc=selection.find_keyword_location(topWords, a['content'])
                if cur_loc>0 and cur_loc<threshold:
                   f.write('%s\t%f\n' % (topWords,round(topTfIdf,5)))
                   count=count+1
                if count is topNumber:
                   break

    f.close()
print "complete"
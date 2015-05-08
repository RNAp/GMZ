from readFile import ArticleReader
import tfidf
import selection

NEWS_TIMEFORMAT = "%Y-%m-%d %H:%M:%S"

# Prepare the file names
inputFileName = "qdotsNanoPhoto_all_nono_dup.txt"
idfFileName = "40NoDupNoPunc_idf.txt"
#savedStopwordFileName = "stopwordfile.txt"
savedWordTfidfFileName = "qdot_MIT_10topwords_loaction_filter.txt"
seedID = "2013032709_00001367_W"

stopwordFileName = "mysql_stop.txt"
topNumber = 10
threshold=0.3

print "reading input file"
ar = ArticleReader()
ar.readFile(inputFileName)    # readFile or readFileMoreFiltering
articleList = ar.getArticleList()

ti = tfidf.TfIdf(idfFileName,stopwordFileName)
print "writing files"
seed_keywords=[]

for a in articleList:
    if seedID == a['id'].strip():
       wordTfIdf = ti.get_doc_keywords(a['content'])
       count=0
       for topWords, topTfIdf in wordTfIdf:
           cur_loc=selection.find_keyword_location(topWords, a['content'])
           if cur_loc>0 and cur_loc<threshold:
               seed_keywords.append(topWords)
               count=count+1
           if count is topNumber:
                break
seed_keywords=set(seed_keywords)
print "Complete seed keywords set"


with open(savedWordTfidfFileName,'w') as f:
    for a in articleList:
        cur_keywords=set()
        wordTfIdf = ti.get_doc_keywords(a['content'])
        count=0
        for topWords, topTfIdf in wordTfIdf:
            cur_loc=selection.find_keyword_location(topWords, a['content'])
            if cur_loc>0 and cur_loc<threshold:
                #f.write('%s\t%f\n' % (topWords,round(topTfIdf,5)))
                cur_keywords.add(topWords)
                count=count+1
            if count is topNumber:
                break
        overlap_score=len(cur_keywords.intersection(seed_keywords))*1.0/topNumber
        f.write('%s\t%s\t%s\t%f\n' % (a['id'].strip(),a['date'],a['url'].strip(),overlap_score))

    f.close()


print "complete"
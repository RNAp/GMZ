'''
The purpose of this code is to implement methods for identifying seed news from raw/extracted raw data. The APIs are defined as follows:



'''


from readFile import ArticleReader
import datetime as dt
import selectedArticle as SA
import selection as sel




def findSeed(filename = None, key = [], date = None):
    ar = ArticleReader()
    
    try:
        ar.readFile(filename)
    except filename == None:
        print "filename error!"
        return -1

    ar.sortArticleByDate() # sort articles by date first
    
    sr = SA.SelectedArticle()

    
    try:
        sr = sel.select_by_date(ar, sr, date, date_range = dt.timedelta(days=90))
    except date == None:
        print "Please specify date!!!"
        return -1

    try:
        sr = sel.select_by_keywords(sr, SA.SelectedArticle(), key, verbose = 'all')
    except key == []:
        print "no keywords specified!"

    if len(sr.articleList) != 0: 
        seedNews = sr.articleList[0]
    else:
        seedNews = None
    return seedNews

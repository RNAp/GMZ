'''
ArticleReader API:

readFile - Given a spinn3r file, read in a list of article dictionary. Each article dictionary has at most five keys: url, date, title, content, and quotes, where the value of date is a datetime object and the value of quotes is a list.
getArticleList - Get the list of articles
sortArticleByDate - Sort the articles by date
'''

import datetime as dt 

NEWS_TIMEFORMAT = "%Y-%m-%d %H:%M:%S"

class ArticleReader(object):

    def __init__(self):
        self.articleList = []
      
    # the following methods were added due to modifications in SelectedArticle class by MC
    def keyWordsSource(self):
        return None

    def urlSource(self):
        return None

    def dateRange(self):
        return None
      
    def readFile(self, filename):
        f = open(filename)
        for line in f:
            fields = line.split('\t')
            if len(fields) == 0:
                continue
            key = fields[0]
            value = fields[-1]
            if key == 'I':
                newArticle = {}
                newArticle['id'] = value
                self.articleList.append(newArticle)
            if key == 'U':
                self.articleList[-1]['url'] = value
            if key == 'D':
                self.articleList[-1]['date'] = dt.datetime.strptime(value.strip(), NEWS_TIMEFORMAT)
            if key == 'T':
                self.articleList[-1]['title'] = value
            if key == 'C':
                self.articleList[-1]['content'] = value
            if key == 'Q':
                quoteList = self.articleList[-1].get('quotes', None)
                if quoteList is not None:
                    self.articleList[-1].get('quotes').append(value)
                else:
                    quoteList = []
                    quoteList.append(value)
                    self.articleList[-1]['quotes'] = quoteList
        f.close()
    def getArticleList(self):
        return self.articleList
    
    def sortArticleByDate(self):
        self.articleList.sort(key=lambda a : a.get('date'))
                            
        
        
# if __name__ == '__main__':
#     ar = ArticleReader() 
#     ar.readFile('sample_of_sample2.txt')     
#     ar.sortArticleByDate()
#     for a in ar.getArticleList():
#         print "--------"
#         for k,v in a.items():
#             if k != 'quotes' and k != 'date':
#                 print k + " : " + v    
#             if k == 'date':
#                 print k + " : " + v.strftime(NEWS_TIMEFORMAT)
#             if k == 'quotes':
#                 for q in v:
#                     print k + " : " + q                 
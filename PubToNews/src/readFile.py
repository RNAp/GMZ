import datetime as dt

NEWS_TIMEFORMAT = "%Y-%m-%d %H:%M:%S"

class ArticleReader(object):
    def __init__(self):
        self.articleDict = {}
                
    def readArticle(self,line):
        articleAsRead = eval(line)
        self.articleDict['url'] = articleAsRead['U']
        self.articleDict['date'] = dt.datetime.strptime(articleAsRead['D'], NEWS_TIMEFORMAT)
        self.articleDict['title'] = articleAsRead['T']
        self.articleDict['content'] = articleAsRead['C']
#         self.articleDict['links'] = articleAsRead['L']
#         self.articleDict['quotes'] = articleAsRead['Q']
        
        
if __name__ == '__main__':
    ar = ArticleReader()
    f = open('part-r-00000')    
    ar.readArticle(f.readline())
    for k,v in ar.articleDict.items():
        print "key: " + k + " value: " + v
                                
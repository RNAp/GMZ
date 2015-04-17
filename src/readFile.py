'''
ArticleReader API:

readFile - Given a spinn3r file, read in a list of article dictionary. Each article dictionary has at most five keys: url, date, title, content, and quotes, where the value of date is a datetime object and the value of quotes is a list.
getArticleList - Get the list of articles
sortArticleByDate - Sort the articles by date
'''
# from writeFile import ArticleWriter
import datetime as dt 

NEWS_TIMEFORMAT = "%Y-%m-%d %H:%M:%S"
EN_THRESHOLD = 0.95

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
                if len(self.articleList) > 0:
                    self._langFiltering()
                if len(self.articleList) > 0:
                    self._urlFiltering()
                if len(self.articleList) > 0:
                    self._deduplication()
                newArticle = {}
                newArticle['id'] = value
                self.articleList.append(newArticle)
            if key == 'S':
                self.articleList[-1]['language'] = fields[1:]
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

    def _langFiltering(self):
        lang = self.articleList[-1].get('language',None)
        if lang is not None:
            # pop the article if its language is not English or below the threshold
            if lang[0] != 'en' or float(lang[1]) < EN_THRESHOLD:
                self.articleList.pop()
            # remove the language key-value pair
            else:
                self.articleList[-1].pop('language')

    def _deduplication(self):
        lastUrl = self.articleList[-1].get('url',None)
        lastTitle = self.articleList[-1].get('title',None)
        lastContent = self.articleList[-1].get('content',None)
        for a in self.articleList[:-1]:
            url = a.get('url',None)
            if url is not None and lastUrl is not None:
                if lastUrl == url:
                    self.articleList.pop()
                    break
            title = a.get('title',None)
            if title is not None and lastTitle is not None:
                if lastTitle == title:
                    self.articleList.pop()
                    break
            content = a.get('content',None)
            if content is not None and lastContent is not None:
                if lastContent == content:
                    self.articleList.pop()
                    break

    def _urlFiltering(self):
        urlBlacklist = ['facebook.com','twitter.com']

        lastUrl = self.articleList[-1].get('url',None)
        if lastUrl is not None:
            for u in urlBlacklist:
                if u in lastUrl:
                    self.articleList.pop()
                    break

    def getArticleList(self):
        return self.articleList
    
    def sortArticleByDate(self):
        self.articleList.sort(key=lambda a : a.get('date'))
                            
        
        
# if __name__ == '__main__':
#     ar = ArticleReader()
#     ar.readFile('part-r-00009')
#     aw = ArticleWriter(ar.getArticleList())
#     aw.writeFile('test_en_part_9.txt')

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
'''
ArticleWriter API:

writeFile - write all information of articles: id, url, date, title, content, and quotes, sorted by date
writeIDDate - only write id and date, sorted by date
'''

import datetime as dt 

NEWS_TIMEFORMAT = "%Y-%m-%d %H:%M:%S"

class ArticleWriter(object):

    def __init__(self, articleList):
        self.articleList = articleList
        self._sortArticleByDate()
        
    def writeFile(self, filename):
        f = open(filename,'w')
        for a in self.articleList:
            for key in a.keys():
                if key == 'id':
                    f.write('I\t%s\n' % a[key].strip())
                    break
            for key in a.keys():
                if key == 'url':
                    f.write('U\t%s\n' % a[key].strip())
                    break
            for key in a.keys():
                if key == 'date':
                    f.write('D\t%s\n' % a[key].strftime(NEWS_TIMEFORMAT))
                    break
            for key in a.keys():
                if key == 'title':
                    f.write('T\t%s\n' % a[key].strip())
                    break
            for key in a.keys():
                if key == 'content':
                    f.write('C\t%s\n' % a[key].strip())
                    break
            for key in a.keys():
                if key == 'quotes':
                    for q in a[key]:
                        f.write('Q\t%s\n' % q.strip())
                    break
            f.write('\n')
        f.close()
    
    def writeIDDate(self, filename):
        f = open(filename,'w')
        for a in self.articleList:
            for key in a.keys():
                    if key == 'id':
                        f.write('%s\t' % a[key].strip())
                        break
            for key in a.keys():
                if key == 'date':
                    f.write('%s\n' % a[key].strftime(NEWS_TIMEFORMAT))
                    break
        f.close()
        
    def _sortArticleByDate(self):
        self.articleList.sort(key=lambda a : a.get('date'))

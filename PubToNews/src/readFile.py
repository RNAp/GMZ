
class ArticleReader(object):
    '''
       Given a spinn3r file, read in a list of article dictionary. 
       Each article dictionary has five keys: url, date, title, content, and quotes, where the value of quotes is a list.
       
    '''
    def __init__(self):
        self.articleList = []
        
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
                self.articleList[-1]['date'] = value
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
    def getArticleList(self):
        return self.articleList
        
        
if __name__ == '__main__':
    ar = ArticleReader() 
    ar.readFile('sample_of_sample.txt')     
    for a in ar.getArticleList():
        print "--------"
        for k,v in a.items():
            if k != 'quotes':
                print k + " : " + v    
            else:
                for q in v:
                    print k + " : " + q                 
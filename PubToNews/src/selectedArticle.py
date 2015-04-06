from readFile import ArticleReader

'''
To be implemented
def dateRange(self, timestamp, interval):
'''


class SelectedArticle(object):
    '''
    Given a seires of selection criterias, save interested_articles into SelectedArticles
    '''

    def __init__(self):
        self.articleList=[]
        self.count=0

        '''
        housekeeping sets to record the selection criterias
        '''
        self.urlSource=[]
        self.dateRange=[]
        self.keyWordsSet=[]


    def addUrlSource(self, urlSet):
        for url in urlSet:
            self.urlSource.append(url)

    def keyWordsSource(self, keyWords):
       for key in keyWords:
           self.keyWordsSet.append(key)

   
    def addArticle(self, selected_article):
        self.articleList.append(selected_article)
        self.count=self.count+1

    def getArticleList(self):
        return self.articleList

    def cout(self):
        return self.count

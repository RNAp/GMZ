from readFile import ArticleReader

'''
To be implemented
def dateRange(self, timestamp, interval):


########################
current APT for selectedArticle class

def addDateRange(self, timestamp, interval):

def dateRange(self):
                
def addUrlSource(self, urlSet):

def urlSource(self):
    
def addKeyWordsSource(self, keyWords):

def keyWordsSource(self):

def addArticle(self, selected_article):

def getArticleList(self):
        
def count(self):

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

        # the date range is stored as a set of dictionaries: {timestamp : interval}
    
        self.dateRange=[]
        
        self.keyWordsSet=[]

    def addDateRange(self, timestamp, interval):
        newDict = {timestamp : interval}
        dateRange.append(newDict)

    def dateRange(self):
        return dateRange
        
    def addUrlSource(self, urlSet):
        for url in urlSet:
            self.urlSource.append(url)

    def urlSource(self):
        return urlSource
    
    def addKeyWordsSource(self, keyWords):
       for key in keyWords:
           self.keyWordsSet.append(key)

    def keyWordsSource(self):
        return keyWordsSet
   
    def addArticle(self, selected_article):
        self.articleList.append(selected_article)
        self.count=self.count+1

    def getArticleList(self):
        return self.articleList

    def count(self):
        return self.count

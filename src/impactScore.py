'''
The purpose of this code is to calculate a normalized impact score for a publication based on weighted-average of visiting traffic of its reporting media souces. 

def impactScore(ArticleReader, urlTraFile="url_traffic.txt")

'''

from readFile import ArticleReader

from urlparse import urlparse



def findDomain(url): # a method that takes in a url string and return the domain of it
    parsed=urlparse(url.strip())
    return '{uri.scheme}://{uri.netloc}'.format(uri=parsed)
    
def _weighted_average(domainDict):
    

def _readUrlTra(urlTraFile):
    f=open(urlTraFile)
    
def impactScore(ArticleReader ar, urlTraFile="url_traffic.txt", NORMALIZATION_CONST=10000):
    domainDict={}
    
    for article in ar.getArticleList():
        cur_url=article['url']
        domain=findDomain(cur_url)
        domainList[domain]=0
    
    
    
    



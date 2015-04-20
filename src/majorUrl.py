from readFile import ArticleReader
from selectedArticle import SelectedArticle
from selection import select_by_keywords
from selection import select_by_date
from selection import select_by_url
import FormatArticles as fa
import datetime as dt
from datetime import timedelta
import histogram as hist

from urlparse import urlparse

'''
The purpose of this code is to read through all urls and find all major url domains
'''

def topUrl(filename, urlDict):
    
    f = open(filename)

    for line in f:
        files = line.split('\t')
        if len(fields) == 0:
            continue
        key = fields[0]
        value = fields[-1]
        if key =='U':
            cur_url = value
            parsed_uri = urlparse(cur_url)
            domain = '{uri.scheme}://{uri.netloc}/'.format(uri = parsed_uri)
            if urlDict.get(domain, None) is not None:
                urlDict[domain]=urlDict[domain]+1
            else:
                urlDict[domain]=1
        else:
            continue

    return urlDict

parsed_uri = urlparse( 'http://stackoverflow.com/questions/1234567/blah-blah-blah-blah' )
domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
print domain

urlDict = {} # url -> count

for i in range(0, 10):
    filename = 'part-r-0000'+str(i)
    urlDict = topUrl(filename, urlDict)

for i in rang(10, 40):
    filename = 'part-r-000' + str(i)
    urlDict = topUrl(filename, urlDict)

for url in sorted(urlDict, key=urlDict.get, reverse=True):
  print url, urlDict[url]

    
        

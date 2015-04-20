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

'''
the following method topUrl parses domain for a particular url and saves it into a dictionary of domain -> counts
'''
def topUrl(filename, urlDict):
    f = open(filename)

    for line in f:
        fields = line.split('\t')
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
    f.close()
    return urlDict

urlDict = {} # url -> count

for i in range(0, 10):
    filename = 'secdata/part-r-0000'+str(i)
    print 'processing ', filename
    urlDict = topUrl(filename, urlDict)

for i in range(10, 40):
    filename = 'secdata/part-r-000' + str(i)
    print 'processing ', filename
    urlDict = topUrl(filename, urlDict)

print 'Total domain count is ', len(urlDict)
f = open('topURL.txt', 'w')
for domain in sorted(urlDict, key=urlDict.get, reverse=True):
    if urlDict[domain] > 1:
        f.write('%s\t'% domain)
        f.write('%s\n'% str(urlDict[domain]))

f.close()
    
        

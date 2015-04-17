'''
this is simply a test script
'''

from readFile import ArticleReader
from selectedArticle import SelectedArticle
from selection import select_by_keywords
from selection import select_by_date
from selection import select_by_url
import FormatArticles as fa
import datetime as dt
from datetime import timedelta
import histogram as hist

NEWS_TIMEFORMAT = "%Y-%m-%d %H:%M:%S"

ar = ArticleReader()

print "reading files"
ar.readFile('part-r-00011')

sr = SelectedArticle()
key = set(['obama', 'gore'])

print "select by date"
date = "2009-01-01 00:00:00"
timestamp = dt.datetime.strptime(date.strip(), NEWS_TIMEFORMAT)
interval = timedelta(days=1000)

sr = select_by_date(ar, sr, timestamp, interval)


print "select by url"
sr = select_by_url(sr, SelectedArticle())

print sr.count

print "################"

for a in sr.getArticleList():
        print "--------"
        cur_t=a.get('title', None)
        if cur_t is not None:
                print cur_t

print "##################"
print "select by keywords"
sr = select_by_keywords(sr, SelectedArticle(), key, 'all')
tol = sr.count
for a in sr.getArticleList():
        print "--------"
        cur_t=a.get('title', None)
        if cur_t is not None:
                print cur_t,
        print a.get('date', None)

print "#################"
print "formatting"

'''
for article in sr.getArticleList():
    cur_t=article.get('title', None)
    cur_c=article.get('content', None)
    if cur_t is not None:
        article['title']=fa.convert_to_match_array(cur_t)
    if cur_c is not None:
        article['content']=fa.convert_to_match_array(cur_c)
'''


date = "2009-01-01 00:00:00"
timestamp = dt.datetime.strptime(date.strip(), NEWS_TIMEFORMAT)
hist.sr_month_hist(sr, timestamp)

print tol

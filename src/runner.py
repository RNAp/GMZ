'''
this is simply a test script
'''
from writeFile import ArticleWriter
from readFile import ArticleReader
from selectedArticle import SelectedArticle
from selection import select_by_keywords
from selection import select_by_date
from selection import select_by_url
from selection import select_by_ID
import FormatArticles as fa
import datetime as dt
from datetime import timedelta
import histogram as hist

NEWS_TIMEFORMAT = "%Y-%m-%d %H:%M:%S"

top = open('top_article_10cutoff.txt')
topID = []

for line in top:
        topID.append(line[:-1])
top.close()


ar = ArticleReader()

print "reading files"
ar.readFile('articles_higgsPhyCern_all_no_dup.txt')

sr = SelectedArticle()

sr = select_by_ID(ar, sr, topID)

print sr.count

print "################"

aw = ArticleWriter(sr.getArticleList())

aw.writeFile('/results/sim02_02_10cutoff_allinfo.txt')



'''
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


for article in sr.getArticleList():
    cur_t=article.get('title', None)
    cur_c=article.get('content', None)
    if cur_t is not None:
        article['title']=fa.convert_to_match_array(cur_t)
    if cur_c is not None:
        article['content']=fa.convert_to_match_array(cur_c)
'''

'''
date = "2009-01-01 00:00:00"
timestamp = dt.datetime.strptime(date.strip(), NEWS_TIMEFORMAT)
hist.sr_month_hist(sr, timestamp)

print tol
'''

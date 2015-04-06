'''
this is simply a test script
'''

from readFile import ArticleReader
from selectedArticle import SelectedArticle
from selection import select_by_keywords
from selection import select_by_date
from selection import select_by_url
import FormatArticles as fa

ar = ArticleReader()
ar.readFile('sample_of_sample.txt')

print 'readfing files'

sr = SelectedArticle()
key = set(['bandwagon', 'obama', 'rock', 'gore'])
url = set(['google.com', 'acs.org'])

print "select by url"
sr = select_by_url(ar, sr)



print "################"

for a in sr.getArticleList():
        print "--------"
        print a['title']


for article in ar.getArticleList():
    cur_t=article.get('title', None)
    cur_c=article.get('content', None)
    if cur_t is not None:
        article['title']=fa.convert_to_match_array(cur_t)
    if cur_c is not None:
        article['content']=fa.convert_to_match_array(cur_c)
    
print "select by keywords"
sr = select_by_keywords(sr, SelectedArticle(), key, 'content')
tol = sr.count
for a in sr.getArticleList():
        print "--------"
        print a['title']


print tol

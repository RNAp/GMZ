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
ar.sortArticleByDate()

print 'readfing files'

sr = SelectedArticle()
key = set(['obama', 'Nobel'])
url = set(['google.com', 'acs.org'])

for article in ar.getArticleList():
    cur_t=article['title']
    cur_c=article['content']
    article['title']=fa.convert_to_match_array(cur_t)
    article['content']=fa.convert_to_match_array(cur_c)
    
sr = select_by_url(ar, sr)
sr = select_by_keywords(ar, sr, key)
tol = sr.count

print tol
for a in sr.getArticleList():
        print "--------"
        print a['content']

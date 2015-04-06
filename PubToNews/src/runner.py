from readFile import ArticleReader
from selectedArticle import SelectedArticle
from selection import select_by_keywords
from selection import select_by_date
from selection import select_by_url

ar = ArticleReader()
ar.readFile('sample_of_sample.txt')

print 'readfing files'

sr = SelectedArticle()
key = set(['obama', 'Nobel'])
url = set(['google.com', 'acs.org'])
sr = select_by_url(ar, sr)
tol = sr.count

print tol
for a in sr.getArticleList():
        print "--------"
        print a['url']

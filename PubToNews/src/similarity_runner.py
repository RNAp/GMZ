
from readFile import ArticleReader
from selectedArticle import SelectedArticle
from selection import select_by_keywords
from selection import select_by_date
from selection import select_by_url
import FormatArticles as fa
import datetime as dt
from datetime import timedelta
import histogram as hist
import similarity as sim

NEWS_TIMEFORMAT = "%Y-%m-%d %H:%M:%S"

ar = ArticleReader()

print "reading files"
ar.readFile('sample_of_sample.txt')
ar = fa.contentCleanUp(ar)

sim.simScore('2008080103_00008227_W', ar)

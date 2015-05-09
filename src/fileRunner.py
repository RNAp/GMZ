'''
this is simply a test script
'''

from writeFile import ArticleWriter
from readFile import ArticleReader
from selectedArticle import SelectedArticle
from selection import select_by_keywords
from selection import select_by_date
from selection import select_by_url
import FormatArticles as fa
import datetime as dt

# key = set([])  # 22874 deep learning without duplicates; CRISPR 5979; higgs part1 81742, part2 81799, part3 78091, part4 81941, 323573 total; higgs+physicists+cern: 38080
# closedate + MIT: 33; closedate + Zhang: 56; closedate + Cas9: 61; just closedate: 210

print "reading file"
ar = ArticleReader()
ar.readFile('CRISPR_all_nono_dup.txt')

# allSelArticles = []
# tolCount = 0   # total articles in first 40 files without duplication: up to 32, memory error; total articles in second 40 files without duplication: 481146

# for i in range(0,40):
#     print ('reading file %d' % i)
#     if i < 10:
#         filename = 'E:\\CS341\\sample\\part-r-0000' + str(i)
#     else:
#         filename = 'E:\\CS341\\sample\\part-r-000' + str(i)
#
#     ar = ArticleReader()
#     ar.readFileMoreFiltering(filename)                        # readFileMoreFiltering or readFile
#     tolCount += len(ar.getArticleList())
#
#
# print ('total articles in first 40 files without duplication: %d' % tolCount)


print "select by date"
sr = SelectedArticle()

date = "2013-12-05 00:00:00"
NEWS_TIMEFORMAT = "%Y-%m-%d %H:%M:%S"
timestamp = dt.datetime.strptime(date.strip(), NEWS_TIMEFORMAT)
date_range = dt.timedelta(days=31)

sr = select_by_date(ar, sr, timestamp, date_range)

# print "select by keywords"
# sr = select_by_keywords(sr, SelectedArticle(), key, 'both')

print 'writing files'
aw = ArticleWriter(sr.getArticleList())
aw.writeFile('CRISPR_all_nono_dup_closeMITdate_noKey.txt')
aw.writeIDDate('CRISPR_id_date_nono_dup_closeMITdate_noKey.txt')
print ('find %d articles' % len(sr.getArticleList()))
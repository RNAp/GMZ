from readFile import ArticleReader
from selectedArticle import SelectedArticle
from selection import select_by_keywords
from selection import select_by_date
from selection import select_by_url
import FormatArticles as fa
import datetime as dt
#from datetime import timedelta


NEWS_TIMEFORMAT = "%Y-%m-%d %H:%M:%S"

def sr_month_hist(SR, timestamp, numInterval=12, filename='month_hist.txt'):
    date_list=[timestamp + dt.timedelta(days=x*30) for x in range(0, numInterval)]
    n = len(date_list)

    result=[]
    SR_month = SelectedArticle()
    for i in range(0, n-1):
        SR_month=select_by_date(SR, SR_month, date_list[0], dt.timedelta(days=30))
        temp_num=SR_month.count
        result.append(temp_num)

    
    f = open(filename,'w')
            
    for j in range(0, n-1):
        print date_list[j]
        print '\t'
        print result[j]
        print '\n'
#        f.write(date_list[j])
#        f.write('\t')
#        f.write(result[j])
                    
    f.close()

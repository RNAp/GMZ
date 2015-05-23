#!/usr/bin/env python

import sys
import urllib2
import datetime as dt

NEWS_TIMEFORMAT = "%Y-%m-%d %H:%M:%S"

def readURL(fname='https://s3-us-west-1.amazonaws.com/gmz-src/urlblack/URL_blacklist.txt'):
    url_list=[]
    f = urllib2.urlopen(fname)
    for line in f.readlines():
        line = line.rstrip()
        url_list.append(line)
    return url_list

def dateLimit(cur_date, start='2014-01-25 00:00:00', end='2014-03-30 11:59:59'):
    sdate=dt.datetime.strptime(start, NEWS_TIMEFORMAT)
    edate=dt.datetime.strptime(end, NEWS_TIMEFORMAT)
    if cur_date>=sdate and cur_date<=edate:
        return True
    else:
        return False
    

def main(separator='\t'):
    flag = False
    counter=0
    cur_ID=''
    cur_url=''
    url_list=readURL()
    # input comes from STDIN (standard input)
    for line in sys.stdin:
        line = line.strip()
        fields = line.split(separator)
    
        if len(fields)==0:
            continue
        key = fields[0].strip()
        value=fields[-1].strip()
        if key=='I':
            counter=counter+1
            flag=True
            cur_ID=value   
        if key=='S': # language filtering
            if fields[1]!='en' or float(fields[2])<0.95:
                flag=False
                continue
        if key=='U': # url filtering
            for url in url_list:
                if url in value:
                    flag=False
                    continue
            if flag==True: # record current url of the article
                cur_url=value        
        #if key=='D': # date filtering
        #    cur_date=dt.datetime.strptime(value, NEWS_TIMEFORMAT)
        #    flag=dateLimit(cur_date)
            
        if key=='D' or key=='T' or key=='C':
            if flag==False:
                continue
            else:
                print '%s\t%s\t%s\t%s' % (cur_url, cur_ID, key,value)
                
if __name__ == "__main__":
    main()

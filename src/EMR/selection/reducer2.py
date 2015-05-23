#!/usr/bin/python 

import sys

def __cleanup():
    return '', '', '', ''

def main():
    cur_url=''
    ID=''
    cur_ID=''
    cur_T=''
    cur_Date=''
    cur_C=''
    for line in sys.stdin:
        # remove leading and trailing whitespace
        line = line.strip()
        # parse the input we got from mapper.py
       
        url, ID, key, value = line.split('\t')
        if cur_url==url and cur_T=='' and cur_C=='' and cur_Date=='': # deals with 
            continue
        if cur_url==url and cur_ID!='' and cur_ID!=ID: # deals with duplicate article with same url
            continue
        
        if cur_url!=url: # if the url is different, it means we are at another article
            cur_url=url
            ID, cur_T, cur_C, cur_Date=__cleanup()
            cur_ID=ID
                
        #key, value=fields.split(':')
        cur_ID=ID
        if key=='T':
            cur_T=value
        if key=='D':
            cur_Date=value
        if key=='C':
            cur_C=value
                
        if cur_T!='' and cur_C!='' and cur_Date!='': 
            print 'I\t%s\nU\t%s\nD\t%s\nT\t%s\nC\t%s\n' % (ID,url,cur_Date, cur_T, cur_C)
            ID, cur_T, cur_C, cur_Date=__cleanup()

if __name__=="__main__":
    main()

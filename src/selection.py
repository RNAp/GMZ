from readFile import ArticleReader
from selectedArticle import SelectedArticle 
import datetime as dt
from datetime import timedelta

'''
        selection defines a series of methods to perform selections on Articles based on specific queries on individual keys: url, date, title, content, and quotes, where the value of quotes is a list.
        select_by_xxx takes in ArticleReader, SelectedArticle, and xxx--'key info', and select articles from ArticleReader and save them into SelectedArticle

'''
'''
#######################
current API for selection module:
select_by_ID(ArticleReader, SelectedArticle, IDlist)

select_by_url(ArticleReader, SelectedArticle, url_Filename='url_list.txt')

select_by_date(ArticleReader, SelectedArticle, time_stamp, date_range = timedelta(days=7))

select_by_keywords(ArticleReader, SelectedArticle, keyWords, verbose='title/content/both/all')
Note: when we want to choose articles contain ALL keywords, use verbose = 'all'

#######################
'''
def _readURLfile(url_Filename='url_list.txt'):
    url_set = set()
    with open(url_Filename, 'r') as f:
        for line in f.readlines():
			url_set.add(line.strip())
    return url_set
'''
House keeping helper function used to preserve house keeping info from previous selectedArticles

'''


def _preserveSR(prev_SR, cur_SR):
    if prev_SR.keyWordsSource() is not None:
        cur_SR.addKeyWordsSource(prev_SR.keyWordsSource())
    if prev_SR.urlSource() is not None:
        cur_SR.addUrlSource(prev_SR.urlSource())
    if prev_SR.dateRange() is not None:
        for dict in prev_SR.dateRange():
            cur_k=dict.keys()
            cur_v=dict.values()
            cur_SR.addDateRange(cur_k[0], cur_v[0])
    return cur_SR


def select_by_ID(ArticleReader, SelectedArticle, IDlist):
    for article in ArticleReader.getArticleList():
        cur_id = article.get('id', None)
        for id in IDlist:
            if id == cur_id:
                SelectedArticle.addArticle(article)            

    return SelectedArticle


'''
        select articles from a mannually maintained url list
'''
def select_by_url(ArticleReader, SelectedArticle, url_Filename='url_list.txt'):
    articles = ArticleReader.articleList
    url_set = _readURLfile(url_Filename)

    _preserveSR(ArticleReader, SelectedArticle) # this is to preserve info from ArticleReader when ArticleReader is actually previous generation of SelectedArticle
    
    SelectedArticle.addUrlSource(url_set)
    for article in ArticleReader.articleList:
        cur_url=article['url']
        for url in url_set:
            if url in cur_url:
                SelectedArticle.addArticle(article)
                break
    return SelectedArticle

'''
        select articles from within a specified date range (default is 7 days) since a particular time_stamp
'''
def select_by_date(ArticleReader, SelectedArticle, time_stamp, date_range = timedelta(days=7)):
    _preserveSR(ArticleReader, SelectedArticle) # this is to preserve info from ArticleReader when ArticleReader is actually previous generation of SelectedArticle
    

    articles = ArticleReader.articleList

    ref_time=time_stamp
    latest_time=ref_time+date_range
    
    for article in ArticleReader.articleList:
        cur_date=article['date']
        '''
                Note: currently the selection is naive and does not consider time-sorted article list
        '''
        if cur_date>=ref_time and cur_date<=latest_time:
            SelectedArticle.addArticle(article)
    return SelectedArticle

'''
        select articles based on wether it contains words in keyWords set or not. The selection can be performed on 'title' or 'content' or both based on verbose value
'''
'''
__find_key_in_array is a helper that searches through array to see wether keyWords are found
'''

def _find_key_in_array(keyWords, targetArr):
    for i in range(len(targetArr)):
        if targetArr[i] in keyWords:
            return True
    return False
    

def _find_key_in_string(keyWords, targetStr):
    for key in keyWords:
        if key in targetStr:
            return True
    return False

def _find_element_in_list(element,list_element):
    try:
        index_element=list_element.index(element)
        return index_element
    except ValueError:
        return -1

def _keyword_location(keyword, content):
    if type(content) is str:
       return content.find(keyword)/len(content)
    elif type(content) is list:
       return _find_element_in_list(keyword,content)/len(content)

def select_by_keywords_location(ArticleReader, SelectedArticle, keyWords, threshold):
    _preserveSR(ArticleReader, SelectedArticle) # this is to preserve info from ArticleReader when ArticleReader is actually previous generation of SelectedArticle
    
    SelectedArticle.addKeyWordsSource(keyWords)
    
    if threshold >1 or threshold < 0:
       print "Invalid threshold: specify threshold between 0 and 1! "
       return SelectedArticle
    
    articles = ArticleReader.articleList
    
    for article in ArticleReader.articleList:
        cur_c=article.get('content', None)
        '''
            the following selections are based on the assumption that: contents are strings or list
            '''
        if cur_c == None:
           continue

        count=0
        for word in keywords:
            cur_loc=_keyword_location(word, cur_c)
            if cur_loc>0 and cur_loc < threshold:
               count=count+1
               if count is len(keywords):
                   SelectedArticle.addArticle(article)

    return SelectedArticle

def select_by_keywords(ArticleReader, SelectedArticle, keyWords, verbose='title'):
    _preserveSR(ArticleReader, SelectedArticle) # this is to preserve info from ArticleReader when ArticleReader is actually previous generation of SelectedArticle
    
    SelectedArticle.addKeyWordsSource(keyWords)
    
    valid_verbose=set(['title', 'content', 'both', 'all'])
    if verbose not in valid_verbose:
        print "Invalid verbose: specify select from 'title', 'content', 'both', or 'all'! "
        return SelectedArticle

    articles = ArticleReader.articleList
    
    for article in ArticleReader.articleList:
        cur_c=article.get('content', None)
        cur_t=article.get('title', None)

        '''
        the following selections are based on the assumption that: titles and contents are arrays
        '''
        if verbose=='title':
            if cur_t == None:
                continue
            if _find_key_in_array(keyWords, cur_t):
                SelectedArticle.addArticle(article)
                continue
        if verbose=='content':
            if cur_c == None:
                continue
            #if __find_key_in_array(keyWords, cur_c):
            if _find_key_in_string(keyWords, cur_c):
                SelectedArticle.addArticle(article)
                continue
        if verbose=='both':
            if cur_t == None or cur_c == None:
                continue
            if _find_key_in_array(keyWords, cur_t) or _find_key_in_string(keyWords, cur_c):
                SelectedArticle.addArticle(article)
                continue
        if verbose == 'all':
            if cur_c == None:
                continue
            mark = 0
            for key in keyWords:
                if key not in cur_c:
                    mark+=1
            if mark == 0:
                SelectedArticle.addArticle(article)
            
    return SelectedArticle

'''
Looks through content and select articles that contains all keywords in given keyWords set
'''
#def contain_all_keywords(ArticleReader, SelectedArticle, keyWords):
            #SelectedArticle.keyWordsSource(keyWords)
    

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

select_by_url(ArticleReader, SelectedArticle, url_Filename='url_list.txt')

select_by_date(ArticleReader, SelectedArticle, time_stamp, date_range = timedelta(days=7))

select_by_keywords(ArticleReader, SelectedArticle, keyWords, verbose='title')

contain_all_keywords(ArticleReader, SelectedArticle, keyWords)  ## to be implemented!!

#######################
'''
def __readURLfile(url_Filename='url_list.txt'):
    url_set = set()
    with open(url_Filename, 'r') as f:
        for line in f.readlines():
			url_set.add(line.strip())
    return url_set

'''
        select articles from a mannually maintained url list
'''
def select_by_url(ArticleReader, SelectedArticle, url_Filename='url_list.txt'):
    articles = ArticleReader.articleList
    url_set = __readURLfile(url_Filename)

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

def __find_key_in_array(keyWords, targetArr):
    for i in range(len(targetArr)):
        if targetArr[i] in keyWords:
            return True
    return False
    

def __find_key_in_string(keyWords, targetStr):
    for key in keyWords:
        if key in targetStr:
            return True
    return False

def select_by_keywords(ArticleReader, SelectedArticle, keyWords, verbose='title'):

    SelectedArticle.keyWordsSource(keyWords)
    
    valid_verbose=set(['title', 'content', 'both'])
    if verbose not in valid_verbose:
        print "Invalid verbose: specify select from 'title', 'content', or 'both'! "
        return SelectedArticle

    articles = ArticleReader.articleList
    
    for article in ArticleReader.articleList:
        cur_c=article['content']
        cur_t=article['title']

        '''
        the following selections are based on the assumption that: titles and contents are arrays
        '''
        if verbose=='title':
            if __find_key_in_array(keyWords, cur_t):
                SelectedArticle.addArticle(article)
                continue
        if verbose=='content':
            #if __find_key_in_array(keyWords, cur_c):
            if __find_key_in_string(keyWords, cur_c):
                SelectedArticle.addArticle(article)
                continue
        if verbose=='both':
            if __find_key_in_array(keyWords, cur_t) or __find_key_in_string(keyWords, cur_c):
                SelectedArticle.addArticle(article)
                continue
    return SelectedArticle
         

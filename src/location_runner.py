# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 12:11:17 2015

@author: Olive
"""

from readFile import ArticleReader
from selectedArticle import SelectedArticle
from selection import _find_element_in_list
from selection import find_keyword_location
from selection import select_by_keywords_location
import FormatArticles as fa
import datetime as dt
from datetime import timedelta
import histogram as hist
import similarity as sim
from writeFile import ArticleWriter

NEWS_TIMEFORMAT = "%Y-%m-%d %H:%M:%S"

ar = ArticleReader()

print "reading files"
ar.readFile('articles_CRISPR_all.txt')
#ar = fa.contentCleanUp(ar)
keyWords=['CRISPR']
threshold=0.1

sr=SelectedArticle()
select_by_keywords_location(ar, sr, keyWords, threshold)



aw=ArticleWriter(sr.getArticleList())

aw.writeFile('output.txt')
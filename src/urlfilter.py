from readFile import ArticleReader
from selectedArticle import SelectedArticle
from selection import block_url
from writeFile import ArticleWriter

arfile='qdots_all_nono_dup.txt'
awout = 'qdots_all_nono_url.txt'
blockurl='URL_blacklist.txt'

ar = ArticleReader()
ar.readFile(arfile)

sr = SelectedArticle()

sr = block_url(ar, sr, blockurl)

aw = ArticleWriter(sr.getArticleList())

aw.writeFile(awout)

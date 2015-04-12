from __future__ import division
from readFile import ArticleReader
from selectedArticle import SelectedArticle
import selection


'''
############################################
The API is described below:


'''

'''
The following method takes in a seed news and a news article and tries to calculate Jaccard similarity for content info S & T/ (S or T)
The news articles are in dict format
'''

def _calSimScore(seed, ar):
    seed_c = set(seed['content'])
    ar_c = set(ar['content'])

    combSet = seed_c.union(ar_c)
    overlapSet = combSet- ((combSet-seed_c).union(combSet-ar_c))

    num_comb = len(combSet)
    num_overlap = len(overlapSet)

    score = num_overlap/num_comb
    
    return score

def _findSeed(seedID, AR):
    seed = {}
    for article in AR.getArticleList():
        if seedID in article['id']:
            seed = article
            break
    return seed

'''
The following method takes in seedID and a list of articles--ArticleReader, and finds seed news, and calculate similarity scores for each article
'''
def simScore(seedID, ArticleReader, filename='similarity.txt'):
    scoreDict = {} # 'id' -> Score
    seed = _findSeed(seedID, ArticleReader)
    cur_score = 0.0
    
    for article in ArticleReader.getArticleList():
        if seedID not in article['id'] and scoreDict.get(article['id'], None) is None:
            cur_score = _calSimScore(seed, article)
            scoreDict[article['id']] = cur_score


    f = open(filename, 'w')
    for id in scoreDict.keys():
        f.write('%s\t' % id.strip())
        f.write('%s\n' % scoreDict[id])
    f.close()
            
    return scoreDict

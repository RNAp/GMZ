import itertools
from math import sqrt

from lsh import MinHashSignature, jaccard_sim

from utils import *

NEWS_TIMEFORMAT = "%Y-%m-%d %H:%M:%S"
NUM_OF_HASH_FUNCS = 100

def getSeedSet(seedID, AR):
    for article in AR.getArticleList():
        if seedID in article.get('id', None):
            return set(article['content'])
    return set()

def calSignatureSimilarity(seedSet, aSet):
    """The probability that two sets' signatures match at some index
    are equal is equal to the Jaccard similarity between the two"""
    dim = NUM_OF_HASH_FUNCS
    mh = MinHashSignature(dim)

    sets = (seedSet, aSet)
    sigs = map(mh.sign, sets)

    ssim = sigsim(*sigs, dim=dim)

    return ssim

def writeSimScores(seedID, ArticleReader, filenameToWrite):
    seedSet = getSeedSet(seedID, ArticleReader)
    if len(seedSet) == 0:
        print 'empty seed set!'
        return
    
    f = open(filenameToWrite + 'ByShingling.txt', 'w')
    
    for article in ArticleReader.getArticleList():
        if seedID not in article.get('id', None):
            f.write('%s\t' % article['id'].strip())
            f.write('%s\t' % article['date'].strftime(NEWS_TIMEFORMAT))
            f.write('%s\n' % calSignatureSimilarity(seedSet, set(article['content'])))

    f.close()

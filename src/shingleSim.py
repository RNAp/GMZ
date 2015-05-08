
from lsh import *
from FormatArticles import *
from utils import *

NEWS_TIMEFORMAT = "%Y-%m-%d %H:%M:%S"
NUM_OF_HASH_FUNCS = 100
SHINGLE_LEN = 10 # character-wise shingle
K_WORD = 3 # word-wise shingle

def _cleanContent(cur_c):
    # stopword_set = load_stopword_set()
    # cur_c = standardize_formatting(cur_c)
    cur_c = convert_to_match_array(cur_c)
    # cur_c = set(cur_c)-stopword_set
    return cur_c

def getSeedSet(seedID, AR):
    for article in AR.getArticleList():
        if seedID in article.get('id', None):
            cur_c = article.get('content', None)
            if cur_c is None:
                print 'empty seed set!'
                return set()
            cur_c = _cleanContent(cur_c)
            return set(hmultiWshingle(cur_c, K_WORD, load_stopword_set()))
    print 'empty seed set!'
    return set()

def calSignatureSimilarity(seedSet, aSet):
    """The probability that two sets' signatures match at some index
    are equal is equal to the Jaccard similarity between the two"""
    dim = NUM_OF_HASH_FUNCS
    mh = MinHashSignature(dim)

    if not aSet:
        return 0

    sets = (seedSet, aSet)
    sigs = map(mh.sign, sets)

    ssim = sigsim(*sigs, dim=dim)

    return ssim

def writeSimScores(seedID, seedSet, ArticleReader, filenameToWrite):
    
    f = open(filenameToWrite, 'w')

    for article in ArticleReader.getArticleList():
        cur_c = article.get('content', None)
        if cur_c is None:
            continue
        cur_c = _cleanContent(cur_c)
        # if seedID not in article.get('id', None):
        f.write('%s\t' % article['id'].strip())
        f.write('%s\t' % article['date'].strftime(NEWS_TIMEFORMAT))
        f.write('%s\t' % article['url'].strip())
        f.write('%f\n' % calSignatureSimilarity(seedSet, set(hmultiWshingle(cur_c, K_WORD, load_stopword_set()))))

    f.close()

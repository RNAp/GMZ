
from lsh import *
from FormatArticles import *
from utils import *

NEWS_TIMEFORMAT = "%Y-%m-%d %H:%M:%S"
NUM_OF_HASH_FUNCS = 100
SHINGLE_LEN = 3 # 3 means 3-word
K_SHINGLE = 10 # 10 means 10-char shingle

# the following method is used to generate words array for multi-word shingling
def _cleanContent(cur_c):
    # stopword_set = load_stopword_set()
    # cur_c = standardize_formatting(cur_c)
    cur_c = convert_to_match_array(cur_c)
    # cur_c = set(cur_c)-stopword_set
    return cur_c

# the following method is used to clean up content string for k-char shingling
#def _cleanContent(cur_c):
    # stopword_set = load_stopword_set()
    # cur_c = standardize_formatting(cur_c)
 #   cur_c = convert_to_match_array(cur_c)
    # cur_c = set(cur_c)-stopword_set
  #  return cur_c


# a helper to calculate multi-word shingling
def _HMultiWshingle(curContent):
    return set(hmultiWshingle(curContent, SHINGLE_LEN))

# a helper to calculate multi-char shingling
def _HKshingle(curContent):
    return set(hkshingle(curContent, K_SHINGLE))

# the following method calculates multi-word based shingling                              
def getSeedSet(seedID, AR):
    for article in AR.getArticleList():
        if seedID in article.get('id', None):
            cur_c = article.get('content', None)
            if cur_c is None:
                print 'empty seed set!'
                return set()
            cur_c = _cleanContent(cur_c)
            #return set(hmultiWshingle(cur_c, SHINGLE_LEN))
            return _HMultiWshingle(cur_c)
    print 'empty seed set!'
    return set()


# the following method calculates k-char shingling
def seedKShingle(seedID, AR):
    for article in AR.getArticleList():
        if seedID in article.get('id', None):
            cur_c = article.get('content', None)
            if cur_c is None:
                print 'empty seed set!'
                return set()
   #         cur_c = _cleanContent(cur_c)
            #return set(hmultiWshingle(cur_c, SHINGLE_LEN))
            return _HKshingle(cur_c)
    print 'empty seed set!'
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

# the following method generates multi-word shingling score
def writeSimScores(seedID, seedSet, ArticleReader, filenameToWrite):
    
    f = open(filenameToWrite + 'ByShingling.txt', 'w')

    for article in ArticleReader.getArticleList():
        cur_c = article.get('content', None)
        if cur_c is None:
            continue
        cur_c = _cleanContent(cur_c)
        if seedID not in article.get('id', None):
            f.write('%s\t' % article['id'].strip())
            f.write('%s\t' % article['date'].strftime(NEWS_TIMEFORMAT))
            f.write('%s\n' % calSignatureSimilarity(seedSet,  _HMultiWshingle(cur_c)))

    f.close()

# the following method generates k-char shingling score
def kcharSimScore(seedID, seedSet, ArticleReader, filenameToWrite):
    
    f = open(filenameToWrite + 'ByShingling.txt', 'w')

    for article in ArticleReader.getArticleList():
        cur_c = article.get('content', None)
        if cur_c is None:
            continue
        cur_c = _cleanContent(cur_c)
        if seedID not in article.get('id', None):
            score = calSignatureSimilarity(seedSet, _HKshingle(cur_c))
            f.write('%s\t' % article['id'].strip())
            f.write('%s\t' % article['date'].strftime(NEWS_TIMEFORMAT))
            f.write('%s\n' % score)
            print article['id'],'\t', score
    f.close()

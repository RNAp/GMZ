#!/usr/bin/python

import sys
import re
import os
import datetime as dt
import urllib2
import string
import operator
import random
import math
from operator import itemgetter
'''
###sys.path.append('./')
from lsh import *
from shingleSim import *
from FormatArticles import *
'''


from collections import defaultdict

NEWS_TIMEFORMAT = "%Y-%m-%d %H:%M:%S"
NUM_OF_HASH_FUNCS = 100
SHINGLE_LEN = 10 # character-wise shingle
K_WORD = 3 # word-wise shingle

TRANSCRIPT_TIMEFORMAT = "%Y-%m-%d %H:%M"
NEWS_TIMEFORMAT = "%Y-%m-%d %H:%M:%S"
HYPHEN_TYPES = ["\xe2\x80\x94", " - ", "\xe2\x80\x93",'\xe2\x80\x92'," -- ","-"] 
NUM_MAP = {'0':'zero', '1': 'one', '2':'two','3':'three','4':'four',
			'5':'five','6':'six','7':'seven','8':'eight','9': 'nine'} 
PUNCTUATION = '"&\'()+,-./:;<=>@[\\]^_`{|}~'




def randset():
    """Return a random set.  These values of n and k have wide-ranging
    similarities between pairs.
    """
    n = random.choice(range(5, 20))
    k = 10
    return tuple(set( random.choice(range(k)) for _ in range(n) ))


def sigsim(X, Y, dim):
    """Return the similarity of the two signatures"""
    return sum(map(operator.eq, X, Y)) / float(dim)

def _no_punct(phrase):
    '''
    Delete all punctuations (as in PUNCTUATION)' '
    '''
    return ' '.join(phrase.translate(string.maketrans("",""),PUNCTUATION).split())


def _convert_word(word):
      '''
         Strips capitalization and punctuation from word;
         also converts numerals to words if < 10.
         call _no_punct()
      '''
      converted = word
      num_equiv = NUM_MAP.get(word, None)
      if num_equiv is not None:
		converted = num_equiv
      return _no_punct(converted).lower()


def _handle_hyphens(phrase):
     '''
         Standardizes how hyphens look 
         (everything of the form word1 - word2 gets turned into word1- word2)
     '''
     dehyphenated = phrase
     for hyphen_type in HYPHEN_TYPES:
		dehyphenated = dehyphenated.replace(hyphen_type, "- ")
     return dehyphenated


def standardize_formatting(phrase):
	'''
            Expresses $, % in a standard way 		
            Converts texts to standard format.
		call _handle_hyphens
	'''
	formatted_phrase = _handle_hyphens(phrase)
	formatted_phrase = formatted_phrase.replace('\xe2\x80\xa6', '... ').replace('\xc2\xa0', '')
	formatted_phrase = formatted_phrase.replace(' per cent ', ' percent ')
	formatted_phrase = formatted_phrase.replace(' usd ', ' $')
	formatted_phrase = formatted_phrase.replace('%',' percent')
	formatted_phrase = re.sub(r'\d+ dollars', lambda x: '$'+x.group(0).split()[0], formatted_phrase)
	return formatted_phrase

def convert_to_match_array(phrase, display_array=None, formatfn = lambda x: x):
	'''
		Converts text to array of words for string alignment; strips
		capitalization and punctuation.

		Arguments:
			display_array (list of str, optional): pre-existing display_array to convert
			formatfn (function, optional): performs further formatting on text before conversion.
	'''
	if display_array is None:
		display_array = convert_to_display_array(phrase, formatfn)
	return [_convert_word(word) for word in display_array]
    
def convert_to_display_array(phrase, formatfn = lambda x: x):
	'''
		Converts text to array of words after format standardization.
		Retains capitalization and punctuation.

		Arguments:
			formatfn (function, optional): custom function to further format phrase 
				before conversion.
	'''
	to_use = formatfn(phrase)
	return standardize_formatting(to_use).split()

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

class Signature(object):
    """Signature Base class."""

    def __init__(self, dim):
        self.dim = dim
        self.hashes = self.hash_functions()

    def hash_functions(self):
        """Returns dim different hash functions"""
        pass

    def sign(self, object):
        """Return the signature for object s"""
        pass


class MinHashSignature(Signature):
    """Creates signatures for sets/tuples using minhash."""

    def hash_functions(self):
        """Return dim different hash functions"""
        def hash_factory(n):
            return lambda x: hash("salt" + str(n) + str(x) + "salt")  # unicode(n), unicode(x)
        return [ hash_factory(_) for _ in range(self.dim) ]

    def sign(self, s):
        """Returns minhash signature for set s"""
        sig = [ float("inf") ] * self.dim
        for hash_ix, hash_fn in enumerate(self.hashes):
            sig[hash_ix] = min(hash_fn(value) for value in s)
        return sig


def kshingle(s, k):
    """Generate k-length shingles of string s"""
    k = min(len(s), k)
    for i in range(len(s) - k + 1):
        yield s[i:i+k]


def hkshingle(s, k):
    """Generate k-length shingles then hash"""
    for s in kshingle(s, k):
        yield hash(s)

def multiWshingle(a, k, stopword_set):
    """Generate k-word shingles of array a"""
    k = min(len(a), k)
    for i in range(len(a) - k + 1):
        if a[i] in stopword_set:
            yield ' '.join(a[i:i+k])


def hmultiWshingle(a, k, stopword_set):
    """Generate k-word shingles then hash"""
    for s in multiWshingle(a, k, stopword_set):
        yield hash(s)

def jaccard_sim(X, Y):
    """Jaccard similarity between two sets"""
    x = set(X)
    y = set(Y)
    return float(len(x & y)) / len(x | y)


def jaccard_dist(X, Y):
    """Jaccard distance between two sets"""
    return 1 - jaccard_sim(X, Y)



K_WORD=3
NEWS_TIMEFORMAT = "%Y-%m-%d %H:%M:%S"


def _cleanContent(cur_c):
    # stopword_set = load_stopword_set()
    # cur_c = standardize_formatting(cur_c)
    cur_c = convert_to_match_array(cur_c)
    # cur_c = set(cur_c)-stopword_set
    return cur_c

def readKeys():
    #return ['global temperature, Forster, Marotzke, Max Planck Institute for Meteorology']
    return ['online games']


def readSeed(fname="https://s3-us-west-1.amazonaws.com/gmz-src/N%26Sseeds/NS1seed.txt"):
    # date='2015-01-01 14:00:00'
    # content='Cherry picking the most recent 15-year interval to refute climate change modeling is misleading and obscures the long-term agreement between the models and measurements, according to study co-author Piers Forster, an atmospheric physicist from the University of Leeds, England. '
    f=urllib2.urlopen(fname)
    for line in f.readlines():
         ID, url, date, title, content=line.strip().split('\t')
    return date.strip(), content.strip().lower()
    
def testKeys(content, keyWords):
    for key in keyWords:
        if key.strip().lower() not in content.strip().lower():
            return False
    return True

def emr_stopword_set(fname='https://s3-us-west-1.amazonaws.com/gmz-src/mysql_stop.txt'):
    stopword_set = set()
    f=urllib2.urlopen(fname)
    for line in f.readlines():
        stopword_set.add(line.strip())
    return stopword_set

    
def getseedSet(content):
    cur_c=_cleanContent(content)
    return set(hmultiWshingle(cur_c, K_WORD, emr_stopword_set()))

def dateLimit(cur_date, seedDate, duration=dt.timedelta(days=7)):
    cur_date=dt.datetime.strptime(cur_date, NEWS_TIMEFORMAT)
    sdate=dt.datetime.strptime(seedDate, NEWS_TIMEFORMAT)
    if cur_date>=sdate and cur_date<=sdate+duration:
        return True
    else:
        return False


class TfIdf:

  def __init__(self, corpus_filename ='https://s3-us-west-1.amazonaws.com/gmz-src/40NoDupNoPunc_idf.txt', stopword_filename = 'https://s3-us-west-1.amazonaws.com/gmz-src/mysql_stop.txt',
               DEFAULT_IDF = 1.5):
    """Initialize the idf dictionary.  
    
       If a corpus file is supplied, reads the idf dictionary from it, in the
       format of:
         # of total documents
         term: # of documents containing the term

       If a stopword file is specified, reads the stopword list from it, in
       the format of one stopword per line.

       The DEFAULT_IDF value is returned when a query term is not found in the
       idf corpus.
    """
    self.num_docs = 0
    self.term_num_docs = {}     # term : num_docs_containing_term
    self.stopwords = []
    self.idf_default = DEFAULT_IDF

    if corpus_filename:
      #corpus_file = open(corpus_filename, "r")
      corpus_file=urllib2.urlopen(corpus_filename)
      # Load number of documents.
      line = corpus_file.readline()
      self.num_docs = int(line.strip())

      # Reads "term:frequency" from each subsequent line in the file.
      for line in corpus_file:
        tokens = line.rpartition(":")
        term = tokens[0].strip()
        frequency = int(tokens[2].strip())
        self.term_num_docs[term] = frequency

    if stopword_filename:
        #stopword_file = open(stopword_filename, "r")
        #stopword_file=urllib2.urlopen
        #self.stopwords = [line.strip() for line in stopword_file]
        self.stopwords=emr_stopword_set()
        
  def get_tokens(self, str):
      """Break a string into tokens, preserving URL tags as an entire token.

       This implementation does not preserve case.  
       Clients may wish to override this behavior with their own tokenization.
      """
      # return re.findall(r"<a.*?/a>|<[^\>]*>|[\w'@#]+", str.lower())
      return convert_to_match_array(str)

  def add_input_document(self, input):
    """Add terms in the specified document to the idf dictionary."""
    self.num_docs += 1
    words = set(self.get_tokens(input))
    for word in words:
      if word in self.term_num_docs:
        self.term_num_docs[word] += 1
      else:
        self.term_num_docs[word] = 1

  def save_corpus_to_file(self, idf_filename, stopword_filename,
                          STOPWORD_PERCENTAGE_THRESHOLD = 0.01):
    """Save the idf dictionary and stopword list to the specified file."""
    output_file = open(idf_filename, "w")

    output_file.write(str(self.num_docs) + "\n")
    for term, num_docs in self.term_num_docs.items():
      output_file.write(term + ": " + str(num_docs) + "\n")

    sorted_terms = sorted(self.term_num_docs.items(), key=itemgetter(1),
                          reverse=True)
    stopword_file = open(stopword_filename, "w")
    for term, num_docs in sorted_terms:
      if num_docs < STOPWORD_PERCENTAGE_THRESHOLD * self.num_docs:
        break

      stopword_file.write(term + "\n")

  def get_num_docs(self):
    """Return the total number of documents in the IDF corpus."""
    return self.num_docs

  def get_idf(self, term):
    """Retrieve the IDF for the specified term.

       This is computed by taking the logarithm of (
       (number of documents in corpus) divided by (number of documents
        containing this term) ).
     """
    if term in self.stopwords:
      return 0

    if not term in self.term_num_docs:
      return self.idf_default

    return math.log(float(1 + self.get_num_docs()) /
      (1 + self.term_num_docs[term]))

  def get_doc_keywords(self, curr_doc):
    """Retrieve terms and corresponding tf-idf for the specified document.

       The returned terms are ordered by decreasing tf-idf.
    """
    tfidf = {}
    tokens = self.get_tokens(curr_doc)
    tokens_set = set(tokens)
    for word in tokens_set:
      # The definition of TF specifies the denominator as the count of terms
      # within the document, but for short documents, I've found heuristically
      # that sometimes len(tokens_set) yields more intuitive results.
      mytf = float(tokens.count(word)) / len(tokens)
      myidf = self.get_idf(word)
      tfidf[word] = mytf * myidf

    return sorted(tfidf.items(), key=itemgetter(1), reverse=True)

    
    
def mapper(args):
    flag=False
    simScore=0.0
    seedDate, seedContent=readSeed()
    seedContent=seedContent.strip().lower()
    seedSet=getseedSet(seedContent)

    keyWords=readKeys()
    seedNorm=0.0
    tol=1e-6
    ti=TfIdf()
    wordTfIdf=ti.get_doc_keywords(seedContent)
    for topWords, topTfIdf in wordTfIdf:
        seedNorm+=topTfIdf**2
        
    seedTopWordTfIdf = [(w,tff) for w, tff in wordTfIdf if tff > tol]
    
    
    
    for line in sys.stdin: # in MR oneline framework, the schema is: ID, url, date, title, content
        cline=line.strip('\t\n')
        if len(cline)==0:
            continue
        ID, url, date, title, content=cline.split('\t')
            
        if dateLimit(date, seedDate) and testKeys(content, keyWords): #perform date filtering

            #print "yes\n"
            cur_c = _cleanContent(content)
            # if seedID not in article.get('id', None):
            
            simScore=calSignatureSimilarity(seedSet, set(hmultiWshingle(cur_c, K_WORD, emr_stopword_set())))

            # cal VSM score
            wordTfIdf=ti.get_doc_keywords(content)

            aNorm=0.0
            vsmSim=0.0
            wordTfIdf = [(w,tff) for w, tff in wordTfIdf if tff > tol]
            for w, tff in wordTfIdf:
                aNorm += tff**2
                for sw, stff in seedTopWordTfIdf:
                    if sw.strip() == w.strip():
                        vsmSim += stff * tff
            vsmSim /= (math.sqrt(aNorm) * math.sqrt(seedNorm))

            print "1\t%s\t%s\t%s\t%s" % (url, date, str(round(vsmSim,5)), str(simScore))


def reducer(args):
    for line in sys.stdin:
        key, url,date,vsm, score=line.split('\t')
        print "%s\t%s\t%s\t%s" % (url,date,vsm, score)

if __name__ == "__main__":
  if sys.argv[1] == "mapper":
    mapper(sys.argv[2:])
  elif sys.argv[1] == "reducer":
    reducer(sys.argv[2:])

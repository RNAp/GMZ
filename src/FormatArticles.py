# -*- coding: utf-8 -*-
"""
def contentCleanUp(ArticleReader): takes in ArticleReader class and clean up its content info, including: calling the following 1,2 & 4 functions. 

Standard functions to do string processing.

1. Standardizes hyphens, $, % and expression for dollars, percent 
   (standardize_formatting)
2. Convert text to array of words after format standardization.
		Retains capitalization and punctuation for display purpose
   (convert_to_display_array)
3. Convert text to array of words for string alignment. Strips capitalization and punctuation from word;
         also converts numerals to words if < 10.
   (convert_to_match_array)
4, load stopword file
"""
import string
from readFile import ArticleReader
import re 


TRANSCRIPT_TIMEFORMAT = "%Y-%m-%d %H:%M"
NEWS_TIMEFORMAT = "%Y-%m-%d %H:%M:%S"
HYPHEN_TYPES = ["\xe2\x80\x94", " - ", "\xe2\x80\x93",'\xe2\x80\x92'," -- ","-"] 
NUM_MAP = {'0':'zero', '1': 'one', '2':'two','3':'three','4':'four',
			'5':'five','6':'six','7':'seven','8':'eight','9': 'nine'} 
PUNCTUATION = '"&\'()+,-./:;<=>@[\\]^_`{|}~'


def _no_punct(phrase):
    '''
    Delete all punctuations (as in PUNCTUATION)' '
    '''
    return ' '.join(phrase.translate(string.maketrans("",""),PUNCTUATION).split())

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

def load_stopword_set(stopword_filename = 'mysql_stop.txt'):
	stopword_set = set()
	with open(stopword_filename, 'r') as f:
		for line in f.readlines():
			stopword_set.add(line.strip())
	return stopword_set


def contentCleanUp(ArticleReader):
    stopword_set = load_stopword_set()
    for article in ArticleReader.getArticleList():
        cur_c = article.get('content', None)
        if cur_c is None:
            continue
        cur_c = standardize_formatting(cur_c)
        cur_c = convert_to_display_array(cur_c)
        cur_c = set(cur_c)-stopword_set
        article['content'] = cur_c

    return ArticleReader
        
    
    


__author__ = 'Yangye Zhu'

from writeFile import ArticleWriter
import datetime as dt

NEWS_TIMEFORMAT = "%Y-%m-%d %H:%M:%S"
EN_THRESHOLD = 0.95
READ_LIMIT = 1e5
DATE_BEFORE = 1
DATE_AFTER = 14

class ArticleReaderWriter(object):

    def __init__(self):
        self.articleList = []

    # the following methods were added due to modifications in SelectedArticle class by MC
    def keyWordsSource(self):
        return None

    def urlSource(self):
        return None

    def dateRange(self):
        return None

    def readwriteLangFiltered(self, filename):
        f = open(filename)
        data = self._readLineAndSplit(f)  # <generator object _readLineAndSplit at 0x0225CE90>
        partNumber = 1
        for fields in data:
            if len(fields) == 0:
                continue
            key = fields[0].strip()
            value = fields[-1].strip()
            if key == 'I':
                if len(self.articleList) > 0:
                    self._langFiltering()
                    if len(self.articleList) >= READ_LIMIT:
                        print "writing langFiltered file part ", partNumber
                        aw = ArticleWriter(self.articleList)
                        aw.writeFile(filename[:-4] + "_langFiltered_" + str(partNumber) + ".txt")
                        partNumber += 1
                        self._dumpArticles()
                newArticle = {}
                newArticle['id'] = value
                self.articleList.append(newArticle)
            if key == 'S':
                self.articleList[-1]['language'] = fields[1:]
            if key == 'U':
                self.articleList[-1]['url'] = value
            if key == 'D':
                self.articleList[-1]['date'] = dt.datetime.strptime(value, NEWS_TIMEFORMAT)
            if key == 'T':
                self.articleList[-1]['title'] = value
            if key == 'C':
                self.articleList[-1]['content'] = value
            if key == 'Q':
                quoteList = self.articleList[-1].get('quotes', None)
                if quoteList is not None:
                    self.articleList[-1].get('quotes').append(value)
                else:
                    quoteList = []
                    quoteList.append(value)
                    self.articleList[-1]['quotes'] = quoteList
        print "writing langFiltered file part ", partNumber
        aw = ArticleWriter(self.articleList)
        aw.writeFile(filename[:-4] + "_langFiltered_" + str(partNumber) + ".txt")
        self._dumpArticles()
        f.close()

    def readwriteDateFiltered(self, filename, seedNewsDate):
        timestamp = dt.datetime.strptime(seedNewsDate.strip(), NEWS_TIMEFORMAT)
        date_before = dt.timedelta(days=DATE_BEFORE)
        date_after = dt.timedelta(days=DATE_AFTER)
        f = open(filename)
        data = self._readLineAndSplit(f)  # <generator object _readLineAndSplit at 0x0225CE90>
        partNumber = 1
        for fields in data:
            if len(fields) == 0:
                continue
            key = fields[0].strip()
            value = fields[-1].strip()
            if key == 'I':
                if len(self.articleList) > 0:
                    self._dateFiltering(timestamp, date_before, date_after)
                    if len(self.articleList) >= READ_LIMIT:
                        print "writing dateFiltered file part ", partNumber
                        aw = ArticleWriter(self.articleList)
                        aw.writeFile(filename[:-4] + "_dateFiltered_" + str(partNumber) + ".txt")
                        partNumber += 1
                        self._dumpArticles()
                newArticle = {}
                newArticle['id'] = value
                self.articleList.append(newArticle)
            if key == 'S':
                self.articleList[-1]['language'] = fields[1:]
            if key == 'U':
                self.articleList[-1]['url'] = value
            if key == 'D':
                self.articleList[-1]['date'] = dt.datetime.strptime(value, NEWS_TIMEFORMAT)
            if key == 'T':
                self.articleList[-1]['title'] = value
            if key == 'C':
                self.articleList[-1]['content'] = value
            if key == 'Q':
                quoteList = self.articleList[-1].get('quotes', None)
                if quoteList is not None:
                    self.articleList[-1].get('quotes').append(value)
                else:
                    quoteList = []
                    quoteList.append(value)
                    self.articleList[-1]['quotes'] = quoteList
        print "writing dateFiltered file part ", partNumber
        aw = ArticleWriter(self.articleList)
        aw.writeFile(filename[:-4] + "_dateFiltered_" + str(partNumber) + ".txt")
        self._dumpArticles()
        f.close()

    def readwriteKeyFiltered(self, filename, keyWords):
        f = open(filename)
        data = self._readLineAndSplit(f)  # <generator object _readLineAndSplit at 0x0225CE90>
        partNumber = 1
        for fields in data:
            if len(fields) == 0:
                continue
            key = fields[0].strip()
            value = fields[-1].strip()
            if key == 'I':
                if len(self.articleList) > 0:
                    self._keyFiltering(keyWords)
                    if len(self.articleList) >= READ_LIMIT:
                        print "writing keyFiltered file part ", partNumber
                        aw = ArticleWriter(self.articleList)
                        aw.writeFile(filename[:-4] + "_keyFiltered_" + str(partNumber) + ".txt")
                        partNumber += 1
                        self._dumpArticles()
                newArticle = {}
                newArticle['id'] = value
                self.articleList.append(newArticle)
            if key == 'S':
                self.articleList[-1]['language'] = fields[1:]
            if key == 'U':
                self.articleList[-1]['url'] = value
            if key == 'D':
                self.articleList[-1]['date'] = dt.datetime.strptime(value, NEWS_TIMEFORMAT)
            if key == 'T':
                self.articleList[-1]['title'] = value
            if key == 'C':
                self.articleList[-1]['content'] = value
            if key == 'Q':
                quoteList = self.articleList[-1].get('quotes', None)
                if quoteList is not None:
                    self.articleList[-1].get('quotes').append(value)
                else:
                    quoteList = []
                    quoteList.append(value)
                    self.articleList[-1]['quotes'] = quoteList
        print "writing keyFiltered file part ", partNumber
        aw = ArticleWriter(self.articleList)
        aw.writeFile(filename[:-4] + "_keyFiltered_" + str(partNumber) + ".txt")
        self._dumpArticles()
        f.close()

    def readwriteDedup(self, filename):
        f = open(filename)
        data = self._readLineAndSplit(f)  # <generator object _readLineAndSplit at 0x0225CE90>
        partNumber = 1
        for fields in data:
            if len(fields) == 0:
                continue
            key = fields[0].strip()
            value = fields[-1].strip()
            if key == 'I':
                if len(self.articleList) > 0:
                    self._deduplication()
                    if len(self.articleList) >= READ_LIMIT:
                        print "writing deduplicated file part ", partNumber
                        aw = ArticleWriter(self.articleList)
                        aw.writeFile(filename[:-4] + "_dedup_" + str(partNumber) + ".txt")
                        partNumber += 1
                        self._dumpArticles()
                newArticle = {}
                newArticle['id'] = value
                self.articleList.append(newArticle)
            if key == 'S':
                self.articleList[-1]['language'] = fields[1:]
            if key == 'U':
                self.articleList[-1]['url'] = value
            if key == 'D':
                self.articleList[-1]['date'] = dt.datetime.strptime(value, NEWS_TIMEFORMAT)
            if key == 'T':
                self.articleList[-1]['title'] = value
            if key == 'C':
                self.articleList[-1]['content'] = value
            if key == 'Q':
                quoteList = self.articleList[-1].get('quotes', None)
                if quoteList is not None:
                    self.articleList[-1].get('quotes').append(value)
                else:
                    quoteList = []
                    quoteList.append(value)
                    self.articleList[-1]['quotes'] = quoteList
        print "writing deduplicated file part ", partNumber
        aw = ArticleWriter(self.articleList)
        aw.writeFile(filename[:-4] + "_dedup_" + str(partNumber) + ".txt")
        self._dumpArticles()
        f.close()

    def _langFiltering(self):
        lang = self.articleList[-1].get('language',None)
        if lang is not None:
            # pop the article if its language is not English or below the threshold
            if lang[0] != 'en' or float(lang[1]) < EN_THRESHOLD:
                self.articleList.pop()
            # remove the language key-value pair
            else:
                self.articleList[-1].pop('language')

    def _keyFiltering(self, keyWords):
        cur_c = self.articleList[-1].get('content',None)
        cur_c = cur_c.strip().lower()
        mark = 0
        for key in keyWords:
            if key not in cur_c:
                mark += 1
        if mark > 0:
            self.articleList.pop()

    def _deduplication(self):
        lastUrl = self.articleList[-1].get('url',None)
        lastTitle = self.articleList[-1].get('title',None)
        lastContent = self.articleList[-1].get('content',None)
        for a in self.articleList[:-1]:
            url = a.get('url',None)
            if url is not None and lastUrl is not None:
                # if url is the same, duplicates!
                if lastUrl == url:
                    self.articleList.pop()
                    break
            title = a.get('title',None)
            content = a.get('content',None)
            if title is not None and lastTitle is not None:
                if content is not None and lastContent is not None:
                    # if both title and content are the same, duplicates!
                    if lastTitle == title and lastContent == content:
                        self.articleList.pop()
                        break

    def _dateFiltering(self, timestamp, date_before, date_after):
        start_time=timestamp - date_before
        end_time=timestamp + date_after
        cur_date=self.articleList[-1].get('date',None)
        if cur_date < start_time or cur_date > end_time:
            self.articleList.pop()

    def _readLineAndSplit(self,f):
        for line in f:
            yield line.split('\t')

    def _dumpArticles(self):
        self.articleList[:] = []

    def getArticleList(self):
        return self.articleList

    def sortArticleByDate(self):
        self.articleList.sort(key=lambda a : a.get('date'))

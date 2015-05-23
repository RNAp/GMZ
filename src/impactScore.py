'''
The purpose of this code is to calculate a normalized impact score for a publication based on weighted-average of visiting traffic of its reporting media souces. 


'''
from urlparse import urlparse

def findDomain(url): # a method that takes in a url string and return the domain of it
    parsed=urlparse(url.strip())
    originalDomain = '{uri.scheme}://{uri.netloc}'.format(uri=parsed)
    fields = originalDomain.split('//')
    if len(fields[1].split('.')) == 3:
        ffields = fields[1].split('.', 1)
        domain = ffields[1]
    if len(fields[1].split('.')) == 2:
        domain = fields[1]

    return domain

def _calDomainTraffic(domainDict, domain):
    for d, t in domainDict.items():
        if d.strip() == domain.strip():
            return t
    return 0

def _readUrlRank(urlRankFile):
    domainDict = {}
    with open(urlRankFile) as f:
        data = _readLineAndSplit(f)
        for fields in data:
            domain = fields[1].strip()
            traffic = 1.0/float(fields[0])
            domainDict[domain] = traffic
    f.close()
    return domainDict

def _readLineAndSplit(f):
        for line in f:
            yield line.split('\t')
    
def impactScore(relevantNewsFilename, urlRankFile="url_rank.txt"):
    domainDict = _readUrlRank(urlRankFile)
    score = 0.0
    with open(relevantNewsFilename) as f:
        data = _readLineAndSplit(f)
        for fields in data:
            url = fields[2].strip()
            domain = findDomain(url)
            score += _calDomainTraffic(domainDict, domain)
    return score


if __name__ == "__main__":
    print impactScore("2015Q1_PlantDev3KeyWords_2015010220_00046943_W_relevant.txt") # result: 0.00514308239043
    
    
    



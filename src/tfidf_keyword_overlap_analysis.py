import datetime as dt
import re

NEWS_TIMEFORMAT = "%Y-%m-%d"

# Prepare the file names
AllArticleFile = "qdots_all_top_words_tfidf_location_filter.txt"
SeedFile = "qdotsNrl_no_dup_seed_top_words_tfidf.txt"

OutputFileName = "qdotsNrl_keyword_overlap_location_filter.txt"

count=10

print "reading input file"
SeedKeywords=set()
with open(SeedFile,'r') as f:
    for i in range(count):
        line=f.readline()
        fields=line.split()
        SeedKeywords.add(fields[0])
    f.close()

day0 = dt.datetime.strptime('2008-01-01',NEWS_TIMEFORMAT)

OverlapCount=[]
wordset=set()
with open(AllArticleFile,'r') as f:
    for line in f:
        line=line.replace(':',' ')
        line=line.split()
        if len(line)==0:
            continue
        elif line[0] == "ID":
            if len(wordset) != 0:
                OverlapCount.append((date,len(wordset.intersection(SeedKeywords))))
            id=line[1]
            wordset=set()
        elif line[0]=="Date":
            date=dt.datetime.strptime(line[1], NEWS_TIMEFORMAT)-day0
            date=str(date).split()
            date=date[0]
        else:
            wordset.add(line[0])

    f.close()

with open(OutputFileName, 'w') as f:
    for pairs in OverlapCount:
        print pairs
        f.write('%s\t%f\n' % (pairs[0],pairs[1]))
    f.close()





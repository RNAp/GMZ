__author__ = 'Yangye Zhu'

import datetime as dt

NEWS_TIMEFORMAT = "%Y-%m-%d %H:%M:%S"
fname = 'articles_higgs_all_without_duplicates'
filenamePrefix = fname + '_part'
fOut = open(fname + '.txt','w')

'''read parts and write out'''
for i in range(4):
    filename = filenamePrefix + str(i+1) + '.txt'
    fIn = open(filename)
    for line in fIn:
        fOut.write(line)
    fIn.close()
fOut.close()

'''sort by date'''
'''
fIn = open(fname + '.txt')
allSelArt = []
for line in fIn:
    fields = line.split('\t')
    fields[1] = dt.datetime.strptime(fields[1].strip(), NEWS_TIMEFORMAT)
    allSelArt.append(fields)
allSelArt.sort(key=lambda a : a[1])

fOut = open(fname + '.txt','w')
for a in allSelArt:
    fOut.write('%s\t' % a[0].strip())
    fOut.write('%s\n' % a[1].strftime(NEWS_TIMEFORMAT))

fOut.close()
'''
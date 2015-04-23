from readFile import ArticleReader
import shingleSim as shsim

# seedID = '2009020517_00010681_W' # qdots
# seedID = '2008080103_00008227_W' # sos
seedID = '2012070412_00058390_W' # higgs

print "calculate seed k-char shingle"
seed_ar = ArticleReader()
seed_ar.readFile('articles_higgsPhyCern_all_no_dup.txt')
# seed_ar.readFile('sample_of_sample.txt')
seedSet = shsim.seedKShingle(seedID, seed_ar)

ar = ArticleReader()

print "reading file"
ar.readFile('articles_higgsPhyCern_all_no_dup.txt')
# ar.readFile('sample_of_sample.txt')

print 'total article number is ', len(ar.getArticleList())

print "sort articles by date"
ar.sortArticleByDate()

print "write shingling similarity score"
shsim.kcharSimScore(seedID, seedSet, ar, 'higgskcharSim')
# shsim.writeSimScores(seedID, seedSet, ar,'sos_no_duplicates_multiW')

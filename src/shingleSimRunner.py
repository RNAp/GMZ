from readFile import ArticleReader
import shingleSim as shsim

# seedID = '2009020517_00010681_W' # qdots
# seedID = '2008080103_00008227_W' # sos
seedID = '2012070412_00058390_W' # higgs

print "get seed set"
seed_ar = ArticleReader()
seed_ar.readFile('articles_higgs_all.txt')
# seed_ar.readFile('sample_of_sample.txt')
seedSet = shsim.getSeedSet(seedID, seed_ar)

ar = ArticleReader()

print "reading file"
ar.readFile('articles_higgs_all.txt')
# ar.readFile('sample_of_sample.txt')

print "sort articles by date"
ar.sortArticleByDate()

print "write shingling similarity score"
shsim.writeSimScores(seedID, seedSet, ar, 'higgsMultiWSim')
# shsim.writeSimScores(seedID, seedSet, ar,'sos_no_duplicates_multiW')

from readFile import ArticleReader
from writeFile import ArticleWriter
import shingleSim as shsim
import cPickle

# seedID = '2013032709_00001367_W' # qdots mit study
# seedID = '2009020517_00010681_W' # qdots nrl study
seedID = '2013121303_00036748_W' # CRISPR Zhang study
# seedID = '2008080103_00008227_W' # sos
# seedID = '2012070411_00030420_W' # higgs, earlier than the one by MC

print "get seed set"
seed_ar = ArticleReader()
seed_ar.readFile('CRISPR_all_nono_dup_closeMITdate_noKey.txt')
seedSet = shsim.getSeedSet(seedID, seed_ar)

# Saving the objects:
# with open('higgsPhyCernSeedSet10Char.pickle', 'w') as f:
#     cPickle.dump(seedSet, f)


# Getting back the objects:
# with open('higgsPhyCernSeedSet10Char.pickle') as f:
#     seedSet = cPickle.load(f)

ar = ArticleReader()
print "reading file"
ar.readFile('CRISPR_all_nono_dup_closeMITdate_noKey.txt')

print "write shingling similarity score"
shsim.writeSimScores(seedID, seedSet, ar, 'CRISPRNoKeyNoNoDupMultiStopWNoPuncSim')

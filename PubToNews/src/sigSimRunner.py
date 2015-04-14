from readFile import ArticleReader
import FormatArticles as fa
import shingleSim as ssim

ar = ArticleReader()

print "reading files"
ar.readFile('sample_of_sample.txt')
ar = fa.contentCleanUp(ar)

# print sim.getSeedSet('2008080103_00008227_W',ar)
ssim.writeSimScores('2008080103_00008227_W', ar,'sample_of_sample')
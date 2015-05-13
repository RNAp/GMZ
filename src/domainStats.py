from urlparse import urlparse


filename="33_pub_url.csv"
out_file = "33_pub_domain.txt"

f=open(filename)
url_stats = {}

for line in f:
    cur_url=line.strip()
    parsed=urlparse(cur_url)
    domain='{uri.scheme}://{uri.netloc}'.format(uri=parsed)
    if url_stats.get(domain, None)==None:
        url_stats[domain]=1
    else:
        url_stats[domain]+=1
f.close()

f=open(out_file, 'w')
for domain in sorted(url_stats, key=url_stats.get, reverse=True):
    f.write('%s\t'% domain)
    f.write('%s\n'% str(url_stats[domain]))

f.close()

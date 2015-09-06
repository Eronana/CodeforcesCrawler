import urllib
import urllib2
import re
import os
import sys
import threading
import HTMLParser
def get_html(url):
	t=5
	while t>0:
		try:
			return urllib2.urlopen(url).read()
		except:
			t-=1
	print "open url failed:%s"%url
def allre(reg):
	return re.compile(reg,re.DOTALL)
def down_src(html):
	src=allre(r'src="(.*?)"').findall(html)
	for s in src:
		nsrc='src/'+s.replace(':','_').replace('/','_')
		open(workdir+nsrc,"w").write(get_html(s))
		html=html.replace(s,'../'+nsrc)
	return html

def get_contest(c):
	html=get_html("http://codeforces.com/contest/%d/problems"%c)
	p=allre('class="caption">(.*?)</div>').findall(html)
	if len(p)==0:
		return None
	title=HTMLParser.HTMLParser().unescape(p[0])
	html=allre('(<div style="text-align: center;.*)').findall(html)[0]
	html=down_src(html)
	return (c,title,html)
def save_contest(contest):
	cid=contest[0]
	title=contest[1].replace('/','_')
	html=contest[2]
	html_path=workdir+'html/[%d]%s.html'%(cid,title)
	open(html_path,'w').write(header+html)
class crawl_contest(threading.Thread):
    def __init__(this):
        threading.Thread.__init__(this)
    def run(this):
    	global begin
    	while begin<=end:
	    	lock.acquire()
	    	curid=begin
	    	begin+=1
	    	lock.release()
	    	contest=get_contest(curid)
	    	lock.acquire()
	    	if contest==None:
	    		print "cannot crawl contest %d"%curid
	    	else:
	    		save_contest(contest)
	    		print "crawled:[%d]%s"%(contest[0],contest[1])
	    	lock.release()
arglen=len(sys.argv)
if arglen<4 or arglen>5:
	print "Usage:\n\t%s begin end threads [workdir]"%sys.argv[0]
	exit()
if arglen==5:
	workdir=sys.argv[4]
else:
	workdir="./"
begin=int(sys.argv[1])
end=int(sys.argv[2])
threads=int(sys.argv[3])
for d in ['src','html']:
	d=workdir+d
	if not os.path.exists(d):
		print "makedirs:%s"%d
		os.makedirs(d)
lock = threading.RLock()
header=open("header.html").read()
print "crawl contest %d to %d\n%d threads used,save in %s"%(begin,end,threads,workdir)
for i in range(threads):
	crawl_contest().start()
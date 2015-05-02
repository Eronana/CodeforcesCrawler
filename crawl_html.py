import urllib
import urllib2
import re
import os
import threading

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
		open(nsrc,"w").write(get_html(s))
		html=html.replace(s,'../'+nsrc)
	return html
def get_problem(url):
	html=get_html(url)
	html=allre(r'(<div class="problemindexholder".*?)<script').findall(html)[0]
	html=down_src(html)
	return html
def get_contest(c):
	html=get_html("http://codeforces.com/contest/"+c)
	p=allre(r'class="id".*?href="(.*?)"').findall(html)
	if len(p)==0:
		return None
	contest=[]
	for x in p:
		contest.append((x[x.rfind('/')+1:],get_problem("http://codeforces.com"+x)))
	title=allre(r'class="rtable.*?<a.*?>(.*?)<').findall(html)[0]
	return (c,title,contest)
header=open("header.html").read()
h_list=open("html_list.txt","w")
def save_contest(contest):
	cid=contest[0]
	title=contest[1].replace('/','_')
	problem=contest[2]
	probs=[]
	for x in problem:
		c=x[0]
		probs.append(c)
		html=x[1]
		html_path='html/'+cid+'_'+c+'.html'
		open(html_path,'w').write(header+html)
	h_list.write("%s----%s----%s\n"%(cid,title,','.join(probs)))
lock = threading.RLock()
class crawl_contest(threading.Thread):
    def __init__(this):
        threading.Thread.__init__(this)
    def run(this):
    	global begin
    	while begin<end:
	    	lock.acquire()
	    	curid=begin
	    	begin+=1
	    	lock.release()
	    	contest=get_contest(str(curid))
	    	lock.acquire()
	    	if contest==None:
	    		print "cannot crawl contest %d"%curid
	    	else:
	    		save_contest(contest)
	    		print "crawled:%d problems in contest %s"%(len(contest[2]),contest[1])
	    	lock.release()
begin=510
end=530
threads=50
print "crawl contest %d to %d\n%d threads used"%(begin,end,threads)
for i in range(threads):
	crawl_contest().start()
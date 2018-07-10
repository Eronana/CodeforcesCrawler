import urllib
import urllib2
import json
import re
import os
import sys
import threading
import HTMLParser

pdfs=[]
def get_html(url):
	if url[0]=='/':
		if url[1]!='/':
			url='https://codeforces.com/'+url
		else:
			url="https:"+url
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
		open(workdir+nsrc,"wb").write(get_html(s))
		html=html.replace(s,'../'+nsrc)
	html=html.replace('style="max-width: 100.0%;max-height: 100.0%;"','')  # windows workaround
	return html

def get_contest_amount():
	c=json.loads(get_html('/api/contest.list'))['result']
	ret=0
	for cc in c:
		if cc['phase']=='FINISHED':
			ret=max(ret,cc['id'])
	return ret
def get_contest(c):
	html=get_html("/contest/%d/problems"%c)
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
	title=title.replace('<br>','')
	title=title.replace('<br_>','')
	html=contest[2]
	html_path=workdir+'html/[%02d]%s.html'%(cid,title)
	pdfs.append(html_path)
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
	    		print "crawled:[%02d]%s"%(contest[0],contest[1])
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
if begin==-1:
	if not os.path.exists("./html/update"):
		f=open("./html/update","w")
		f.write("0")
		f.close()
	begin=int(open("./html/update","r").read())+1
	print "crawl missing contests from %d:"%(begin)
if end==-1:
	print "trying to get amount of contests ... ",
	end=get_contest_amount()
	print "%d"%end
threads=int(sys.argv[3])
for d in ['src','html']:
	d=workdir+d
	if not os.path.exists(d):
		print "makedirs:%s"%d
		os.makedirs(d)
lock = threading.RLock()
header=open("header.html").read()
print "crawl contest %d to %d\n%d threads used,save in %s"%(begin,end,threads,workdir)
t=[]
for i in range(threads):
	t.append(crawl_contest())
	t[len(t)-1].start()
for i in t:
	i.join()

f=open("./html/update","w")
f.write(str(end))
f.close()
print "converting into pdf..."
for i in pdfs:
	pdf_path="./pdf"+i.replace(".html",".pdf").replace("./html","")
	os.system('wkhtmltopdf -q "%s" "%s"'%(i,pdf_path))
	print "coverted:[%s]"%pdf_path

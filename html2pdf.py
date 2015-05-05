import urllib2
import re
import os
import sys
import threading

def html2pdf(contest):
	cat="pdftk"
	cid=contest[0]
	title=contest[1]
	for x in contest[2]:
		html_path=workdir+'html/'+cid+'_'+x+'.html'
		problem=workdir+'problem/'+cid+'_'+x+'.pdf'
		cmd='wkhtmltopdf -q'\
			' --footer-html footer.html'\
			' "%s" "%s"'%(html_path,problem)

		os.popen(cmd)
		cat+=' '+problem
		lock.acquire()
		print "Generate:%s_%s.pdf"%(cid,x)
		lock.release()
	contest_path='"'+workdir+'contest/'+title+'.pdf"'
	cat+=' cat output '+contest_path
	os.popen(cat)
	print "Merge:%s.pdf"%(title)
arglen=len(sys.argv)
if arglen<2 or arglen>3:
	print "Usage:\n\t%s threads [workdir]"%sys.argv[0]
	exit()
if arglen==3:
	workdir=sys.argv[2]
else:
	workdir="./"
threads=int(sys.argv[1])
for d in ['problem','contest']:
	d=workdir+d
	if not os.path.exists(d):
		print "makedirs:%s"%d
		os.makedirs(d)

contest=[]
for x in open(workdir+"html_list.txt").read().split('\n'):
	s=x.split('----')
	if len(s)!=3:
		continue
	c=(s[0],s[1],s[2].split(','))
	contest.append(c)
cur=0
end=len(contest)
lock = threading.RLock()
print "%d contests loaded"%(end)
class gogogo(threading.Thread):
    def __init__(this):
        threading.Thread.__init__(this)
    def run(this):
    	global cur
    	while cur<end:
	    	lock.acquire()
	    	curcontest=contest[cur]
	    	cur+=1
	    	lock.release()
	    	html2pdf(curcontest)

print "%d threads used,save in %s"%(threads,workdir)
for i in range(threads):
	gogogo().start()
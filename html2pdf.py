import urllib
import urllib2
import re
import os
import threading

def html2pdf(contest):
	cat="pdftk"
	cid=contest[0]
	title=contest[1]
	for x in contest[2]:
		html_path='html/'+cid+'_'+x+'.html'
		problem='"problem/'+cid+'_'+x+'.pdf"'
		cmd='wkhtmltopdf -q "'+html_path+'" '+problem
		os.popen(cmd)
		cat+=' '+problem
		lock.acquire()
		print "Generate:%s_%s.pdf"%(cid,x)
		lock.release()
	contest_path='"contest/'+title+'.pdf"'
	cat+=' cat output '+contest_path
	os.popen(cat)
	print "Merge:%s.pdf"%(title)

contest=[]
for x in open("html_list.txt").read().split('\n'):
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
threads=8
print "%d threads used"%(threads)
for i in range(threads):
	gogogo().start()
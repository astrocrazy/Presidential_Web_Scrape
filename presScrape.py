import urllib
from bs4 import BeautifulSoup
import re

def sourceLookup(pres):
	print 'Looking Up Webpage...'
	s = pres
	url = 'http://en.m.wikipedia.org/wiki/'
	name = s.split()
	size = len(name)
	x=0
	z=1
	while x < size:
		if z<size:
			url = url+ name[x]+'_'
		else: 
			url = url+ name[x]
		x=x+1
		z=z+1
	html = urllib.urlopen(url)
	print 'Done'
	print 'Accessing Source'
	source = html.read()
	print 'Done'
	html.close()
	return source

def keyInfoTableFilter(source):
	soup = BeautifulSoup(source)
	#soup.prettify()
	print 'Getting Information'
	infotable=soup.find('table',{'class':'infobox vcard'})
	print 'Done'
	#infotable.prettify()
	return infotable

def main(pres):
	file = open('President.txt','r')
	source = sourceLookup(pres)
	infotable = keyInfoTableFilter(source)
	infotable = removeAttrs(infotable)
	#print infotable
	print'Filing Information'
	array=[]
	thArray=[]
	for t in infotable.findAll('td'):
		array.append(t.contents)
	for t in infotable.findAll('th'):
		thArray.append(t.contents)
	print 'Done'
	z=0
	w=0
	print 'Filtering Extra Symbols'
	finalArr =[]
	finalthArr=[]
	for t in array:
		t=str(t)
		t=remove_html_tags(t)
		t=removeStuff(t)
		t=replaceCommas(t)
		t=replaceHyphens(t)
		finalArr.insert(z,t)
		z=z+1
	for t in thArray:
		t=str(t)
		t=remove_html_tags(t)
		t=removeStuff(t)
		t=replaceCommas(t)
		t=replaceHyphens(t)
		finalthArr.insert(w,t)
		w=w+1
	z=0
	if 'Personal details' in finalthArr:
		finalthArr.remove('Personal details')
	if 'Incumbent' in finalthArr:
		finalthArr.remove('Incumbent')
	if 'Military service' in finalthArr:
		finalthArr.remove('Military service')
	for t in finalthArr:
		print str(z)+'. '+t + ': '+finalArr[z]
		z+=1
	print 'split'
	#z=0
	#for t in finalthArr:
		#print str(z)+'. '+t
		#z+=1
	print 'Done'
	
def removeAttrs(soup):
	for tag in soup.findAll(True): 
		tag.attrs = None
	return soup

def remove_html_tags(data):
	p = re.compile(r'<.*?>')
	return p.sub('', data)

def removeStuff(data):
	#return re.sub(r'u\'\\n\'',"",data)
	return re.sub(r'\[[0-9][0-9]\]|u\'\\n\'|\[[0-9][0-9][0-9]\]|u\'\s+\'|,',"",data)

def replaceCommas(text):
	regex = re.compile("""(January|February|March|April|June|July|August|September|October|November|December)[ ]([0-9]{1,2})[ ]([0-9]{4})""", re.X)
	return regex.sub(r"\1 \2, \3", text)

def replaceHyphens(text):
	text= re.sub(r'\\xa0\\',r' -', text)
	text= re.sub(r'u2013',r'', text)
	text = re.sub(r'u\'\\n|\[|\]',r'',text)
	text = re.sub(r'u\' \'',r'',text)
	text = re.sub(r'u\'|\'',r'',text)
	text = re.sub(r'\\', r'-',text)
	text = re.sub(r'\-u2022','',text)
	return re.sub(r'\\xa0|\s+',r' ', text) 

file = open('President.txt','r')
for num in range(0,45):
	pres=file.readline()
	main(pres)

import urllib2
import sys
import codecs
import urlparse
try: 
    from BeautifulSoup import BeautifulSoup
except ImportError:
    from bs4 import BeautifulSoup
	
def setOutputUTF8():
	UTF8Writer = codecs.getwriter('utf8')
	sys.stdout = UTF8Writer(sys.stdout)
	reload(sys)  
	sys.setdefaultencoding('utf8')
	
	
def getChapterUrl(url, chapter, bookName):
	return str(url + "/" + str(chapter) + "/"+ bookName)

def manageURL(url):
	parsedURL = urlparse.urlparse(url)
	repartitioned = parsedURL.path.rpartition('/')
	bookName = repartitioned[2]
	newPath = repartitioned[0].rpartition('/')[0]
	url = "http://" + parsedURL.netloc + newPath
	return(url, bookName)
	
def printBook(url, bookName):
	response = urllib2.urlopen(getChapterUrl(url, 1, bookName))
	page_source = response.read()
	parsed_html = BeautifulSoup(page_source)
	options = parsed_html.body.find('select', attrs={'name':'chapter'}).findAll("option")

	for option in options:
		for attribute in option.attrs:
			if attribute[0] == u'value':
				try:
					chapterURL = getChapterUrl(url, attribute[1], bookName)
					print("chapterURL: %s"%chapterURL)
					response2 = urllib2.urlopen(chapterURL)
					parsed_html = BeautifulSoup(response2.read())
					allParagraphs =  parsed_html.findAll('p')
					
					for line in allParagraphs:
						lineText = line.getText().replace('\r\n', ' ').replace('\n', ' ')
						print(lineText)
					sys.exit(0)
				except:
					continue


if __name__== "__main__":
	#set sys.out to support utf8
	setOutputUTF8()

	#get url
	url = sys.argv[1]

	#get url for the book in general and book name
	(url, bookName) = manageURL(url)

	#go over the chapters and print them out
	printBook(url, bookName)

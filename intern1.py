# import libraries
import urllib.request
from bs4 import BeautifulSoup
import re
from datetime import datetime
import xlsxwriter

class AppURLopener(urllib.request.FancyURLopener):
    version = "Mozilla/5.0"

class WebScrapper:
    def __init__(self, homePage, rootUrl):
        self.homePage = homePage
        self.rootUrl = rootUrl
        self.currentUrl = self.rootUrl
        self.opener = AppURLopener()
        self.links = []


    def findTags(self, url, tag, tagDict):
        # query the website and return the html to the variable ‘page’
        # parse the html using beautiful soup and store in variable `soup`
        page = self.opener.open(url)
        print("warn", url)
        soup = BeautifulSoup(page, 'html.parser')
        print("warn")

        # find all the tags
        scrappedTags = soup.find_all(tag, attrs=tagDict)
        print("warn")
        print(scrappedTags)
        return scrappedTags



    def getAllAnchorTags(self, scrappedTags, regExp):
        for eachBlock in scrappedTags:
            for eachTag in eachBlock:
                matchObj = re.match(r'(.*)(\/shareprice.*)(")', str(eachTag), re.M | re.I)
                try:
                    relativeDir = matchObj.group(2)
                    completeLink = self.homePage + relativeDir
                    print(completeLink)
                    self.links.append(completeLink)
                except:
                    print("error in regex")
                    pass
        return self.links

    def scrapeEachLink(self, links):
        for eachLink in links:
            print(eachLink)

def main():
    webObj = WebScrapper("https://www.moneyam.com", "https://www.moneyam.com/share-list_T.html")
    tags = webObj.findTags("https://www.moneyam.com/share-list_T.html",'tr' ,{'class': 'stdTblRow'})
    links = webObj.getAllAnchorTags(tags, '(.*)(\/shareprice.*)(")')
    webObj.scrapeEachLink(links)

main()
'''










class AppURLopener(urllib.request.FancyURLopener):
    version = "Mozilla/5.0"

opener = AppURLopener()

quote_page = "https://www.moneyam.com/share-list_T.html"

# query the website and return the html to the variable ‘page’
page = opener.open(quote_page)
# parse the html using beautiful soup and store in variable `soup`
soup = BeautifulSoup(page, 'html.parser')

# Take out the <div> of name and get its value

name_box = soup.find_all('tr', attrs={'class': 'stdTblRow'})
for i in name_box:
    name = i.text.strip() # strip() is used to remove starting and trailing
    #print (i)
    for j in i:
        print(str(j))
        matchObj = re.match(r'(.*)(\/shareprice.*)(")', str(j), re.M | re.I)
        try:
            print(matchObj.group(2))
        except:
            pass
# get the index price


workbook = xlsxwriter.Workbook('hello.xlsx')
worksheet = workbook.add_worksheet()

worksheet.write('A1', name)
worksheet.write('B1', datetime.now())

workbook.close()# specify the url'''
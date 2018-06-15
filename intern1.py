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
        #print("warn", url)
        soup = BeautifulSoup(page, 'html.parser')
        #print("warn")

        # find all the tags
        scrappedTags = soup.find_all(tag, attrs=tagDict)
        #print("warn")
        #print(scrappedTags)
        return scrappedTags



    def getAllAnchorTags(self, scrappedTags, regExp):
        for eachBlock in scrappedTags:
            for eachTag in eachBlock:
                matchObj = re.match(r'(.*)(\/shareprice.*)(")', str(eachTag), re.M | re.I)
                try:
                    relativeDir = matchObj.group(2)
                    completeLink = self.homePage + relativeDir
                    #print(completeLink)
                    self.links.append([eachBlock.text.strip().split("\n"), completeLink])
                except:
                    #print("error in regex")
                    pass
        return self.links

    def scrapeLink(self, tags):
        for each in tags:
            name = each.text.strip().split()  # strip() is used to remove starting and trailing
            name = ''.join(name)
            # print(name)
            matchObj = re.match(r'.*(Bidprice\d*\.\d*)(Openprice\d*\.\d*)(Askprice\d*\.\d*)(Prevclose\d*\.\d*).*',
                                str(name), re.M | re.I)
            try:
                #print(matchObj.group(1), matchObj.group(2), matchObj.group(3), matchObj.group(4))
                return matchObj.group(1), matchObj.group(2), matchObj.group(3), matchObj.group(4)
            except:
                pass


def main():
    dataList = []
    webObj = WebScrapper("https://www.moneyam.com", "https://www.moneyam.com/share-list_T.html")
    tags = webObj.findTags("https://www.moneyam.com/share-list_T.html",'tr' ,{'class': 'stdTblRow'})
    links = webObj.getAllAnchorTags(tags, '(.*)(\/shareprice.*)(")')
    #print(links)
    count = 1
    for eachLink in links:
        try:
            if(count != 43):
                tags = webObj.findTags(eachLink[1], 'div', {'class': 'ui-helper-clearfix'})
                bid, open, ask, prev = webObj.scrapeLink(tags)
                currentData = [eachLink[0][0], eachLink[0][1], eachLink[0][2], bid, open, ask, prev]
                dataList.append(currentData)
                print(currentData)
                print(count)
            count+=1
        except:
            print("error at", count)



class excelWriter:
    def __init__(self, fileName):
        self.saveFile = fileName

    def writeIntoFile(self, content):
        pass



main()
print("Finished")


'''class AppURLopener(urllib.request.FancyURLopener):
    version = "Mozilla/5.0"

opener = AppURLopener()

quote_page = "https://www.moneyam.com/shareprice/TPFZ"

# query the website and return the html to the variable ‘page’
page = opener.open(quote_page)
# parse the html using beautiful soup and store in variable `soup`
soup = BeautifulSoup(page, 'html.parser')

# Take out the <div> of name and get its value

name_box = soup.find_all('div', attrs={'class': 'ui-helper-clearfix'})
for each in name_box:
    name = each.text.strip().split() # strip() is used to remove starting and trailing
    name = ''.join(name)
    #print(name)
    matchObj = re.match(r'.*(Bidprice\d*\.\d*)(Openprice\d*\.\d*)(Askprice\d*\.\d*)(Prevclose\d*\.\d*).*', str(name), re.M | re.I)
    try:
        print(matchObj.group(1), matchObj.group(2), matchObj.group(3), matchObj.group(4))
    except:
        pass
        #print("qq",name,"qq")

workbook = xlsxwriter.Workbook('hello.xlsx')
worksheet = workbook.add_worksheet()

worksheet.write('A1', name)
worksheet.write('B1', datetime.now())

workbook.close()# specify the url'''
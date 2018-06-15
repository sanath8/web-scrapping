# import libraries
import urllib.request
from bs4 import BeautifulSoup
import csv
from datetime import datetime
import xlsxwriter



quote_page = 'https://stackoverflow.com/questions/34475051/need-to-install-urllib2-for-python-3-5-1'

# query the website and return the html to the variable ‘page’
page = urllib.request.urlopen(quote_page)
# parse the html using beautiful soup and store in variable `soup`
soup = BeautifulSoup(page, 'html.parser')

# Take out the <div> of name and get its value
name_box = soup.find('a', attrs={'class': 'question-hyperlink'})
name = name_box.text.strip() # strip() is used to remove starting and trailing
print (name_box, name)
# get the index price
'''price_box = soup.find('div', attrs={'class' : 'price'})
price = price_box.text
print (price)'''
# open a csv file with append, so old data will not be erased

workbook = xlsxwriter.Workbook('hello.xlsx')
worksheet = workbook.add_worksheet()

worksheet.write('A1', name)
worksheet.write('B1', datetime.now())

workbook.close()# specify the url
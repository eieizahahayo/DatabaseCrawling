import bs4
import requests
import xlsxwriter
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import datetime
import time

def crawInfo(input,f,count,n):
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}
    response = requests.get(input, headers=headers)
    page = soup(response.content, "html5lib")
    # f.write("S.No,Research Title,Journal Name,Volume and Date of publication,Keywords,Doi number,Author name,Affiliation,Email ID\n")

    #------------Title----------------------------------------------------------------
    try:
        title = page.find("span",{"class":"hlFld-Title"})
        print("Title : " + title.cite.text)
    except Exception as e:
        print("Exception title : " + str(e))

    #------------Journal Name----------------------------------------------------------------
    try:
        journal = page.find("div",{"id":"citation"})
        print("Journal : " + journal.text)
    except Exception as e:
        print("Exception title : " + str(e))

    #------------Volume----------------------------------------------------------------
    try:
        voldiv = page.find("div",{"id":"citation"})
        vol = page.findAll("span")
        date = ""
        for each in vol:
            date += each.text
        print("Journal : " + date)
    except Exception as e:
        print("Exception volume + date : " + str(e))


#-------------------------------------------------------------------------------------------------------------------------------
def acs(input,name):
    now = datetime.datetime.now()
    filename = "ACS_" + name + ".xlsx"
    filepath = "acs/csv/" + filename
    workbook = xlsxwriter.Workbook(filepath)
    f = workbook.add_worksheet()
    f.write('A1', 'Keyword : ')
    f.write('B1', input)
    f.write('A2', 'Database : ')
    f.write('B2', 'http://journals.sagepub.com/')
    f.write('A3', 'Date : ')
    f.write('B3', str(now.isoformat()))
    for i in range(0,999999):
        try:
            link = []
            headers = {
                'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}
            my_url = 'https://pubs.acs.org/action/doSearch?AllField=' + input.replace(" ","+") + '&pageSize=100&startPage=' + str(i)
            response = requests.get(my_url, headers=headers)
            page = soup(response.content, "html5lib")
            body = page.findAll("div",{"class":"art_title linkable"})
            print("---------------------------------------------------------------")
            count = 1
            n = 4
            print(my_url)
            print(len(body))
            for each in body:
                link.append("https://pubs.acs.org" + each.a['href'])
                print("link : https://pubs.acs.org" + each.a['href'])
            for each in link:
                n = crawInfo(each,f,count,n)
                count += 1
        except Exception as e:
            print("Exception big : " + str(e))
    f.close()

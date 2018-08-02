import bs4
import requests
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import datetime
import re
import xlsxwriter
import time
import random

def crawling(f,input,first,last):
    count = 1
    n = 5
    values = [5,30,35,40,45,50,55,60,120]
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}
    print("enter arXiv")
    my_url = 'https://arxiv.org/search/?query=' + input.replace(" ","+") + '&searchtype=journal_ref&order=-announced_date_first&size=50'
    response = requests.get(my_url, headers=headers)
    page = soup(response.content, "html5lib")
    body = page.findAll("a")
    links = []
    for a in body:
        if("arXiv:" in a.text):
            links.append(a['href'])
    for each in links:
        print("try : " + each)
        time.sleep(random.choice(values))
        n = crawInfoArxiv(each,f,count,n)
        count +=1
    for i in range(int(first)+1,int(last)):
        try:
            headers = {
                'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}
            print("enter arXiv")
            my_url = 'https://arxiv.org/search/?query=' + input.replace(" ","+") + '&searchtype=journal_ref&order=-announced_date_first&size=50&start=' + str(i*50)
            response = requests.get(my_url, headers=headers)
            page = soup(response.content, "html5lib")
            body = page.findAll("a")
            links = []
            for a in body:
                if("arXiv:" in a.text):
                    links.append(a['href'])
            for each in links:
                print("try : " + each)
                n = crawInfoArxiv(each,f,count,n)
                count +=1
        except Exception as e:
            print("Exception : " + str(e))
            print("Exception page : " + str(i))
            if("Connection aborted." in str(e) or "HTTPSConnectionPool" in str(e) or "Connection broken:" in str(e)):
                print("Internet is down")
                time.sleep( 60 )
            else:
                break

def init(f,input):
    now = datetime.datetime.now()
    f.write('A1', 'Keyword : ')
    f.write('B1', input)
    f.write('A2', 'Database : ')
    f.write('B2', 'https://arxiv.org/')
    f.write('A3', 'Date : ')
    f.write('B3', str(now.isoformat()))
    f.write('A4', 'S.No')
    f.write('B4', 'Website')
    f.write('C4', 'Title')
    f.write('D4', 'Subject')
    f.write('E4', 'Date')
    f.write('F4', 'Ref')
    f.write('G4', 'Doi number')
    f.write('H4', 'Author name')

def crawInfoArxiv(url,f,count,n):
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}
    response = requests.get(url, headers=headers)
    page = soup(response.content, "html5lib")
    body = page.find("body")
    re = {"\n":" " , ",":" ","Title:":" ","Authors:":" "}

    #-------------------Initialization--------------------------------------------------------
    try:
        print("link : " + url)
        f.write('A' + str(n) , str(count))
        f.write('B' + str(n) , url)
    except Exception as e:
        if("Connection aborted." in str(e) or "HTTPSConnectionPool" in str(e) or "Connection broken:" in str(e)):
            print("Internet is down")
            time.sleep( 60 )



    #-------------------------Title---------------------------------
    try:
        title = body.find("h1",{"class":"title mathjax"})
        print("Title : " + replace_all(title.text,re))
        f.write('C' + str(n) , title.text)
    except Exception as e:
        if("Connection aborted." in str(e) or "HTTPSConnectionPool" in str(e) or "Connection broken:" in str(e)):
            print("Internet is down")
            time.sleep( 60 )
        f.write('C' + str(n) , 'Cannot get title')
        print("Exception Title : " + str(e))

    #-------------------------Subject---------------------------------
    try:
        subj = body.find("span",{"class":"primary-subject"})
        print("Subject : " + replace_all(subj.text,re))
        f.write('D' + str(n) , subj.text)
    except Exception as e:
        if("Connection aborted." in str(e) or "HTTPSConnectionPool" in str(e) or "Connection broken:" in str(e)):
            print("Internet is down")
            time.sleep( 60 )
        f.write('D' + str(n) , 'Cannot get subject')
        print("Exception Subject : " + str(e))

    #-------------------------Date---------------------------------
    try:
        date = body.find("div",{"class":"dateline"})
        print("Date : " + replace_all(date.text,re))
        f.write('E' + str(n) , date.text)
    except Exception as e:
        if("Connection aborted." in str(e) or "HTTPSConnectionPool" in str(e) or "Connection broken:" in str(e)):
            print("Internet is down")
            time.sleep( 60 )
        f.write('E' + str(n) , 'Cannot get date')
        print("Exception Date : " + str(e))

    #-------------------------Ref---------------------------------
    try:
        ref = body.find("td",{"class":"tablecell jref"}).text
        print("Ref : " + replace_all(ref,re))
        f.write('F' + str(n) , ref)
    except Exception as e:
        if("Connection aborted." in str(e) or "HTTPSConnectionPool" in str(e) or "Connection broken:" in str(e)):
            print("Internet is down")
            time.sleep( 60 )
        f.write('F' + str(n) , 'Cannot get ref')
        print("Exception ref : " + str(e))

    #-------------------------DOI---------------------------------
    arr = [{"class":"tablecell doi"},{"class":"tablecell report-number"}]
    check = False
    check2 = False
    try:
        for each in arr:
            try:
                if(check):
                    break
                divDoi = body.find("div","metatable")
                doi = divDoi.find("td",each)
                print("Doi : " + doi.text)
                f.write('F' + str(n) , doi.text)
                check = True
                print("DOI True 1")
            except:
                if("Connection aborted." in str(e) or "HTTPSConnectionPool" in str(e) or "Connection broken:" in str(e)):
                    print("Internet is down")
                    time.sleep( 60 )
                continue
    except Exception as e:
        if("Connection aborted." in str(e) or "HTTPSConnectionPool" in str(e) or "Connection broken:" in str(e)):
            print("Internet is down")
            time.sleep( 60 )
        f.write('G' + str(n) , 'Cannot get doi')
        check2 = True
        print("DOI True 2")
        print("Exception doi : " + str(e))
    if(check == False and check2 == False):
        f.write('G' + str(n) , 'Cannot get doi')
        print("Cannot get doi")

    #-------------------------Authors---------------------------------
    try:
        divAut = body.find("div",{"class":"authors"})
        auts = divAut.findAll("a")
        for i in range(0,len(auts)):
            print("Authors : " + replace_all(auts[i].text,re))
            f.write('H' + str(n) , auts[i].text)
            n += 1
    except Exception as e:
        if("Connection aborted." in str(e) or "HTTPSConnectionPool" in str(e) or "Connection broken:" in str(e)):
            print("Internet is down")
            time.sleep( 60 )
        f.write('H' + str(n) , 'Cannot get authors')
        print("Exception Authors : " + str(e))

    print("-------------------------------------------------------------------------------")
    return n

#-------------------------------------------------arXiv------------------------------------------------------------------------------
def arXiv(input,name,first,last):
    filename = "arxiv_" + name + ".xlsx"
    filepath = "arxiv/csv/" + filename
    workbook = xlsxwriter.Workbook(filepath)
    f = workbook.add_worksheet()
    init(f,input)
    crawling(f,input,first,last)
    workbook.close()

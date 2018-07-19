import bs4
import requests
import xlsxwriter
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import datetime

def crawInfo(input,f,count,n):
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}
    response = requests.get(input, headers=headers)
    page = soup(response.content, "html5lib")

    #------------Title----------------------------------------------------------------
    try:
        title = page.find("div",{"class":"publicationContentTitle"})
        print("Title : " + title.h1.text)
    except Exception as e:
        print("Exception title : " + str(e))


#-------------------------------------------------------------------------------------------------------------------------------
def sage(input):
    for i in range(1,999999):
        if(i == 1):
            link = []
            headers = {
                'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}
            my_url = 'http://journals.sagepub.com/action/doSearch?AllField=' + input.replace(" ","+") + '&pageSize=100&startPage=' + str(i)
            response = requests.get(my_url, headers=headers)
            page = soup(response.content, "html5lib")
            now = datetime.datetime.now()
            filename = "Sagepub_" + input.replace(" ","_") + ".xlsx"
            filepath = "sagepub/csv/" + filename
            workbook = xlsxwriter.Workbook(filepath)
            f = workbook.add_worksheet()
            f.write('A1', 'Keyword : ')
            f.write('B1', input)
            f.write('A2', 'Database : ')
            f.write('B2', 'http://journals.sagepub.com/')
            f.write('A3', 'Date : ')
            f.write('B3', str(now.isoformat()))
            body = page.findAll("article",{"class":"searchResultItem"})
            # print(page.find("article",{"class":"searchResultItem"}).h2.text)
            print("---------------------------------------------------------------")
            count = 1
            n = 4
            print(len(body))
            for each in body:
                link.append("http://journals.sagepub.com" + each.h2.a['href'])
                print("link : http://journals.sagepub.com" + each.h2.a['href'])
            for each in link:
                n = crawInfo(each,f,count,n)
                count += 1
        # else:
        #     try:
        #         headers = {
        #             'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}
        #         my_url = 'https://link.springer.com/search/page/' + str(i) + '?facet-content-type=%22Article%22&query=' + input.replace(" ","+")
        #         response = requests.get(my_url, headers=headers)
        #         page = soup(response.content, "html5lib")
        #         now = datetime.datetime.now()
        #         body = page.findAll("li",{"class":"no-access"})
        #         print(len(body))
        #         print("---------------------------------------------------------------")
        #         count = 1
        #         n = 4
        #         for each in body:
        #             link.append(each.h2.a['href'])
        #             print("link : " + each.h2.a['href'])
        #         for each in link:
        #             n = crawInfo(each,f,count,n)
        #             count += 1
        #     except Exception as e:
        #         print("Exception else : " + str(e))
        #         break
    workbook.close()

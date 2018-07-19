import bs4
import requests
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import datetime
import xlsxwriter

#-----------------------------------------------ScienceDirect--------------------------------------------------------------------------------
def scienceDirect(input,name):
    filename = "scienceDirect_" + name + ".xlsx"
    filepath = "scienceDirect/csv/" + filename
    now = datetime.datetime.now()
    workbook = xlsxwriter.Workbook(filepath)
    f = workbook.add_worksheet()
    f.write('A1', 'Keyword : ')
    f.write('B1', input)
    f.write('A2', 'Database : ')
    f.write('B2', 'https://www.sciencedirect.com/')
    f.write('A3', 'Date : ')
    f.write('B3', str(now.isoformat()))
    count = 1
    n = 4
    f.write('A' + str(n) , 'S.No')
    f.write('B' + str(n) , 'Website')
    f.write('C' + str(n) , 'Title')
    f.write('D' + str(n) , 'Journal name')
    f.write('E' + str(n) , 'Volume and date')
    f.write('F' + str(n) , 'Keywords')
    f.write('G' + str(n) , 'Doi number')
    f.write('H' + str(n) , 'Author name')
    f.write('I' + str(n) , 'Email')
    f.write('K' + str(n) , 'Affiliation')
    f.write('L' + str(n) , 'Country')
    n += 1
    offset = 0
    count = 1
    for i in range(0,99999):
        try:
            print("enter SD")
            headers = {
                'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}
            breaker = False
            print("------------------------------------------------------------------------")
            my_url = 'https://www.sciencedirect.com/search?qs=' + input.replace(" ","%20") + '&show=100&sortBy=relevance&offset=' + str(offset)
            offset += 100
            response = requests.get(my_url, headers=headers)
            page = soup(response.content, "html5lib")
            body = page.findAll("a",{"class":"result-list-title-link u-font-serif text-s"})
            stop = body[0].text
            links = []
            checker = []
            for each in body:
                links.append(each['href'])
            for each in links:
                print("try : " + each)
                n = crawInfoScienceDirect(each,f,count,n)
                count += 1
                n += 1
        except Exception as e:
            print("Exception big : " + str(e))
            break
    print("-------------------------------------")
    print(input)
    workbook.close()



def crawInfoScienceDirect(input,f,count,n):
    print("------------------------------------------------------------------------")
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}
    url = "https://www.sciencedirect.com"+input
    response = requests.get(url, headers=headers)
    page = soup(response.content, "html5lib")
    body = page.find("body")

    #---------------------------Initialization---------------------------------------------------------
    print(url)
    f.write('A' + str(n) , str(count))
    f.write('B' + str(n) , url)

    #---------------------------Title---------------------------------------------------------
    try:
        temp = [{"tag": "span", "className": {"class":"title-text"}}, {"tag":"span", "className":{"class":"reference"}}, {"tag":"h1", "className":{"class":"svTitle"}}]
        checkTitle = False
        for each in temp:
            if(checkTitle):
                break
            title = body.find(each['tag'] , each['className'])
            print("Title : " + title.text)
            f.write('C' + str(n) , title.text)
            checkTitle = True
    except Exception as e:
        print("Exception title : " + str(e))
        f.write('C' + str(n) , 'Cannot get title')
    #---------------------------Journal---------------------------------------------------------
    try:
        findFieldStudy = [{"tag": "a", "className": {"class":"publication-title-link"}}, {"tag":"div", "className":{"class":"title"}}]
        done = False
        for ele in findFieldStudy:
            try:
                if(done):
                    break
                journal = body.find(ele['tag'],ele['className'])
                print("Journal : " + journal.text)
                f.write('D' + str(n) , journal.text)
                done = True
            except:
                continue
        if(done == False):
            print("Field of study is a picture.")
            f.write('D' + str(n) , 'Cannot get journal')
    except Exception as e:
        print("Exception journal : " + str(e))
        f.write('D' + str(n) , 'Cannot get journal')

    #---------------------------Detail---------------------------------------------------------
    ans = ""
    try:
        detail = body.find("div",{"class":"text-xs"}).text
        print(detail)
        ans += detail
        print("done try 1")
    except Exception as e:
        print("Exception1 : " + str(e))
        f.write('E' + str(n) , 'Cannot get detail')

    try:
        vol = body.find("p",{"class":"specIssueTitle"}).text
        print(vol)
        ans += vol
        print("done try 3")
    except Exception as e:
        print("Exception3 : " + str(e))
        f.write('E' + str(n) , 'Cannot get detail')

    try:
        detail = body.find("p",{"class":"volIssue"}).text
        print(detail)
        ans += detail
        print("done try 2")
    except Exception as e:
        print("Exception2 : " + str(e))
        f.write('E' + str(n) , 'Cannot get detail')

    f.write('E' + str(n) , ans)

    #---------------------------Key words---------------------------------------------------------
    kwAns = []
    doi = ""
    findArr = [{"tag":"div","className":{"class":"keywords-section"}},{"tag":"ul","className":{"class":"keyword"}},{"tag":"div","className":{"class":"svKeywords"}}]
    alreadyDone = False
    for ele in findArr:
        try:
            if(alreadyDone):
                break
            kw = body.find(ele['tag'], ele['className'])
            temp2 = kw.findAll("span")
            alreadyDone = True
            for i in range(len(temp2)):
                kwAns.append(temp2[i].text)
                #doi number --------------------------------------------------
                doiArr = [{"class":"doi"},{"class":"S_C_ddDoi"}]
                done = False
                for ele in doiArr:
                    try:
                        if(done):
                            break
                        doi = body.find("a",ele)
                        print(doi.text)
                        f.write('G' + str(n) , doi.text)
                        done = True
                    except:
                        continue
                if(done == False):
                    print("Cannot get DOI")
                    f.write('G' + str(n) , 'Cannot get DOI')
                #-------------------------------------------------------------
        except Exception as e:
            continue
    if(alreadyDone == False):
        print("no keywords")
        kwAns.append("no keywords")
        #doi number --------------------------------------------------
        doiArr = [{"class":"doi"},{"class":"S_C_ddDoi"}]
        done = False
        for ele in doiArr:
            try:
                if(done):
                    break
                doi = body.find("a",ele)
                print(doi.text)
                f.write('G' + str(n) , doi.text)
                done = True
            except Exception as e:
                print("except : " + str(e))
                continue
        if(done == False):
            print("Cannot get DOI")
            f.write('G' + str(n) , 'Cannot get DOI')
        #-------------------------------------------------------------
        for each in kwAns:
            f.write('F' + str(n) , each)
            n += 1
    else:
        try:
            for each in kwAns:
                f.write('F' + str(n) , each)
                n += 1
        except Exception as e:
            print("Exception kw : " + str(e))
    print("-----------------------------------------------------------------")
    return n

import bs4
import requests
import xlsxwriter
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import datetime
import re
import random

def init(f,input):
    f.write('A1', 'Keyword : ')
    f.write('B1', input)
    f.write('A2', 'Database : ')
    f.write('B2', 'https://link.springer.com/')
    f.write('A3', 'Date : ')
    f.write('B3', str(now.isoformat()))
    f.write('A4', 'S.No')
    f.write('B4', 'Website')
    f.write('C4', 'Title')
    f.write('D4', 'Journal name')
    f.write('E4', 'Volume')
    f.write('F4', 'Date')
    f.write('G4', 'Keywords')
    f.write('H4', 'Doi number')
    f.write('I4', 'Author name')
    f.write('J4', 'E-mail')
    f.write('K4', 'Affiliation')
    f.write('L4', 'Country')

def crawling(f,input):
    count = 1
    n = 5
    values = [5,30,35,40,45,50,55,60,120]
    for i in range(1,999999):
        try:
            link = []
            headers = {
                'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}
            my_url = 'https://link.springer.com/search/page/' + str(i) + '?facet-content-type=%22Article%22&query=' + input.replace(" ","+")
            response = requests.get(my_url, headers=headers)
            page = soup(response.content, "html5lib")
            body = page.findAll("li",{"class":"no-access"})
            print(len(body))
            if(len(body) == 0):
                break
            print("---------------------------------------------------------------")
            for each in body:
                link.append(each.h2.a['href'])
                print("link : " + each.h2.a['href'])
            for each in link:
                time.sleep(random.choice(values))
                n = crawInfo(each,f,count,n)
                count += 1
                n += 1
        except Exception as e:
            print("Exception else : " + str(e))
            if("Connection aborted." in str(e) or "HTTPSConnectionPool" in str(e) or "Connection broken:" in str(e)):
                print("Internet is down")
                time.sleep( 60 )
            else:
                break

def checkCountry(text):
    check = True
    countryArr = ["Afghanistan", "Albania", "Algeria", "American Samoa", "Andorra", "Angola", "Anguilla", "Antarctica", "Antigua and Barbuda", "Argentina", "Armenia", "Aruba", "Australia", "Austria", "Azerbaijan", "Bahamas", "Bahrain", "Bangladesh", "Barbados", "Belarus", "Belgium", "Belize", "Benin", "Bermuda", "Bhutan", "Bolivia", "Bosnia and Herzegowina", "Botswana", "Bouvet Island", "Brazil", "British Indian Ocean Territory", "Brunei Darussalam", "Bulgaria", "Burkina Faso", "Burundi", "Cambodia", "Cameroon", "Canada", "Cape Verde", "Cayman Islands", "Central African Republic", "Chad", "Chile", "China", "Christmas Island", "Cocos (Keeling) Islands", "Colombia", "Comoros", "Congo", "Congo, the Democratic Republic of the", "Cook Islands", "Costa Rica", "Cote d'Ivoire", "Croatia (Hrvatska)", "Cuba", "Cyprus", "Czech Republic", "Denmark", "Djibouti", "Dominica", "Dominican Republic", "East Timor", "Ecuador", "Egypt", "El Salvador", "Equatorial Guinea", "Eritrea", "Estonia", "Ethiopia", "Falkland Islands (Malvinas)", "Faroe Islands", "Fiji", "Finland", "France", "France Metropolitan", "French Guiana", "French Polynesia", "French Southern Territories", "Gabon", "Gambia", "Georgia", "Germany", "Ghana", "Gibraltar", "Greece", "Greenland", "Grenada", "Guadeloupe", "Guam", "Guatemala", "Guinea", "Guinea-Bissau", "Guyana", "Haiti", "Heard and Mc Donald Islands", "Holy See (Vatican City State)", "Honduras", "Hong Kong", "Hungary", "Iceland", "India", "Indonesia", "Iran", "Iraq", "Ireland", "Israel", "Italy", "Jamaica", "Japan", "Jordan", "Kazakhstan", "Kenya", "Kiribati", "Korea, Democratic People's Republic of", "Korea, Republic of", "Kuwait", "Kyrgyzstan", "Lao, People's Democratic Republic", "Latvia", "Lebanon", "Lesotho", "Liberia", "Libyan Arab Jamahiriya", "Liechtenstein", "Lithuania", "Luxembourg", "Macau", "Macedonia, The Former Yugoslav Republic of", "Madagascar", "Malawi", "Malaysia", "Maldives", "Mali", "Malta", "Marshall Islands", "Martinique", "Mauritania", "Mauritius", "Mayotte", "Mexico", "Micronesia, Federated States of", "Moldova, Republic of", "Monaco", "Mongolia", "Montserrat", "Morocco", "Mozambique", "Myanmar", "Namibia", "Nauru", "Nepal", "Netherlands", "Netherlands Antilles", "New Caledonia", "New Zealand", "Nicaragua", "Niger", "Nigeria", "Niue", "Norfolk Island", "Northern Mariana Islands", "Norway", "Oman", "Pakistan", "Palau", "Panama", "Papua New Guinea", "Paraguay", "Peru", "Philippines", "Pitcairn", "Poland", "Portugal", "Puerto Rico", "Qatar", "Reunion", "Romania", "Russian Federation","Russia", "Rwanda", "Saint Kitts and Nevis", "Saint Lucia", "Saint Vincent and the Grenadines", "Samoa", "San Marino", "Sao Tome and Principe", "Saudi Arabia", "Senegal", "Seychelles", "Sierra Leone", "Singapore", "Slovakia (Slovak Republic)","Scotland","Czechoslovakia", "Slovenia", "Solomon Islands", "Somalia", "South Africa", "South Georgia and the South Sandwich Islands", "Spain", "Sri Lanka", "St. Helena", "St. Pierre and Miquelon", "Sudan", "Suriname", "Svalbard and Jan Mayen Islands", "Swaziland", "Sweden", "Switzerland", "Syrian Arab Republic","Syria", "Taiwan, Province of China", "Tajikistan", "Tanzania, United Republic of", "Thailand", "Togo", "Tokelau", "Tonga", "Trinidad and Tobago", "Tunisia", "Turkey", "Turkmenistan", "Turks and Caicos Islands", "Tuvalu", "Uganda", "Ukraine", "United Arab Emirates", "United Kingdom","England", "United States","United States of America","America","U.S.A.", "United States Minor Outlying Islands", "Uruguay", "Uzbekistan", "Vanuatu", "Venezuela", "Vietnam", "Virgin Islands (British)", "Virgin Islands (U.S.)", "Wallis and Futuna Islands", "Western Sahara", "Yemen", "Yugoslavia", "Zambia", "Zimbabwe","USA","UK"]
    for each in countryArr:
        match = re.search(each, text)
        if(match):
            return match.group(0)
    if(check):
        return(" ")


def crawInfo(input,f,count,n):
    url = "https://link.springer.com" + input
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}
    response = requests.get(url, headers=headers)
    page = soup(response.content, "html5lib")

    #----------------------Initialization-----------------------------------------------------------------------------
    print(url)
    f.write('A' + str(n) , str(count))
    f.write('B' + str(n) , url)


    #------------------------Title---------------------------------------------------------------------------
    try:
        title = page.find("h1",{"class":"ArticleTitle"})
        print("Title : " + title.text)
        f.write('C' + str(n) , title.text)
    except Exception as e:
        print("Cannot get title : " + str(e))
        if("Connection aborted." in str(e) or "HTTPSConnectionPool" in str(e) or "Connection broken:" in str(e)):
            print("Internet is down")
            time.sleep( 60 )
        f.write('C' + str(n) , 'Cannot get title')


    #------------------------Journal name---------------------------------------------------------------------------
    try:
        jname = page.find("span",{"class":"JournalTitle"})
        print("Journal name : " + jname.text)
        f.write('D' + str(n) , jname.text)
    except Exception as e:
        print("Cannot get journal name : " + str(e))
        if("Connection aborted." in str(e) or "HTTPSConnectionPool" in str(e) or "Connection broken:" in str(e)):
            print("Internet is down")
            time.sleep( 60 )
        f.write('D' + str(n) , jname.text)

    #--------------------------Volume-------------------------------------------------------------------------
    try:
        volume = page.find("p",{"class":"icon--meta-keyline-before"})
        temp = volume.findAll("span")
        vol = ""
        for each in temp:
            vol = vol + each.text + " | "
        print(vol)
        f.write('E' + str(n) , vol)
    except Exception as e:
        print("Cannot get volume : " + str(e))
        if("Connection aborted." in str(e) or "HTTPSConnectionPool" in str(e) or "Connection broken:" in str(e)):
            print("Internet is down")
            time.sleep( 60 )
        f.write('E' + str(n) , 'Cannot get volume')

    #------------------------Date---------------------------------------------------------------------------
    try:
        date = page.find("div",{"class":"main-context__column"})
        print(date.div.text)
        # f.write(date.div.text + ",")
        f.write('F' + str(n) , date.div.text)
    except Exception as e:
        print("Cannot get date : " + str(e))
        if("Connection aborted." in str(e) or "HTTPSConnectionPool" in str(e) or "Connection broken:" in str(e)):
            print("Internet is down")
            time.sleep( 60 )
        f.write('F' + str(n) , 'Cannot get date')

    #------------------------Key words 1---------------------------------------------------------------------------
    try:
        keywords = page.findAll("span",{"class":"Keyword"})
    except Exception as e:
        print("Exception keywords : " + str(e))
        if("Connection aborted." in str(e) or "HTTPSConnectionPool" in str(e) or "Connection broken:" in str(e)):
            print("Internet is down")
            time.sleep( 60 )
        f.write('G' + str(n) , 'Cannot get keywords')


    #----------------------Doi-----------------------------------------------------------------------------
    try:
        doi = page.find("span",{"id" : "doi-url"})
        print(doi.text)
        # f.write(doi.text + ",")
        f.write('H' + str(n) , doi.text)
    except Exception as e:
        print("Exception doi : " + str(e))
        if("Connection aborted." in str(e) or "HTTPSConnectionPool" in str(e) or "Connection broken:" in str(e)):
            print("Internet is down")
            time.sleep( 60 )
        f.write('H' + str(n) , 'Cannot get DOI number')

    #---------------------Authors and email 1------------------------------------------------------------------------------
    authorsArr = []
    mailArr = []
    try:
        count = 1
        ul = page.findAll("ul",{"class":"test-contributor-names"})
        authors = ul[1].findAll("li",{"class":"u-mb-2 u-pt-4 u-pb-4"})
        for each in authors:
            if(len(each.text) > 1):
                name = each.span.text
                num = each.ul.text
                print("Authors : " + name + " | " + num + ".")
                authorsArr.append(name + " | " + num + ".")
                try:
                    mail = each.find("a",{"class":"gtm-email-author"})
                    print("Email : " + mail['title'])
                    mailArr.append(mail['title'])
                except Exception as e:
                    print("Exception Email : " + str(e))
                    mailArr.append("Email is not available")
                    if("Connection aborted." in str(e) or "HTTPSConnectionPool" in str(e) or "Connection broken:" in str(e)):
                        print("Internet is down")
                        time.sleep( 60 )
                count = count + 1
    except Exception as e:
        print("Exception authors : " + str(e))
        if("Connection aborted." in str(e) or "HTTPSConnectionPool" in str(e) or "Connection broken:" in str(e)):
            print("Internet is down")
            time.sleep( 60 )
        authorsArr.append("Cannot get author information")
        mailArr.append("Email is not available")


    #-------------------Affiliation--------------------------------------------------------------------------------
    affiArr = []
    try:
        ol = page.find("ol",{"class":"test-affiliations"})
        affi = ol.findAll("li")
        for each in affi:
            print("Affiliation : " + each.text)
            affiArr.append(each.text)
    except Exception as e:
        print("Exception Affiliation : " + str(e))
        if("Connection aborted." in str(e) or "HTTPSConnectionPool" in str(e) or "Connection broken:" in str(e)):
            print("Internet is down")
            time.sleep( 60 )
        affiArr.append("Cannot get affiliation")

    maximum = max([len(keywords),len(authorsArr),len(mailArr)])
    #------------------------Key words 2---------------------------------------------------------------------------
    kn = n
    for each in keywords:
        f.write('G' + str(kn) , each.text)
        kn += 1

    #------------------------Author and mail 2---------------------------------------------------------------------------
    an = n
    for each in authorsArr:
        f.write('I' + str(an) , each)
        an += 1

    mn = n
    for each in mailArr:
        f.write('J' + str(mn) , each.replace(" ",""))
        mn += 1

    #------------------------Affiliation 2 and country---------------------------------------------------------------------------
    afn = n
    for each in affiArr:
        country = checkCountry(each)
        f.write('K' + str(afn) , each)
        f.write('L' + str(afn) , country)
        afn += 1

    n += maximum

    print("-----------------------------------------------------------")
    return n

#-------------------------------------------------------------------------------------------------------------------------------
def springer(input,name):
    now = datetime.datetime.now()
    filename = "Springer_" + name + ".xlsx"
    filepath = "springer/csv/" + filename
    workbook = xlsxwriter.Workbook(filepath)
    f = workbook.add_worksheet()
    init(f,input)
    crawling(f,input)
    workbook.close()

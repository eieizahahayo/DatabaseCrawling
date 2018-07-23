import bs4
import requests
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import datetime
import re
import xlsxwriter
import pymongo
from pymongo import MongoClient

def connectDB():
    MdbURI = "mongodb://a:a123456@ds125381.mlab.com:25381/crawlerdata"
    client = MongoClient(MdbURI,connectTimeoutMS=30000)
    db = client.get_database("crawlerdata")
    return db.Wiley

def pushRECORD(record,mycol):
    mycol.insert_one(record)

def checkCountry(text,country):
    check = True
    countryArr = ["Afghanistan", "Albania", "Algeria", "American Samoa", "Andorra", "Angola", "Anguilla", "Antarctica", "Antigua and Barbuda", "Argentina", "Armenia", "Aruba", "Australia", "Austria", "Azerbaijan", "Bahamas", "Bahrain", "Bangladesh", "Barbados", "Belarus", "Belgium", "Belize", "Benin", "Bermuda", "Bhutan", "Bolivia", "Bosnia and Herzegowina", "Botswana", "Bouvet Island", "Brazil", "British Indian Ocean Territory", "Brunei Darussalam", "Bulgaria", "Burkina Faso", "Burundi", "Cambodia", "Cameroon", "Canada", "Cape Verde", "Cayman Islands", "Central African Republic", "Chad", "Chile", "China", "Christmas Island", "Cocos (Keeling) Islands", "Colombia", "Comoros", "Congo", "Congo, the Democratic Republic of the", "Cook Islands", "Costa Rica", "Cote d'Ivoire", "Croatia (Hrvatska)", "Cuba", "Cyprus", "Czech Republic", "Denmark", "Djibouti", "Dominica", "Dominican Republic", "East Timor", "Ecuador", "Egypt", "El Salvador", "Equatorial Guinea", "Eritrea", "Estonia", "Ethiopia", "Falkland Islands (Malvinas)", "Faroe Islands", "Fiji", "Finland", "France", "France Metropolitan", "French Guiana", "French Polynesia", "French Southern Territories", "Gabon", "Gambia", "Georgia", "Germany", "Ghana", "Gibraltar", "Greece", "Greenland", "Grenada", "Guadeloupe", "Guam", "Guatemala", "Guinea", "Guinea-Bissau", "Guyana", "Haiti", "Heard and Mc Donald Islands", "Holy See (Vatican City State)", "Honduras", "Hong Kong", "Hungary", "Iceland", "India", "Indonesia", "Iran", "Iraq", "Ireland", "Israel", "Italy", "Jamaica", "Japan", "Jordan", "Kazakhstan", "Kenya", "Kiribati", "Korea, Democratic People's Republic of", "Korea, Republic of", "Kuwait", "Kyrgyzstan", "Lao, People's Democratic Republic", "Latvia", "Lebanon", "Lesotho", "Liberia", "Libyan Arab Jamahiriya", "Liechtenstein", "Lithuania", "Luxembourg", "Macau", "Macedonia, The Former Yugoslav Republic of", "Madagascar", "Malawi", "Malaysia", "Maldives", "Mali", "Malta", "Marshall Islands", "Martinique", "Mauritania", "Mauritius", "Mayotte", "Mexico", "Micronesia, Federated States of", "Moldova, Republic of", "Monaco", "Mongolia", "Montserrat", "Morocco", "Mozambique", "Myanmar", "Namibia", "Nauru", "Nepal", "Netherlands", "Netherlands Antilles", "New Caledonia", "New Zealand", "Nicaragua", "Niger", "Nigeria", "Niue", "Norfolk Island", "Northern Mariana Islands", "Norway", "Oman", "Pakistan", "Palau", "Panama", "Papua New Guinea", "Paraguay", "Peru", "Philippines", "Pitcairn", "Poland", "Portugal", "Puerto Rico", "Qatar", "Reunion", "Romania", "Russian Federation","Russia", "Rwanda", "Saint Kitts and Nevis", "Saint Lucia", "Saint Vincent and the Grenadines", "Samoa", "San Marino", "Sao Tome and Principe", "Saudi Arabia", "Senegal", "Seychelles", "Sierra Leone", "Singapore", "Slovakia (Slovak Republic)","Scotland","Czechoslovakia", "Slovenia", "Solomon Islands", "Somalia", "South Africa", "South Georgia and the South Sandwich Islands", "Spain", "Sri Lanka", "St. Helena", "St. Pierre and Miquelon", "Sudan", "Suriname", "Svalbard and Jan Mayen Islands", "Swaziland", "Sweden", "Switzerland", "Syrian Arab Republic","Syria", "Taiwan, Province of China", "Tajikistan", "Tanzania, United Republic of", "Thailand", "Togo", "Tokelau", "Tonga", "Trinidad and Tobago", "Tunisia", "Turkey", "Turkmenistan", "Turks and Caicos Islands", "Tuvalu", "Uganda", "Ukraine", "United Arab Emirates", "United Kingdom","England", "United States" ,"U.S.A.","America","United States of America", "United States Minor Outlying Islands", "Uruguay", "Uzbekistan", "Vanuatu", "Venezuela", "Vietnam", "Virgin Islands (British)", "Virgin Islands (U.S.)", "Wallis and Futuna Islands", "Western Sahara", "Yemen", "Yugoslavia", "Zambia", "Zimbabwe","USA","UK"]
    for each in countryArr:
        match = re.search(each, text)
        if(match):
            country.append(match.group(0))
            check = False
    if(check):
        country.append(" ")

def contact(input,link,title,journal,vol,date,doi,mycol,kw):
    print("enter contact")
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}
    response = requests.get(input, headers=headers)
    page = soup(response.content, "html5lib")
    body = page.findAll("div",{"class":"accordion-tabbed__tab-mobile accordion__closed"})
    print(len(body))
    authors = []
    for i in range(len(body) // 2):
        name = ""
        email = []
        email2 = []
        country = []
        affiliation = []
        #--------------Authors----------------------------------------------
        print("Author : " + body[i].a.span.text)
        name = body[i].a.span.text
        try:
            add = body[i].find("div",{"class":"author-info accordion-tabbed__content"})
            try:
                allP = add.findAll("p")
                for each in allP:
                    print("Address : " + each.text)
                    affiliation.append(each.text)
                    match = re.search("(( )*[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+.[a-zA-Z0-9-.]+)", each.text)
                    if(match):
                        email.append(match.group(0))
                        print("Found email in author : " + match.group(0))
            except Exception as e:
                print("Exception address1 : " + str(e))
                affiliation.append("Cannot get affiliation")
        except Exception as e:
            print("Exception address2 : " + str(e))
            affiliation.append("Cannot get affiliation")

        #--------------email 1----------------------------------------------
        print("Len email : " + str(len(email)))
        try:
            info = body[i].find("div",{"class":"bottom-info"})
            match = re.search("(( )*[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)", info.text)
            if match:
                print("Email : " + match.group(0))
                email.append(match.group(0))
            else:
                print("Email not match :" + info.text)
                print("Email not match")
                if(len(email) == 0):
                    print("Enter if len(email)")
                    email.append("Cannot get email")
        except Exception as e:
            print("Exception email : " + str(e))
            if(len(email) == 0):
                print("Enter if len(email)")
                email.append("Cannot get email")

        #--------------email 2----------------------------------------------
        try:
            text = page.find("div",{"class":"article-header__correspondence-to"})
            match = re.search(body[i].a.span.text, text.text)
            if(match):
                match = re.search("(( )*[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)", text.text)
                if(match):
                    email2.append(match.group(0))
                else:
                    email2.append("Cannot get email")
            else:
                email2.append("Cannot get email")
        except Exception as e:
            print("Exception email2 : " + str(e))
            email2.append("Cannot get email")
        print("-----------------------------------------")
        #--------------Country and affiliation----------------------------------------------
        for each in affiliation:
            checkCountry(each,country)
        info = {
            "name" : name,
            "email" : email,
            "email2" : email2,
            "affiliation" : affiliation,
            "country" : country
        }
        authors.append(info)
    record = {
        "keyword" : kw,
        "link" : "https://onlinelibrary.wiley.com" + link,
        "title" : title,
        "journal" : journal,
        "vol" : vol,
        "date" : date,
        "doi" : "https://nph.onlinelibrary.wiley.com" + doi,
        "authors" : authors
    }
    pushRECORD(record,mycol)

#-------------------------------------------------Wiley------------------------------------------------------------------------------
def wiley(input,name,kw):
    mycol = connectDB()
    for i in range(0,999999):
        print("Page : " + str(i))
        stop = True
        try:
            headers = {
                'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}
            my_url = input + '&startPage=' + str(i)
            response = requests.get(my_url, headers=headers)
            page = soup(response.content, "html5lib")
            body = page.findAll("div",{"class":"item__body"})
            for each in body:
                link = each.h2.span.a['href']
                title = each.h2.text
                info = each.find("div",{"class":"meta__info"})
                date = info.find("span",{"class":"meta__epubDate"}).text
                doi = each.h2.span.a['href']
                #-------------------Initialization--------------------------------------------------------
                print("link : " + link)
                #--------------Title----------------------------------------------
                print("Title : " + title)
                #--------------Journal----------------------------------------------
                journal = info.find("a",{"class":"meta__serial"}).text
                print("Journal : " + journal)
                try:
                    vol = info.find("a",{"class":"meta__volume"}).text
                    print("Volume : " + vol)
                except Exception as e:
                    vol = "Cannot get volume"
                    print("Exception volume : " + str(e))
                #--------------Date----------------------------------------------
                try:
                    print("Date : " + date)
                except Exception as e:
                    print("Exception date : " + str(e))

                #--------------Doi----------------------------------------------
                try:
                    print("Doi : https://nph.onlinelibrary.wiley.com" + doi)
                except Exception as e:
                    print("Exception doi : " + str(e))

                #--------------Authors and email----------------------------------------------
                parse = "https://nph.onlinelibrary.wiley.com" + doi
                contact(parse,link,title,journal,vol,date,doi,mycol,kw)
                print("-------------------------------------------")
                stop = False
            if(stop):
                break
        except Exception as e:
                print("Exception big : " + str(e))
                print("Page : " + str(i))
                break
    print("Jimmy")

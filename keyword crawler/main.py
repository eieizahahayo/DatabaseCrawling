import bs4
import requests
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import datetime
from arxiv.arxiv import *
from scienceDirect.scienceDirect import *
from wiley.wiley import *
from springer.springer import *
from europePMC.europePMC import *
def craw(key,name,choice,first,last):
    print("start key", key)
    if(choice == "Wiley"):
        print("wiley key", key)
        wiley(key,name,first,last)
    elif(choice == "Springer"):
        print("springer key", key)
        springer(key,name,first,last)
    elif(choice == "Europe PMC"):
        print("pmc key", key)
        pmc(key,name,first,last)
    elif(choice == "Science Direct"):
        scienceDirect(key,name,first,last)
    elif(choice == "arXiv"):
        arXiv(key,name,first,last)

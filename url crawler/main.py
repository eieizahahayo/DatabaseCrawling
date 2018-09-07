import bs4
import requests
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import datetime
from wiley.wiley import *
from europePMC.europePMC import *
from scienceDirect.scienceDirect import *
from springer.springer import *

def craw(key,name,choice,first,last):
    print("start key", key)
    if(choice == "Wiley"):
        wiley(key,name,first,last)
    elif(choice == "Europe PMC"):
        pmc(key,name,first,last)
    elif(choice == "Science Direct"):
        scienceDirect(key,name,first,last)
    elif(choice == "Springer"):
        springer(key,name,first,last)

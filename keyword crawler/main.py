import bs4
import requests
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import datetime
from arxiv.arxiv import *
from acs.acs import *
from scienceDirect.scienceDirect import *
from wiley.wiley import *
from springer.springer import *
from sagepub.sagepub import *
from researchgate.researchgate import *
from europePMC.europePMC import *

def craw(key,name,choice):
    print("start key", key)
    if(choice == "Wiley"):
        print("wiley key", key)
        wiley(key,name)
    elif(choice == "Springer"):
        print("springer key", key)
        springer(key,name)
    elif(choice == "Europe PMC"):
        print("pmc key", key)
        pmc(key,name)
    elif(choice == "Science Direct"):
        scienceDirect(key,name)
    elif(choice == "arXiv"):
        arXiv(key,name)
    # elif(choice == "5"):
    #     key = input("Enter the keyword : ")
    #     name = input("Enter file name : ")
    #     sage(key,name)
    # elif(choice == "6"):
    #     key = input("Enter the keyword : ")
    #     name = input("Enter file name : ")
    #     gate(key,name)
    # elif(choice == "6"):
    #     key = input("Enter the keyword : ")
    #     name = input("Enter file name : ")
    #     acs(key,name)

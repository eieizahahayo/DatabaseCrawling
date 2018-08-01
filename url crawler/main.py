import bs4
import requests
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import datetime
from wiley.wiley import *
from europePMC.europePMC import *
from scienceDirect.scienceDirect import *

def craw(key,name,choice,first,last):
    print("start key", key)
    if(choice == "Wiley"):
        wiley(key,name,first,last)
    elif(choice == "Europe PMC"):
        pmc(key,name,first,last)
    elif(choice == "Science Direct"):
        scienceDirect(key,name,first,last)
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

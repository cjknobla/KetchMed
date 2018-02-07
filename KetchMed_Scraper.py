# -*- coding: utf-8 -*-
"""
Created on Tue Feb  6 11:12:02 2018

@author: cjknobla
"""

### Web Scraper for KetchMed Contact Information
### Prototype 1: Scrape home page for email addresses

# Import Beautiful Soup

from bs4 import BeautifulSoup
import requests
import re
import urllib
import csv
from urllib.error import URLError, HTTPError
from urllib.request import urlopen

#Import URL list
URL_list = []

with open('contact.csv') as csvDataFile:
    csvReader = csv.reader(csvDataFile)
    for row in csvReader:
        URL_list.append(row[0])

#Define URL

#URL_list = ["abhsgroup.com", "abhmaryland.com", "abhseattle.com"]
emailUniqueFull = []
ii = 0

for contactURL in URL_list:

    ##Code Block to navigate to "contact us" page
    '''
    #Get list of web-links from home page
    links = []
    r = requests.get("http://www." + URL)
    data = r.text
    soup = BeautifulSoup(data, "lxml")
    for link in soup.find_all("a"):
        links.append(link.get("href"))
      
    #remove "none" types    
    #del links[0]
    #del links[0]
    
    # Search for contact URL    
    r = re.compile(".*(contact-us).*")
    contact = [m.group(0) for l in links for m in [r.search(l)] if m]
    contactURL = contact[0]
    '''
    #find email addresses in contactURL
    try:
        f = urllib.request.urlopen("http://www." + contactURL)
    except (URLError, HTTPError):
        print(URL_list[ii] + ": Bad Gateway")
        ii+=1
    else:
        try:
            s = f.read().decode('utf-8')
        except:
            print(URL_list[ii] + ": Encoding Error")
            ii+=1
        else:
            emailList = re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[cngeo][oedr][mtvug]",s)
            
            #Remove Duplicate Email Addresses
            emailUnique = []
            for x in emailList:
                if x not in emailUnique:
                    emailUnique.append(x)
                    
            ##Append email list to full list
            emailUniqueFull.append([URL_list[ii], emailUnique])
            ii+=1
            
    #Clean up Results
output = "Unique_Emails.csv"
    
with open(output, "w") as output:
    writer = csv.writer(output, lineterminator = '\n')
    writer.writerows(emailUniqueFull)
            

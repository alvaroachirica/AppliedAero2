# -*- coding: utf-8 -*-
"""
Created on Fri Feb  4 20:53:19 2022

@author: alvaroms
"""

from bs4 import BeautifulSoup
import re
try:
    import urllib.request as urllib2
except ImportError:
    import urllib2

# Base filepath for the UIUC airfoil website (uged for accessing.dat files)
baseFlpth = "https://m-selig.ae.illinois.edu/ads/"

# Open the webpage and create the soup
html_page = urllib2.urlopen("https://m-selig.ae.illinois.edu/ads/coord_database.html")
soup = BeautifulSoup(html_page, 'lxml')

# Loop over al1 relevant file and gave each one
ind = 1
#links = []
for link in soup.find_all('a',attrs={'href': re.compile('\.dat', re.IGNORECASE)}):
    urllib2.urlretrieve(baseFlpth+link.get("href"),link.get("href").rsplit("/",1)[-1])
    print("Saving file %i" %ind)
    ind = ind + 1
import re
from bs4 import BeautifulSoup
import requests
import pandas as pd
import time
from selenium import webdriver



URL ='https://www.buybuybaby.com/store/giftregistry/registry_search_guest.jsp?_requestid=32292&pagFilterOpt=96&pagNum=1'

content = requests.get(URL).text

soup = BeautifulSoup(content, 'html.parser')

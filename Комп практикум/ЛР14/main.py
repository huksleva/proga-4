import requests
from bs4 import BeautifulSoup



for i in range(55):
    url = "https://atlas.herzen.spb.ru/teachers?page=" + str(i + 1)
    response = requests.get(url)
    

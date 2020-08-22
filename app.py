import webbrowser
import requests
from bs4 import BeautifulSoup
import os
import mysql.connector

config = {
   'user': 'root',
   'password': 'root',
   'host': '127.0.0.1',
   'database': 'rentalMadla',
   'port': '8889'
}

link = mysql.connector.connect(**config)

# print(link)

url = "https://www.finn.no/realestate/lettings/search.html?location=0.20012&location=1.20012.20196&location=2.20012.20196.20723&location=2.20012.20196.20724&stored-id=42739577&"

r = requests.get(url)
soup = BeautifulSoup(r.content, "html.parser")

# for annonse in (soup.select('article.ads__unit')):
#     for link in annonse.select('h2.ads__unit__content__title a[id]'):
#         print(link['id'])
#         print(link.text)



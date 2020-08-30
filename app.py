import webbrowser
import requests
from bs4 import BeautifulSoup
import os
import mysql.connector
from datetime import date

config = {
    'user': 'root',
    'password': 'root',
    'host': '127.0.0.1',
    'database': 'rentalMadla',
    'port': '8889'
}

db = mysql.connector.connect(**config)
cur = db.cursor(buffered=True)

# get adds from finn.no saved query
url = "https://www.finn.no/realestate/lettings/search.html?location=0.20012&location=1.20012.20196&location=2.20012.20196.20723&location=2.20012.20196.20724&stored-id=42739577&"

r = requests.get(url)
soup = BeautifulSoup(r.content, "html.parser")

rentals = []  # holds the data that we will return
sql = "SELECT id, adName, address, m2, price, finnId, rentalType, createdDate, closedDate, numberOfDaysAtFinn FROM " \
      "rentalMadla "
cur.execute(sql)
if cur.rowcount > 0:
    for (id, adName, address, m2, price, finnId, rentalType, createdDate, closedDate, numberOfDaysAtFinn) in cur:
        rentals.append({
            "id": id,
            "adName": adName,
            "address": address,
            "m2": m2,
            "price": price,
            "finnId": finnId,
            "rentalType": rentalType,
            "createdDate": createdDate,
            "closedDate": closedDate,
            "numberOfDaysAtFinn": numberOfDaysAtFinn
        })

for ads in (soup.select('article.ads__unit')):
   for ad in ads.select('div.ads__unit__content'):
      finnId = ad.select_one('h2.ads__unit__content__title a[id]')['id']
      print(ad.select_one('h2.ads__unit__content__title a[id]')['id'])  # finnId

      adName = ad.select_one('h2.ads__unit__content__title a[id]').text
      print(ad.select_one('h2.ads__unit__content__title a[id]').text)  # adName

      address = ad.select_one('div.ads__unit__content__details').text
      print(ad.select_one('div.ads__unit__content__details').text)  # address

      m2 = ad.select_one('div.ads__unit__content__keys div').text
      print(ad.select_one('div.ads__unit__content__keys div').text)  # m2

      price = ad.select('div.ads__unit__content__keys > div')[1].text
      print(ad.select('div.ads__unit__content__keys > div')[1].text)  # price

      rentalType = ad.select('div.ads__unit__content__list')[1].text
      print(ad.select('div.ads__unit__content__list')[1].text)  # rental type

      today = date.today()

      try:

          sql = "INSERT INTO rentalMadla " \
                "(adName, address, m2, price, finnId, rentalType, createdDate) " \
                "VALUES (%s, %s, %s, %s, %s, %s, %s)"
          cur.execute(sql, (adName, address, m2, price, finnId, rentalType, today))
          db.commit()
      finally:
          cur.close()

import bs4
import requests
import pandas as pd
import re


res = requests.get('http://www.sherdog.com/fighter/Dong-Hyun-Kim-16374')#connect to webpage


soup = bs4.BeautifulSoup(res.text, 'lxml')#convert res file to type beautifulsoup


v1 = soup.findAll('div',{'class':'fight_history'})# find everything within specified div

for i in v1:
    fight_history = i.text


print(fight_history)#print fight history of Dong-Hyun-Kim
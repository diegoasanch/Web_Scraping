from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

time1 = datetime.now()

titles = []
years = []
ratings = []

driver = webdriver.Chrome(r"C:\Apps\chromedriver_win32\chromedriver.exe")
driver.get(r"https://www.imdb.com/chart/top")
content = driver.page_source
soup = BeautifulSoup(content, features="html.parser")

for a in soup.findAll('td', attrs={'class':'titleColumn'}):
    text = [x.strip() for x in a.text.split('\n') if x!= '']
    titles.append(text[1])
    years.append(text[2])

for a in soup.findAll('td', attrs={'class':'ratingColumn imdbRating'}):
    rating = a.text.strip('\n')
    ratings.append(rating)

df = pd.DataFrame({'Movie title':titles,'Year':years,'Rating':ratings}) 
df.to_csv('movies.csv', index=False, encoding='utf-8')

driver.close()
time2 = datetime.now()
elapsed_time = (time2 - time1).total_seconds()
print(f"Runtime: {elapsed_time} seconds")
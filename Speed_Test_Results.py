from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

clean = lambda string: string.strip('\n').strip()

def soupGenerator(url, parser="html.parser", driver_path=r"C:\Apps\chromedriver_win32\chromedriver.exe"):
    driver = webdriver.Chrome(driver_path)
    driver.get(url)
    content = driver.page_source
    driver.close()
    return BeautifulSoup(content, parser)

def fillArray(array, soup):
    for a in soup.findAll('tr', attrs={'class':'data-result results'}):
        rank = a.find('td', attrs={'class': 'rank actual-rank'}).text
        country = a.find('td', attrs={'class': 'country'}).text
        speed = a.find('td', attrs={'class': 'speed'}).text
        array.append([int(clean(rank)), clean(country), float(clean(speed))])

def __main__():

    try:
        time1 = datetime.now()
        time = time1.strftime("%Y %b %d %H:%M:%S")
        url = r"https://www.speedtest.net/global-index"
        soup = soupGenerator(url)
        fixed = soup.find('div', attrs={"id": "column-fixed"})
        mobile = soup.find('div', attrs={"id": "column-mobile"})

        fixed_rankings = []
        fixed_sheet_name = 'Fixed Connection index'
        mobile_rankings = []
        mobile_sheet_name = 'Mobile Connection index'

        for array, soup in [[fixed_rankings, fixed],[mobile_rankings, mobile]]:
            fillArray(array, soup)

        with pd.ExcelWriter('speed_test.xlsx') as writer:

            df1 = pd.DataFrame(data=fixed_rankings, columns=['Rank','Country', 'Speed Mb/s'])
            df1.to_excel(writer, sheet_name=fixed_sheet_name, index=False, startrow=2, startcol=0)
            df2 = pd.DataFrame(data=mobile_rankings, columns=['Rank','Country', 'Speed Mb/s'])
            df2.to_excel(writer, sheet_name=mobile_sheet_name, index=False, startrow=2, startcol=0)
            
            ws = writer.sheets[fixed_sheet_name]
            ws.cell(row=1, column=1).value = 'Updated on: ' + time
            ws2 = writer.sheets[mobile_sheet_name]
            ws2.cell(row=1, column=1).value = 'Updated on: ' + time
        
        time2 = datetime.now()
        runtime = time2 - time1

        print('Runtime:', runtime)
    
    except:
        print('Error desconocido.')
        
if __name__ == "__main__":
    __main__()

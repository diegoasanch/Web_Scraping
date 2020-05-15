from selenium import webdriver
from bs4 import BeautifulSoup

def soupGenerator(url, parser="html.parser", driver_path=r"C:\Apps\chromedriver_win32\chromedriver.exe"):
    driver = webdriver.Chrome(driver_path)
    driver.get(url)
    content = driver.page_source
    driver.close()
    return BeautifulSoup(content, parser)
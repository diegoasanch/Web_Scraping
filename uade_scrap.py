# from scraping_tools import soupGenerator
from selenium import webdriver
import time

def login(url, usr, psw, driver_path=r"C:\Apps\chromedriver_win32\chromedriver.exe"):
    driver = webdriver.Chrome(driver_path)
    driver.get(url)
    driver.find_element_by_id('ctl00_ContentPlaceHolderMain_txtUser').send_keys(usr)
    driver.find_element_by_id('ctl00_ContentPlaceHolderMain_txtClave1').send_keys(psw)
    time.sleep(10)
    

def __main__():

    url = r'https://www.webcampus.uade.edu.ar/Login.aspx'

    with open('cre.txt', 'r') as creds:
        usr, psw = creds.readline().split(';')
    login(url, usr, psw)

if __name__ == "__main__":
    __main__()

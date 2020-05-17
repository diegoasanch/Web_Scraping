from bs4 import BeautifulSoup
from selenium import webdriver
from pandas import ExcelWriter, DataFrame
import time

def login(driver, url, usr, psw):

    driver.get(url)
    driver.find_element_by_id('ctl00_ContentPlaceHolderMain_txtUser').send_keys(usr)
    driver.find_element_by_id('ctl00_ContentPlaceHolderMain_txtClave1').send_keys(psw)
    driver.get(driver.current_url)

def logout(driver):

    driver.find_element_by_id('ctl00_Top1_lnkCerrarSesion').click()

def notesExtract(table):
    grades = []
    for grade in table.findAll('td', class_='td-texbox'):
        grades.append(grade.text)
    return grades
    
def classInfoExtract(driver, url):

    driver.get(url)
    soup = BeautifulSoup(driver.page_source, features="html.parser")
    time.sleep(1)
    
    classes = []
    grades_list = []

    period = soup.find('tr', class_='td-ADMdoc-REG').text
    
    for classroom in soup.findAll('tr', class_="td-AULA-bkg"):
        name = classroom.find('a').text
        
        grades_table = classroom.find('td', class_='tabla-ID2').findAll('tr')[1]
        grades= notesExtract(grades_table)

        classes.append(name)
        grades_list.append(grades)
    return classes, grades_list, period

def createExcel(class_matrix, header, file_name='Notas_UADE.xlsx'):

    with ExcelWriter(file_name, mode='w+') as writer:
        for row in class_matrix:
            class_info, grades, sheet, title = row 

            class_data = DataFrame(data=grades, index=class_info, columns=header)
            class_data.to_excel(writer, sheet_name=sheet, startrow=3)

            sheet = writer.sheets[sheet]
            sheet.cell(row=1, column=1).value = title
    writer.close()

def classMatrixCreate(driver, links):
    matrix = []
    for link in links:
        url = r'https://www.webcampus.uade.edu.ar/' + link
        clases, grades, period = classInfoExtract(driver, url)
        page_name = period.split('-')[1].strip()

        if 'Cuatrimestre' in page_name: page_name.replace('Cuatrimestre', 'Cuatr.')
        
        matrix.append([clases, grades, page_name, period])
    return matrix

def semestersExtract(driver):
    
    links = []
    soup = BeautifulSoup(driver.page_source, features="html.parser")

    for menu in soup.findAll('li', class_='rmItem'):
        if menu.text.split('\n')[0].lower() == 'mis cursos':
            for item in menu.findAll('li', class_="rsmItem"):
                item_name = item.text
                if 'cuatr' in item_name.lower() and item_name.endswith('Grado Monserrat'):
                    links.append(item.find('a')['href'])
    return links

def __main__():

    url = r'https://www.webcampus.uade.edu.ar/Login.aspx'
    driver_path = r"C:\Apps\chromedriver_win32\chromedriver.exe"
    driver = webdriver.Chrome(driver_path)

    with open('cre.txt', 'r') as creds:
        usr, psw = creds.readline().split(';')

    login(driver, url, usr, psw)

    links = semestersExtract(driver)
    class_matrix = classMatrixCreate(driver, links)
    header =  ['Parcial 1', 'Parcial 2', 'Recup', 'TP', 'Cursada', 'Examen Final', 'Condicion Final', 'Asistencia']
    createExcel(class_matrix, header)
    logout(driver)

if __name__ == "__main__":
    __main__()

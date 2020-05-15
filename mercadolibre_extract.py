# from scraping_tools import soupGenerator
from bs4 import BeautifulSoup
from selenium import webdriver
from pandas import ExcelWriter, DataFrame
from datetime import datetime
from time import sleep

def soupGenerator(url, parser="html.parser", driver_path=r"C:\Apps\chromedriver_win32\chromedriver.exe"):
    driver = webdriver.Chrome(driver_path)
    driver.get(url)
    content = driver.page_source
    driver.close()
    return BeautifulSoup(content, parser)

def get_time(time_format="%Y %b %d %H:%M:%S"):
    return datetime.now().strftime(time_format)

price_cell = lambda row: row[1]

def timer(func):
    'Prints function runtime'

    def wrapper():
        time1 = datetime.now()
        func()
        time2 = datetime.now()
        print(f'Runtime: {time2 - time1}')
        sleep(5)
        
    return wrapper

def item_class_finder(results_list):
    known_classes = [
        '<div class="rowItem item highlighted item--grid new"',
        '<div class="rowItem item product-item highlighted item--grid new with-reviews"',
        '<div class="rowItem item highlighted item--stack new"'
    ]
    for c in known_classes:
        if c in results_list:
            item_class = c[11:].strip('"')
            break
    else:
        item_class = None
    
    return item_class

def error_log(item, url, search_results, error):
    with open('mlScrapperErrorsLog.txt', mode='a+') as log:
        log.write(('-'*10) + f' log time {get_time()} ' + ('-'*10))
        log.write(f'\n\n"{error}" error occured while trying to scrap\n{url}\n\nSearched: "{item}"\n')
        if error == 'classError':
            log.write('\nThe item class could not be identified.\n\n - searchResults Class content:\n')
            log.write(search_results)
        log.write('\n\n' + ('-'*50) + '\n\n')


@timer
def __main__():

    try:
        error = ''

        to_search = input('Ingrese el articulo a buscar: ').lower()
        keywords = to_search.split()
        url = r"https://listado.mercadolibre.com.ar/" + f"{'-'.join(keywords)}#D[A:{'%20'.join(keywords)}]"
        excel_file_name = '_'.join(keywords) + '_ML.xlsx'

        if to_search == '':
            error = 'emptySearchError'
            print('No se ingreso ningun campo para la busqueda.')
            raise

        soup = soupGenerator(url)
        time = get_time()

        products = []
        titles = ['Nombre', 'Precio', 'Rating', 'Link', 'Reviews']
        search_name = to_search.title()
        sheet_n = f"{get_time('%b %d %H.%M')} search"

        results = str(soup.find(id='searchResults'))
        item_class = item_class_finder(results)

        if item_class == None:
            error = 'classError'
            print('No se pudo determinar la clase interna del grid de productos :(')
            error_log(to_search, url, results, error)
        else:

            for item in soup.findAll('div', class_=item_class):
                
                name = item.find('span', class_='main-title')
                
                price = list(map(int, item.find('span', class_='price__fraction').text.split('.')))
                
                if len(price) == 2:
                    price = (price[0]*1000) + price[1]
                elif len(price) == 1:
                    price = price[0]
                else:
                    price = 'N/A'
                
                rating = len(item.findAll('div', class_='star star-icon-full')) + .5 * len(item.findAll('div', class_='star star-icon-half'))
                reviews = item.find('div', class_='item__reviews-total')

                name = 'N/A' if name == None else name.text
                reviews = 'N/A' if reviews == None else int(reviews.text)
                
                link = item.find('a')['href']
                

            products.sort(key=price_cell)

            with ExcelWriter(excel_file_name, mode='a+') as writer:
                df1 = DataFrame(data=products, columns=titles)
                df1.to_excel(writer, sheet_name=sheet_n, index=False, startrow=3)
                
                sheet = writer.sheets[sheet_n]
                sheet.cell(row=1, column=1).value = f'Mercadolibre search: {search_name}'
                sheet.cell(row=2, column=1).value = 'Searched on: ' + time

            writer.close()
    except:
        if error == '': error = 'Unknown'
        print('An nexpected error occured :(')
        error_log(to_search, url, None, error)

if __name__ == "__main__":
    __main__()

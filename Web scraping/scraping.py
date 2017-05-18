# from collections import defaultdict
from bs4 import BeautifulSoup
import requests
# import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pyvirtualdisplay import Display
from pymongo import MongoClient
'''
Submitting form with selenium
'''
def start_Chrome():
    chrome_options = Options()
    chrome_options.add_argument('--dns-prefetch-disable')
    driver = webdriver.Chrome(chrome_options = chrome_options)
    return driver

def get_URL(driver, URL):
    driver.get(URL)
    fname = driver.find_element_by_id('firstNameReg_1')
    lname = driver.find_element_by_id('lastNameReg_1')

    return driver, fname, lname

def search_by_name(fname_value, lname_value, fname, lname, driver):
    '''
    INPUT:
    - fname_value, lname_value: values of first names (at least 1 character) and last names (at least 2 characters)
    - fname, lname: driver.find_element_by_id() object for elements first name and last name
    - driver: selenium webdriver object

    Steps:
    - Step 1: Perform searches using the combination of first names and last names
    - Step 2: Save the search result (html) file

    RETURN: html

    '''
    # Submit the 'Search' form
    fname.send_keys(fname_value)
    lname.send_keys(lname_value)
    driver.find_element_by_id('btnFindRegistry_1').click()

    #Filter '96' per page for faster scraping
    driver.find_element_by_id('pagFilterOpt').send_keys('96')

    # Get the page sourcecode
    html = driver.page_source
    return html

def next_page(driver):
    '''
    Clicking on 'Next Page' button if that exists
    '''
    driver.find_element_by_xpath("//a[@title='Next Page']").click()
    return driver


# def create_dict(fname_value, lname_value, html):
#     '''
#     INPUT: firstname, lastname
#     OUTPUT: dictionary {'firstname+lastname':[]}
#     '''
#     key = '{0}+{1}'.format(fname_value, lname_value)
#     html_dict = {key:[html]}
#     return html_dict

# def add_html_to_dict(fname_value, lname_value, html_dict, html):
#     key = '{0}+{1}'.format(fname_value, lname_value)
#     html_dict[key].append(html)
#     return html_dict
#
def add_html_to_db(fname_value, lname_value, html, table):
    search_combo = '{0}+{1}'.format(fname_value, lname_value)
    table.insert({'name':search_combo, 'html':html})
    return

# def save_search_results(filename, html_dict, mode='a'):
#     '''
#     mode: 'r', 'w', 'a'
#     ('a': appending)
#     '''

    # with open(filename, mode) as f:
    #     json.dump(html_dict, f)

def create_mongo_table(db_name, table_name):
    client = MongoClient()
    db = client[db_name]
    table = db[table_name]
    return table

def search_scraper(fname_list, lname_list, URL, table):
    driver = start_Chrome()
    driver, fname, lname = get_URL(driver, URL)
    # search_results = defaultdict()
    for f in fname_list:
        for l in lname_list:
            html = search_by_name(f, l, fname, lname, driver)
            add_html_to_db(f, l, html, table)

            # save_search_sourcecode(f,l, html)

            # select next page & save all pages
            while html.find('Next Page') > 0:
                driver = next_page(driver)
                # driver.find_element_by_xpath("//a[@title='Next Page']").click()
                html = driver.page_source
                add_html_to_db(f, l, html, table)

                # save_search_sourcecode(f, l, html)
            # table.insert(html_dict)
            # search_results.update(html_dict)
            # driver.close()
            driver, fname, lname = get_URL(driver, URL)
    return table

if __name__ == '__main__':

    fname_list = [ 'u', 'v', 'w', 'x', 'y', 'z']
    lname_list = ['sm', 'jo', 'wi', 'br', 'da', 'mi', 'mo', 'ta', 'an', 'th', 'ja', 'wh', 'ha', 'ma', 'ga', 'ro', 'cl', 'le', 'wa', 'al', 'yo', 'he', 'ki', 'wr', 'lo', 'hi', 'sc', 'gr', 'ad', 'ba', 'go', 'ne', 'ca']

    # first_test = ['a', 'b']
    # last_test = ['sm']

    display = Display(visible=0, size = (800,600))
    display.start()
    URL = 'https://www.buybuybaby.com/store/page/BabyRegistry'
    table = create_mongo_table('babyreg', 'searches_p2')
    table = search_scraper(fname_list, lname_list, URL, table)
    print 'Total number of pages: %' %table.count()
    # save_search_results('search_pages.json', search_results, 'w')

    driver.quit()
    display.stop()

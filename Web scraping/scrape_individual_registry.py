import re
from bs4 import BeautifulSoup
import requests
from selenium import webdriver

URL_registry_page = 'https://www.buybuybaby.com/store/giftregistry/view_registry_guest.jsp?pwsToken=&eventType=Baby&inventoryCallEnabled=true&registryId=543871988&pwsurl='
driver = webdriver.Chrome()
driver.get(URL_registry_page)

html = driver.page_source

soup = BeautifulSoup(html, 'html.parser')

def save_html(url, html):
    '''

    Saving all html source pages

    '''
    output = {url: html}

    with open('all_pages.json', 'w') as f:
        json.dump(output, f)

    return

def get_gender(soup):
    gender = soup.find('span', class_='getGender').text.split()
    return gender[-1]

def get_registry_id(soup):
    reg_id = soup.find('span', class_='registryId').text
    return reg_id

def get_event_date(soup):
    event_date = soup.find('span', class_='eventDate').text
    return event_date

def get_product_details(soup):
    '''
    Return: list of tuples.

    Each tuple contains:
    (product_name, product_sku, product_id, product_url)

    '''
    all_tags = soup.find_all('span', class_='blueName')
    product_list = []
    for tag in all_tags:
        product_name = tag.text
        # product_list.append(product_name)
        if tag.find('a'):
            product_sku = tag.a['data-skuid']
            product_id = tag.a['data-productid']
            product_url = tag.a['href']

        else:
            product_sku = ''
            product_id = ''
            product_url=''
        tup = (product_name, product_sku, product_id, product_url)
        product_list.append(tup)
    return product_list

def get_product_attributes(soup):

    '''
    Return: a list of tuples. Each tuple contains (color, size, UPC):
    - product color
    - product size
    - product UPC (unique product code)
    NOte: not all attributes are available for every product
    '''
    all_tags = soup.find_all('dl', class_='productAttributes')
    all_product_attributes = []
    for tag in all_tags:
        att_name = [t.text[:-1] for t in tag.find_all('dt')]
        att_list = [t.text for t in tag.find_all('dd')]

        color = att_list[att_name.index('COLOR')] if 'COLOR' in att_name else ''
        size = att_list[att_name.index('SIZE')] if 'SIZE' in att_name else ''
        UPC = att_list[att_name.index('UPC')] if 'UPC' in att_name else ''
        product_tup = (color, size, UPC)
        all_product_attributes.append(product_tup)

    return all_product_attributes


def get_price(soup):
    all_tags = soup.find_all('span', class_='columnHeader rlpPrice')
    price_list = []
    for tag in all_tags:
        price_list.append(tag.text[1:])
    return price_list

def get_request_quantity(soup):
    '''
    Return: Number of requested quantity for each item
    ex: 'Requested1'
    '''

    all_tags = soup.find_all('div', class_='requested')
    all_quantity = []
    for tag in all_tags:
        requested_count = tag.text.split('Requested')[-1]
        all_quantity.append(requested_count)
    return all_quantity

def save_image(soup):
    return

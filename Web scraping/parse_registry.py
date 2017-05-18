import re
import json
from bs4 import BeautifulSoup
import requests
from pymongo import MongoClient


def start_mongo(database, table):
    client = MongoClient()
    db = client[database]
    table = db[table]
    return db, table

def get_cursor(table, key):
    cursor = table.find({key:{'$exists':1}}, {'_id':0, 'link':0, 'state':0})
    return cursor

# def get_soups(table, key):
#     cursor = table.find({key:{'$exists':1}}, {'_id':0, 'link':0, 'state':0, 'id':0})
#     # htmls = table.distinct(key)
#     # cursor = table.find({key:{'$exists':1}}, {'_id':0, 'state':0, 'id':0})
#     soups = []
#     for doc in cursor:
#         for k, v in doc.iteritems():
#             soup = BeautifulSoup(v, 'html.parser')
#             soups.append(soup)
#     return soups

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
        product_name = tag.text.strip()
        # product_list.append(product_name)
        if tag.find('a'):
            product_sku = tag.a['data-skuid']
            #product_id = tag.a['data-productid']
            product_url = tag.a['href']

        else:
            product_sku = ''
            #product_id = ''
            product_url=''
        tup = (product_name, product_sku,
               #product_id,
               product_url)
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
        # UPC = att_list[att_name.index('UPC')] if 'UPC' in att_name else ''
        product_tup = (color, size, '') # removed 'UPC'
        all_product_attributes.append(product_tup)

    return all_product_attributes


def get_price(soup):
    all_tags = soup.find_all('span', class_='columnHeader rlpPrice')
    price_list = []
    for tag in all_tags:
        price_list.append(tag.text.strip()[1:])
    return price_list

def get_requested_quantity(soup):
    '''
    Return: Number of requested quantity for each item
    ex: 'Requested1'
    '''

    all_tags = soup.find_all('div', class_='requested')
    all_quantity = []
    for tag in all_tags:
        requested_count = tag.text.split()[-1]
        all_quantity.append(requested_count)
    return all_quantity

def get_purchased_quantity(soup):
    all_tags = soup.find_all('div', class_='purchase')
    all_quantity = []
    for tag in all_tags:
        purchased_count = tag.text.split()[-1]
        all_quantity.append(purchased_count)
    return all_quantity

def save_image(soup):

    return

def update_table(table, regid, product_details, product_att, price, re_quantity, purchased):

    for i in xrange(len(product_details)):
        table.update_one({'id':regid, 'product_details':product_details[i]},
                        {'$set': {'id':regid,
                        # 'gender': gender, 'event_date': event_date,
                        'product_details': product_details[i],
                        'product_att': product_att[i],
                        'price': price[i],
                        're_quantity': re_quantity[i],
                        'purchased': purchased[i]
                        }
                        }, upsert = True)

    return table

def parse_registry():
    db, table = start_mongo('babyreg', 'urls')
    # soups = get_soups(table, 'html')
    new_table = db['registries']
    regids_new_table = new_table.distinct('id')
    cursor = get_cursor(table, 'html')
    for doc in cursor:
        for k, v in doc.iteritems():
            html = doc['html']
            regid = doc['id']
            if regid in regids_new_table:
                pass
            else:
                soup = BeautifulSoup(html, 'html.parser')
                # import pdb; pdb.set_trace()
                # for soup in soups:
                try:
                    # gender = get_gender(soup)
                    # regid = get_registry_id(soup)
                    # event_date = get_event_date(soup)
                    product_details = get_product_details(soup)
                    product_att = get_product_attributes(soup)
                    price = get_price(soup)
                    re_quantity = get_requested_quantity(soup)
                    purchased = get_purchased_quantity(soup)
                    if len(product_details) == len(product_att) == len(price) == len(re_quantity) == len(purchased):
                        new_table = update_table(new_table, regid,
                                                #  gender, event_date,
                                                 product_details, product_att, price, re_quantity, purchased)
                except AttributeError:
                    pass

    return new_table

if __name__ == '__main__':
    table = parse_registry()
    # cursor = table.find()
    # df = pd.DataFrame(list(cursor))
    # df.to_csv('registries.csv')

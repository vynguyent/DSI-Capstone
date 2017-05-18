from pymongo import MongoClient
from bs4 import BeautifulSoup
import requests
import time
from post_requests import get_registry
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options

def start_mongo(database, table):
    client = MongoClient()
    db = client[database]
    table = db[table]
    return db, table

def get_search_results(table, key):
    cursor = table.find({key:{'$exists':1}}, {'_id':0, 'name':0})
    # htmls = table.distinct(key)
    links = []
    states = []
    ids = []
    for doc in cursor:
        for k, v in doc.iteritems():
        # for html in htmls:
            temp_state_id = []
            soup = BeautifulSoup(v, 'html.parser')
            link_tags = soup.find_all('div', class_='grid_2 alpha bold')
            state_id_tags = soup.find_all('div', class_='grid_1 alpha')
            for tag in link_tags:
                link = tag.find('a')['href']
                links.append(link)
            for tag in state_id_tags:
                temp_state_id.append(tag.text)
            for i in xrange(len(temp_state_id)):
                if i%2 == 0:
                    states.append(temp_state_id[i])
                else:
                    ids.append(temp_state_id[i])


    states = [s.split() for s in states][1:]
    ids = [i.split() for i in ids][1:]

    return links, states, ids

 def get_event_date(table1, table2, key):
     cursor = table1.find({key:{'$exists':1}}, {'_id':0, 'name':0})
     for doc in cursor:
         for k, html in doc.iteritems():
             soup = BeautifulSoup(html, 'html.parser')
             link_tags = soup.find_all('div', class_='grid_2 alpha bold')

             date_tags = soup.find_all('div', class_='grid_2 alpha')
             dates = filter(lambda x: (len(x)==0) or re.search(r'\/\d{4}$', x),  [i.text.strip() for i in date_tags])

             for link_tag, date in zip(link_tags, dates):
                 link = link_tag.find('a')['href']
                 table2.update_one({'link':link}, {'$set': {'event_date': date}}, upsert = True)
     return link, date

def update_table(database, table, links, states, ids):
    urls = database[table]

    for i in xrange(len(links)):
        urls.update_one({'link':links[i]}, {'$set': {'link':links[i], 'state': states[i], 'id': ids[i]}}, upsert = True)

    return urls

def get_id_and_event_date(url):
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'html.parser')
    regid = soup.find('span', class_='registryId').text
    event_date = soup.find('span', class_='eventDate').text
    return regid, event_date

# def start_Chrome():
#     chrome_options = Options()
#     chrome_options.add_argument('--dns-prefetch-disable')
#     driver = webdriver.Chrome(chrome_options = chrome_options)
#     driver.implicitly_wait(5)
#     return driver
#
# def get_URL(driver, URL):
#
#     driver.get(URL)
#     requested_ele = driver.find_element_by_class_name("requested")
#     html = driver.page_source
#
#     return html

def update_html_to_table(table, key):

    link_list = table.distinct(key)

    for link in link_list:
        URL = 'https://www.buybuybaby.com/store/giftregistry/'
        try:
            regid, event_date = get_id_and_event_date(URL+link)
            html = get_registry(regid, event_date)
            table.update_one({'link': link}, {'$set': {'html': html, 'event_date':event_date}}, upsert=True)
        except AttributeError:
            pass
        # time.sleep(3)
    return table

def parse_search_results():
    db, table = start_mongo('babyreg', 'urls') # Remember to change 'urls' to 'searches_p2' later
    # links, states, ids = get_search_results(table, 'html')
    # urls_table = update_table(db, 'urls', links, states, ids)
    urls_table = update_html_to_table(table, 'link') # Remember to change 'table' to 'urls_table' later
    return urls_table

if __name__ == '__main__':
    parse_search_results()

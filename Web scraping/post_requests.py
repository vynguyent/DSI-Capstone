from bs4 import BeautifulSoup
import requests

def get_registry(regid):
    url = 'https://www.buybuybaby.com/store/giftregistry/frags/registry_items_guest.jsp'


    # YOU NEED TO CONFIGURE THESE FOR EACH REQUEST
    # _registryId = regid
    # _eventDate = event_date


    my_headers = {
        'origin': 'https://www.buybuybaby.com',
        'referer': 'https://www.buybuybaby.com/store/giftregistry/view_registry_guest.jsp?pwsToken=&eventType=Baby&inventoryCallEnabled=true&registryId=_registryId&pwsurl=',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
        'x-requested-with' : 'XMLHttpRequest'
    }

    params = {
        'registryId':regid,
        'startIdx':0,
        'isGiftGiver':True,
        'blkSize':1000,
        'isAvailForWebPurchaseFlag':False,
        'userToken':'UT1021',
        'sortSeq':1,
        'view':1,
        'eventTypeCode':'BA1',
        'eventType':'BA1',
        'pwsurl':'',
        'totalToCopy':None,
        'eventDate':None,
        'isChecklistDisabled':False
    }

    html = requests.post(url,data=params,headers=my_headers).text
    return html

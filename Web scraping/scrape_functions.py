import re
from bs4 import BeautifulSoup
import requests


def get_recipe_id(soup):
    all_id_tags = soup.find_all(lambda tag: tag.name=='ar-save-item' and 'data-id' in tag.attrs)
    recipe_ids = [tag.attrs['data-id'] for tag in data_id_tags]
    return recipe_ids

def get_recipe_name(soup):
    return soup.find_all('h1')[0].text

def get_rating_reviews(soup):
    '''
    Returns:
    - Average rating
    - Total number of reviews

    '''
    rating = soup_temp.find('meta', itemprop = 'ratingValue')['content']
    review_count = soup_temp.find('meta', itemprop='reviewCount')['content']
    return rating,review_count

def get_made_count(soup):
    total_made_it = soup.find('div', class_='total-made-it')['data-ng-init']
    made_count = re.sub(r'\D',"",total_made_it)
    return made_count

def get_cook_url(soup):
    '''
    Return: cook's URL
    Example: /cook/mccormickspice/

    '''
    submitter_tags = soup.find_all('div', class_='submitter')
    for tag in submitter_tags:
    if tag.find('a'):
        cook_url = tag.find('a')['href']
    else:
        cook_url=''
    return cook_url

def get_cook_user_name(cook_url):
    return re.split('/')[2]

def get_intro(soup):
    '''
    Return: a short introduction of the recipe
    '''
    intro = soup.find('div', class_='submitter__description').text
    return intro


def get_ingredients(soup):
    ingredients_list = soup.find_all('span', itemprop = 'ingredients')

    return [ingredient.text for ingredient in ingredients_list]

def get_directions(soup):
    directions = test_soup.find_all('span', class_ = 'recipe-directions__list--item')
    for ele in directions:
        return ele.text

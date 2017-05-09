import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import time
from scrape_functions import *

URL = 'http://allrecipes.com/recipes/'

# num_pages = 100
# for page_num in xrange(2,num_pages+1):
    # next_URL = URL+'?page={}'.format(page_num)

content = requests.get(URL).text

soup = BeautifulSoup(content, 'html.parser')

# Getting the recipes' ids

recipe_ids = get_recipe_id(soup)
recipe_url = 'http://allrecipes.com/recipe/'

# Getting info from individual page for each recipe
recipe_names = []
recipe_rating = []
recipe_review_count = []
recipe_made_count = []
recipe_intro = []
recipe_directions = []
cook_url = []
cook_user_name = []


for rep_id in recipe_ids:
    recipe_url_temp = recipe_url + rep_id
    content_temp = requests.get(recipe_url_temp).text
    soup_temp = BeautifulSoup(content_temp, 'html.parser')

    #get recipe name
    recipe_name_temp = get_recipe_name(soup_temp)
    recipe_names.append(recipe_name_temp)

    # get recipe's ratings and review count
    rating_temp, review_count_temp = get_rating_reviews(soup_temp)
    recipe_rating.append(rating_temp)
    recipe_review_count.append(review_count_temp)

    # get recipe's total 'made' count
    made_count_temp = get_made_count(soup_temp)
    recipe_made_count.append(made_count_temp)

    # get recipe introduction
    recipe_intro_temp = get_intro(soup_temp)
    recipe_intro.append(recipe_intro_temp)

    # get recipe instructions
    recipe_directions_temp = get_directions(soup_temp)
    recipe_directions.append(recipe_directions_temp)

    # get ingredients
    recipe_ingredients_temp = get_ingredients(soup)
    recipe_ingredients.append(recipe_ingredients_temp)

    # get cook's URL, user name
    cook_url_temp = get_cook_url(soup_temp)
    cook_user_name_temp = get_cook_user_name(cook_url_temp)
    cook_user_name.append(cook_user_name_temp)

    # get dish image


    time.sleep(2) # sleep for 2 seconds

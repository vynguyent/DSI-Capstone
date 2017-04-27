# 1. Chef right: recipe recommender
## About
I'm hoping to build a recipe recommender system that could recommend recipes to users based on user similarity, item similarity, food trend and seasons

Users will first be shown a series of photos of dishes where they can swipe left or right if they do not like or like to dish. I will use that to recommend 10 dishes a day. And I'll send to users the dishes that they swiped right.

## Problem
To give users the recipes that are personalized, season-based and introduce them to latest food trend

## Presentation
I'm hoping to build a web app

## Data
I'm planing to scrape from the following sites. Although epicurious pictures are prettier, they lack reviews and users' comments. So I prefer to use allrecipes.
- Allrecipes.com
- Epicurious

Nonetheless, I found the following dataset that has been scraped and available.
- dataset: https://datahub.io/dataset/recipe-dataset

## Next step
Getting the data


# 2. Which start-up is the next Unicorn?: predicting start-up's fundraising activity

## About
Crunchbase is my go-to source when I want to check out any start-ups and I believe there is good information provided by the site such as the company's info, its social media, its latest news, its founders, its investors and particularly the amount of funding it has had.

So I'm hoping to build a model to predict whether a start-up will be able to raise funds (in other words, its potential), how long does it take the company to raise funds and potentially how much.

At a high level, companies in the trending/hot industries (e.g. Artificial Intelligence, Machine Learning, Chatbots, etc.) are more likely to raise funds than others. Or if the co-founders had successful track records, or the angel investors, which incubators they are part of, or which accelerator they went through, companies' social activities, etc.

For trending industries, I'm thinking of using stock markets data, twitter hashtags

## Users
Venture Capital, Private equity firms, angel investors

## Problem
Helping investors identify and shortlist potential companies to consider for investment in the ocean of hundreds of thousands startups.

Is there a formula of success? Can we use data to streamline and automate this process and allow machines to do the first cut?

## Presentation
I hope to create a web app to allow users to input a company URL on crunchbase and able to return my prediction. Or users can sign up to receive one company's recommendation per day

## Data
I'm planning to scrape primarily from Crunchbase, but I think I might get some great info from angelist and incubators' sites too.
- Crunchbase
- Angelist
- Incubators

Besides I'm planning to use Google Finance data to identify bullish/bearish industries, Twitter hashtags, and Techcrunch articles

- Google Finance
- Twitter
- Techcrunch

## Next step
Getting the data

# 3. Travel planner: Curate trips
## About
I'm thinking of using people's check-ins to identify their travel trails. And from there, I will create several trips for people who are planning to travel to consider.

## Problem
Many of us love to travel. We always have a constraint (budget, trip length, region, etc.). So this recommender can help people make a decision easier.

## Presentation
Web app

## Data
I'm thinking of using Foursquare data/API to get details about check-ins

## Next step
Getting the data

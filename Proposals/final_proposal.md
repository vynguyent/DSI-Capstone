# Why?
- Everyone's taste is different. Some people like salads, some people like savory food, some people like pastries, etc. But we when we browse for recipes, there are simply thousands out there that we don't know which one to choose from. That motivates me to build a recommender system to personalize the recipes that suit the user's preference.
- When choosing recipe, the first thing we look at is often not the long list of ingredients, nor the detailed instructions. The thing that appeals to us when choosing what recipes to cook is most of the time, the picture of the dish. When we think of a dish we love, we often remember how wonderful the dish looks and of course how tasty it is. Therefore, my recommender will show several photos of dishes for users to select as a way to collect their preference.
- I love cooking. But I always run out of ideas what to cook. I would go to allrecipes.com and oftentimes, I'm just too overwhelmed with what recipe to choose in the forest of millions of recipes. In the end, I just cook the same thing over and over! So I hope this project can help other cooks, like me, to have personalized recommendation for recipes.

# What?
I'm extracting information about the recipes (ingredients, instructions, cook time, cook method, number of ratings, number of reviews and number of times the recipe has been attempted) and the cooks (dishes they liked, made and the date they liked it and their location)

## Similarity filtering
From such information, I'm training a model to find similarity between dishes based on its ingredients and preparation instructions, potentially using ,dimensionality reduction for the instructions.

## Collaborative filtering
Then, I use the information about the cooks (which dishes they like, etc.) to train a Collaborative filtering model.

Then for each user, I'll display to them a sequence of photos of dishes for them to select (or swipe left and right if time permits) to use as input data for making recommendations.

If time permits, I can also include the weather API to incorporate how the weather will affect one's preference for different dishes. (using the date a user like a dish and and user's location)

## Regression/Classification
Potentially, I could also build a regression model to predict ratings of dishes and use that as input into the Collaborative filtering model


# Data
## Step 1: Collecting data to train the model
I'm scraping from allrecipes.com (refer to folder DSI Capstone/Web scraping)
About recipes:
- ingredients
- instructions
- cook time
- cook method
- number of ratings
- number of reviews
- number of times the recipe has been attempted

About cooks:
- dishes they liked
- dishes they made
- the date they liked it
- their location (city, state)
- comments

If time permits, I can incorporate weather API (refer to Collaborative filtering)

Potentially I could use comments to create content-boosted Collaborative filtering, but not all users give comments, or very few of them do I would expect. So it might not be feasible

## Step 2: Collecting data from a single user to make recommendations


# Presentation
-  A web app that takes input from users: they will select the dishes that appeal to them
- If time permits, make it a mobile-friendly version that allows users to swipe left or right

# Next step
- Scraping all the data

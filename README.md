# Expecting the unexpected
##Overview
I built a recommender to help young mothers create a baby product registry that is comprehensive and caters to their needs and preferences. My model learnt about user’s information and product’s information, identify users and products that are similar to each other. It then incorporated these explicit preferences and similarity into the user’s implicit preferences and item’s implicit similarity (from the items that users have already selected) to make a prediction about what are other products a user may like.

##Details
###Data Collection
I collected my own data by scraping over 100,000 registries from buybuybaby.com, one of the most popular website for baby products, with almost 30,000 products and close to 5 millions records. The data was scraped, parsed and stored in AWS and MongoDB. 

###Feature engineering and training the model
I used an ensemble model of content-boosted Matrix Factorization model and similarity-based collaborative filtering model to build my model. To deal with sparsity, I reduce my items space (products) by drop items that appear few than 50 times. Although that forgoes the “surprise” factor for users who have “eccentric” tastes that are unique, it helps make better prediction in general.

To improve the model, I also engineered new features for users (such as gender, quarter of the delivery date, regions) and items. I also used TF-IDF and Non-negative matrix factorization to identify the product category (latent features) and incorporated that into the item’s feature space. These data were then incorporated into the Matrix Factorization model to identify users and items that are similar not only implicitly but also explicitly.

As a last step, to achieve a comprehensive list of items in the recommended registry, I reweighed the recommendation results by choosing the items that are most different from each other and from those that have already been selected by users.

###Cross validation
I cross validated my models on a test set of users whose subset of items were kept in the training set. I used precision and recall as metrics and choose the model with the highest precision and recall.


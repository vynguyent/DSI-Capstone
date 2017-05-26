from users import Users
from registries import Registries
from recommender import Recommender

# Getting the data; Preprocessing the data; Engineering features
reg_filepath = '../Data/Scraped/allregistries.csv'
r = Registries(filepath)

r.preprocess_registries_data()
save_pickle(r, '../Data/Results/Registries.p')
r.create_registry_df()
r.registries.to_csv('../Data/Results/registries.csv')

r.create_items_df()
r.items.to_csv('../Data/Results/items.csv')

user_filepath = '../Data/Scraped/users.csv'
u = Users(user_filepath)
u.preprocess_users_data()

user_item_data = r.registries

# Splitting training and testing sets
train_data, test_data = r.train_test_split(test_proportion=0.2)

# Training the models
rec = Recommender()
rec.fit(train, user_data, item_data)

# Making recommendations
dist_mat = r.get_item_pairwise_dist()
recommendations = rec.recommend(test_data, dist_mat, num_items=100)

# Evaluating the model
rec.evaluate(test_data, cutoffs=[20, 30, 50])

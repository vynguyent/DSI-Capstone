'''
1. Get data
- get the data from mongodb, put it into dataframe

2. Collaborative Filtering: user-based
step 1:
- create a matrix of registry (user) - item, 1s for yes and 0s for no
- create a matrix of registry (user) - characteristics (state, date of the year, boy/girl)
- (can i use item similarity filtering? i.e. product color, size, description, rating, price)

step 2:
- Reduce dimensionality: SVD, NMF

step 3:
Compute similarity between users:
- Jaccard similarity (for boolean data: buy/not buy)
- Compute similarity matrix of pair-wise similarity between users

3. Model
- train the model
    + GraphLab: which model?
    + for cold-start problem: recommend most popular items for users to select
    + once user has made some selection, use CF user-based model

- make recommendation

'''

from pymongo import MongoClient
import re
import pandas as pd
import graphlab as gl
from sklearn.model_selection import train_test_split

# client = MongoClient()
# db = client['babyreg']
# cursor = db['registries'].find()
# cursor_states = db['urls'].find({},{'_id':0, 'link':0, 'html':0})
#
# registries = pd.DataFrame(list(cursor))
# states = pd.DataFrame(list(cursor_states))

def preprocess_registries_data(filename):

    df = pd.read_csv(filename)

    df['product_details'] = [x.strip('[]').split(',') for x in df['product_details']]
    df['product_att'] = [x.strip('[]').split(',') for x in df['product_att']]

    df['product_name'] = [p[0].strip('u\'').decode('unicode_escape').encode('ascii','ignore') for p in df.product_details]

    df['product_url'] = [x[-1].strip(' u\'') for x in df.product_details]
    df['product_id'] = [int(re.search(r'/(\d+)\?',x).group(1)) if x!='' else '' for x in df.product_url]
    df = df[df.product_id != ''] # convert to integer for graphlab models
    df['color'] = [x[0].strip(' u\'') for x in df.product_att]
    df['size_others'] = [x[1].strip(' u\'') for x in df.product_att]

    df['price'] = df.price.astype(float)
    df = df.drop(['_id','product_details', 'product_att'], axis=1)

    # Create registries dataframe
    registries = df[['id', 'product_id']]
    registries['requested'] = 1

    # Create items dataframe
    items = df[['product_id', 'color', 'size_others','price']]
    return df, registries, items


def preprocess_users_data(filename):
    users = pd.read_csv(filename)
    users['birth_month'] = [datetime.strptime(x, '%m/%d/%Y').month if type(x) is str else '' for x in users.event_date]
    users['birth_year'] = [datetime.strptime(x, '%m/%d/%Y').year if type(x) is str else '' for x in users.event_date]

    users = users.drop(['Unnamed: 0', 'link', 'event_date'], axis = 1)
    return users


def preprocess_for_graphlab(df):
    '''

    All columns need to be of the same type to be processed by GraphLab models

    '''
    for col in df.columns:
        df = df[df[col] !='']
        df[col] = [int(x) for x in df[col]]

    gl_df = gl.SFrame(df)
    return gl_df


# Splitting train and test set (How?)

# Train the model
# rec_base = gl.ranking_factorization_recommender.create(observation_data=registries_gl,
#                                                        user_id='id',
#                                                        item_id='product_id',
#                                                        target='requested',
#                                                        #user_data=users,
#                                                       # item_data=items,
#                                                        num_factors=5,
#                                                        ranking_regularization=0.3
#                                                        )

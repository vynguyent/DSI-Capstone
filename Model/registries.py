import pandas as pd
import re
import graphlab as gl
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF
from nltk.stem.wordnet import WordNetLemmatizer
from helper import *

class Registries(object):
    def __init__(self, filepath):
        self.filepath = filepath
        self.data = None

    def preprocess_registries_data(self):

        self.data = pd.read_csv(self.filepath)

        self.data['product_details'] = [x.strip('[]').split(',') for x in self.data['product_details']]
        self.data['product_att'] = [x.strip('[]').split(',') for x in self.data['product_att']]

        self.data['product_name'] = [p[0].strip('u\'').decode('unicode_escape').encode('ascii','ignore') for p in self.data.product_details]

        self.data['product_url'] = [x[-1].strip(' u\'') for x in self.data.product_details]
        self.data['product_id'] = [int(re.search(r'/(\d+)\?',x).group(1)) if x!='' else '' for x in self.data.product_url]
        self.data = self.data[self.data.product_id != ''] # convert to integer for graphlab models
        self.data['color'] = [x[0].strip(' u\'') for x in self.data.product_att]
        self.data['color_scheme'] = ['NEUTRAL' if type(x) is float else 'BLUE' if 'BLUE' in x.split() else 'PINK' if 'PINK' in x.split() else 'NEUTRAL' for x in self.data.color]
        self.data['size_others'] = [x[1].strip(' u\'') if type(x) is str else '' for x in self.data.product_att]

        # self.data['price'] = self.data.price.astype(float).fillna(0.0)
        self.data = self.data.drop(['product_details', 'product_att'], axis=1)

        return self.data

    def load_registry_data(self, data):
        self.data = data

    def create_registry_df(self):
        # Create registries dataframe
        self.registries = self.data[['id', 'product_id']]
        self.registries['requested'] = 1
        return self.registries

    def create_items_df(self):
        self.items = self.data[['product_id', 'product_name','color', 'color_scheme', 'size_others','price']]
        self.get_item_category_with_NMF()
        return self.items

    def tfidf_item_desc(self):
        self.items['desc'] = [x+' '+y for x, y in zip(self.items.product_name, self.items.size_others)]
        corpus = self.items['desc'].values
        wordnet = WordNetLemmatizer()
        docs_wordnet = [[wordnet.lemmatize(word) for word in re.split('\W+', words)] for words in corpus]
        stop_words = ['baby', 'child', 'infant', 'newborn', 'in', 'with', 'of', '+', '&', 'and', 'by']
        self.items.vectorizer = TfidfVectorizer(stop_words=stop_words)
        self.items.doc_term_mat = self.items.vectorizer.fit_transform(corpus)
        # feature_words = self.items.vectorizer.get_feature_names()
        return self.items.doc_term_mat

    def get_item_category_with_NMF(self, num_category=4):
        self.items.doc_term_mat = self.tfidf_item_desc()
        nmf = NMF(n_components=num_category)
        W_sklearn = nmf.fit_transform(self.items.doc_term_mat)
        H_sklearn = nmf.components_
        items_cat_ind = np.argsort(W_sklearn, axis=1)
        self.items['category'] = items_cat_ind[:,-1] # get the top category

        return self.items

    def get_item_pairwise_dist(self, metric='cosine'):
        tfidf_arr = self.items.doc_term_mat.toarray()
        dist_mat = pairwise_distances(tfidf_arr, metric)
        return dist_mat

    def dummify(df,column_name, drop_first = False):
        dummies = pd.get_dummies(df[column_name], prefix = column_name, drop_first = False)
        df = df.drop(column_name, axis = 1)
        return pd.concat([df,dummies], axis = 1)

    def to_SFrame(self, categorical_cols):
        '''
        categorical_cols: list of column names for categorical variables
        '''

        items_gl = self.items.dropna()
        reg_gl = self.registries.dropna()
        for col in categorical_cols:
            items_gl = dummify(items_gl, col)
        items_gl = gl.SFrame(items_gl)
        reg_gl = gl.SFrame(reg_gl)
        return reg_gl, items_gl

    def train_test_split(self, test_proportion = 0.2):
        reg_gl, _ = self.to_SFrame
        train, test = gl.recommender.util.random_split_by_user(dataset = reg_gl,
                                                              user_id = 'id',
                                                              item_id = 'product_id',
                                                              max_num_users = 1000,
                                                              item_test_proportion = 0.2,
                                                              random_seed = 100)

        return train, test

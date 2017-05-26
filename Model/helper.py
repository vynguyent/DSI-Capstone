import numpy as np
import pandas as pd
import cPickle as pickle



def save_pickle(matrix, filename):
    with open(filename, 'wb') as f:
        pickle.dump(matrix, f, pickle.HIGHEST_PROTOCOL)
def load_pickle(filename):
    with open(filename, 'rb') as f:
        matrix = pickle.load(f)
    return matrix

def dummify(df,column_name, drop_first = False):
    dummies = pd.get_dummies(df[column_name], prefix = column_name, drop_first = False)
    df = df.drop(column_name, axis = 1)
    return pd.concat([df,dummies], axis = 1)


def remove_outliers(df, column_names, std = 3):
    for col in column_names:
        df = df[(df[col].std() <= std)]
    return df

# Making plots
# Categorical variable plot, label is cateogrical
def cat_bar_plot(df, predictor_column, label_column):
    agg = df.groupby([predictor_column, label_column]).apply(len)
    agg = agg.unstack(level=label_column)
    agg.plot(kind='bar')

# Numberical variable plot, label is cateogrical
def num_kde_plot(df, predictor_column, label_column, title):
    df[df[label_column]==1][predictor_column].plot.kde(label = 1)
    df[df[label_column]==0][predictor_column].plot.kde(label = 0)
    plt.title(title)
    plt.legend()

def combine_df(df):
    df = preprocess_registries_data('registries_p1.csv')
    for i in xrange(2,9):
        df_temp  = preprocess_registries_data('registries_p{}.csv'.format(i))
        df = pd.concat([df, df_temp], axis = 0)
    return df

def get_item_details(df, item_df):
    columns = df.columns.tolist()
    columns.append(['product_name', 'color'])
    return df.merge(item_df, on='product_id', how='left')[columns]


from sklearn.metrics.pairwise import pairwise_distances

def get_min_within_dist_list(product_index_list, dist_mat):
    dist = []

    for i, x in enumerate(product_index_list):
        rest_of_pdts = product_index_list[:i] + product_index_list[i+1:]
        dist_min = np.min(dist_mat[x, rest_of_pdts])
        dist.append(dist_min)
    return dist

def get_min_cross_dist_list(product_id_list, product_index_list, dist_mat):
    cross_dist = []
    for i in product_id_list:
        cross_dist_min = np.min(dist_mat[i, product_index_list])
        cross_dist.append(cross_dist_min)
    return cross_dist

def get_most_different_items(min_dist_list, product_id_list, product_list, n_products):
    min_dist_ind = np.argsort(min_dist_list)
    most_diff_items_ind = min_dist_ind[-n_products:]
    most_diff_items = product_id_list.iloc[most_diff_items_ind]
    most_diff_items = product_list[product_list.product_id.isin(most_diff_items)][['product_id','product_name']]
    return most_diff_items

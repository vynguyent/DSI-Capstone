import pandas as pd
import graphlab as gl
from helper import *

class Recommender(object):
    def __init__(self):
        self.train = None
        self.user_data = None
        self.item_data = None
        self.MFmodel = None
        self.CFmodel = None

    def fit(self, user_item_data, user_data, item_data):
        self.train = user_item_data
        self.train.downweigh_rare_items()
        self.user_data = user_data
        self.item_data = item_data
        self.MFmodel = gl.ranking_factorization_recommender.create(observation_data=self.train,
                                                              user_id='id',
                                                              item_id='product_id',
                                                              target='requested',
                                                              user_data=user_data,
                                                              item_data=item_data,
                                                              num_factors=20,
                                                              binary_target=True,
                                                              ranking_regularization=0.3,
                                                              random_seed = 100)

        self.CFmodel = gl.item_similarity_recommender.create(observation_data=self.train,
                                                              user_id='id',
                                                              item_id='product_id',
                                                              target='requested',
                                                              user_data=user_data,
                                                              item_data=item_data,
                                                              num_factors=20,
                                                              binary_target=True,
                                                              ranking_regularization=0.3,
                                                              random_seed = 100
                                                               )
        return self.MFmodel , self.CFmodel

    def recommend(self, test_data, dist_mat, num_items=100):
        test_ids = test_data.to_dataframe()['id'].unique()
        recommendationsMF = self.MFmodel.recommend(test_ids, k=num_items).to_dataframe()
        recommendationsCF = self.CFmodel.recommend(test_ids, k=num_items).to_dataframe()
        recommendations = recommendationsMF.append(recommendationsCF)
        rec_data = recommendations.to_dataframe()
        final_recs = fine_tune_recommendations(rec_data, test_ids, self.item_data, dist_mat, num_items)
        final_recs = get_item_details(final_recs, self.item_data)

        return final_recs

    def evaluate(self, test_data, cutoffs):
        '''
        cutoffs: a list of k top items in the recommended results to compare between the test set and the recommended results
        '''
        evalMF = self.MFmodel.evaluate_precision_recall(test_data, cutoffs)
        evalCF = self.CFmodel.evaluate_precision_recall(test_data, cutoffs)
        return 'Matrix Factorization model results: \n', evalMF , 'Collaborative Filtering model results: \n', evalCF

    def fine_tune_recommendations(rec_data, test_ids, dist_mat, num_items=100):
        train_df = self.train.to_dataframe()
        final_rec = pd.DataFrame(columns=['id', 'product_id', 'product_name', 'color'])

        for id_ in user_ids:
            rec_items = rec_data[rec_data.id==id_]['product_id']
            rec_items_ind = self.item_data[self.item_data.product_id.isin(rec_items)].index.tolist()
            within_dist = get_min_within_dist_list(rec_items_ind, dist_mat)
            first_cut = get_most_different_items(within_dist, rec_items, self.item_data, num_items)
            first_cut_ind = first_cut.index.tolist()
            if id_ in train_df.id.values:
                train_pdts = train_df[train_df['id']==id_]['product_id']
                train_pdts_ind = item_data[item_data.product_id.isin(train_pdts)].index.tolist()
                cross_dist = get_min_cross_dist_list(first_cut_ind, train_pdts_ind, dist_mat)
                second_cut = get_most_different_products(cross_dist, first_cut['product_id'], item_data, num_items*0.5)
            else:
                second_cut = first_cut
            second_cut['id'] = [id_]*len(second_cut)
            final_rec = pd.concat((final_rec,second_cut), axis=0)
        final_rec[['id', 'product_id']] = final_rec[['id', 'product_id']].astype(int)
        return final_rec

    def downweigh_rare_items(self, item_count_threshold=20):
        '''
        For items that appears 20 (item_count_threshold) or fewer times, the model zeroized these items and assumed they were not included
        '''

        item_count = self.train.groupby('product_id', as_index=False)['requested'].count()
        item_count_subset = item_count[item_count.requested > item_count_threshold]
        item_count_subset = item_count_subset.rename(columns={'requested':'requested_above_threshold'})
        self.train = self.train.merge(item_count_subset, on = 'product_id', how='right')
        return self.train[['id', 'product_id', 'requested']]

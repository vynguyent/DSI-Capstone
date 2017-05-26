import pandas as pd
from helper import *
from datetime import datetime

class Users(object):
    def __init__(self, filepath):
        self.filepath = filepath

    def preprocess_users_data(self):
        self.data = pd.read_csv(self.filepath)
        self.data['birth_month'] = [datetime.strptime(x, '%m/%d/%Y').month if type(x) is str else '' for x in self.data.event_date]
        self.data['birth_year'] = [datetime.strptime(x, '%m/%d/%Y').year if type(x) is str else '' for x in self.data.event_date]
        self.data['quarter'] = ['spring' if (x>=1 and x<=3) else 'summer' if (x>3 and x<=6) else 'autumn' if (x>6 and x<=9) else 'winter' for x in self.data.birth_month]
        self.data['region'] = get_regions(self.data)
        self.data = self.data.drop(['link', 'event_date', 'birth_month', 'birth_year', 'state'], axis = 1)
        return self.data

    def get_regions(df):
        farwest = ['WA', 'OR', 'CA', 'NV']
        rocky = ['MT', 'ID', 'WY', 'UT', 'CO']
        southwest = ['AZ', 'NM', 'OK', 'TX']
        plains = ['ND', 'MN', 'SD', 'NE', 'IA', 'MO', 'KS']
        greatlakes = ['WI', 'IL', 'IN', 'OH', 'MI']
        eastcoast = ['ME', 'NH', 'VT', 'MA', 'RI', 'CT', 'NY', 'PA', 'NJ', 'DE', 'MD', 'DC']
        southeast = ['AR', 'LA', 'MS', 'AL', 'TN', 'KY', 'WV', 'VA', 'NC', 'SC', 'GA', 'FL']
        df['region'] = ['farwest' if x in farwest else 'rocky' if x in rocky else 'southwest' if x in southwest else 'plains' if x in plains else 'greatlakes' if x in greatlakes else 'eastcoast' if x in eastcoast else 'southeast' if x in southeast else 'others' for x in df.state]
        return df['region']

    def load_user_data(self, user_data):
        self.data = user_data

    def to_SFrame(self, categorical_cols):
        '''
        categorical_cols: list of column names for categorical variables
        '''

        df_gl = self.data.dropna()
        for col in categorical_cols:
            df_gl = dummify(df_gl, col)
        df_gl = gl.SFrame(df_gl)
        return df_gl

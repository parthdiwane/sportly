#!/usr/bin/env python
# coding: utf-8

# In[17]:


import pandas as pd
import os

curr_dir = os.getcwd()

parent_dir = os.path.dirname(curr_dir) # gtes the name of the parent directory

singles_net_stats_path = os.path.join(parent_dir, 'stats', 'singles_net_stats', 'singles_net_stats2.csv')
df = pd.read_csv(singles_net_stats_path)


# In[18]:


from sklearn.preprocessing import LabelEncoder
from collections import defaultdict


# In[19]:


# columns that need to be encoded
str_vals = ['tourney_name', 'surface','tourney_level','winner_hand','winner_ioc','loser_hand','loser_ioc','round','winner_name','loser_name','winner_entry','loser_entry']
# array of encoded label encoder objs
label_encoder_variables = []
for variable_name in str_vals:
    var_name = "nlabel_" + variable_name
    globals()[var_name] = LabelEncoder()
    label_encoder_variables.append(globals()[var_name])


# In[20]:


label_encoder_variables


# In[21]:


# 1
def encode():
    for i in range(len(str_vals)):
        if str_vals[i] in df.columns:
            encoded_number = label_encoder_variables[i].fit_transform(df[str_vals[i]]) # encodes each needed column --> type df
            df[str_vals[i] + "_n"] = encoded_number
    df.to_csv(singles_net_stats_path)


# In[22]:


encode()


# In[23]:


# 2
def build_player_name_map():
    player_name_map = defaultdict(int)

    winners = zip(df['winner_name'], df['winner_name_n'])
    losers = zip(df['loser_name'], df['loser_name_n'])

    for name, encoded in list(winners) + list(losers):
        player_name_map[name] = encoded

    return player_name_map


# In[24]:


# 3 
def drop_cols():
    # drop str value columns plus winner name and loser name
    global df
    for col in str_vals: 
        if col in df.columns:
            df = df.drop(str_vals,axis='columns')
            temp_cols = ['score','Unnamed: 0.1','Unnamed: 0']
            for temp_cols1 in temp_cols:
                if temp_cols1 in df.columns:
                    df = df.drop(['winner_rank','loser_rank','score','Unnamed: 0.1','Unnamed: 0'],axis='columns')


# In[26]:


# rank diff --> negative = loser rank points > winner rank points --> positive = winner rank points > loser rank points
df['rank_points_diff'] = df['winner_rank_points'] - df['loser_rank_points']
df


# In[27]:


from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import numpy as np
import warnings
import joblib
warnings.filterwarnings('ignore')


# In[29]:


y = df['winner_name_n']
X = []
for column_name in list(df.columns):
    if column_name != 'winner_name_n' and column_name != 'loser_name_n':
        X.append(column_name)
X = df[X]
X.drop(str_vals,axis='columns')


# In[30]:


# 4
def train_model():
    global X
    global y
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    random_forest_classifier = RandomForestClassifier(n_estimators=100,criterion='entropy',max_depth=13,n_jobs=1,random_state=42)
    random_forest_classifier.fit(X_train,y_train)
    joblib.dump(random_forest_classifier, 'rf_model.pkl')
    return random_forest_classifier


# In[ ]:


if __name__ == "__main__":
    train_model()


# In[ ]:





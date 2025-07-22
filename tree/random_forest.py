#!/usr/bin/env python
# coding: utf-8

# In[15]:


import pandas as pd 
import os

curr_dir = os.getcwd()

parent_dir = os.path.dirname(curr_dir) # gtes the name of the parent directory

singles_net_stats_path = os.path.join(parent_dir, 'stats', 'singles_net_stats', 'singles_net_stats.csv')
df = pd.read_csv(singles_net_stats_path)


# In[16]:


df.head()


# In[17]:


from sklearn.preprocessing import LabelEncoder
from collections import defaultdict


# In[18]:


str_vals = ['tourney_name', 'surface','tourney_level','winner_hand','winner_ioc','loser_hand','loser_ioc','round','winner_name','loser_name','winner_entry','loser_entry']
label_encoder_variables = []
player_name_map = defaultdict(int)
for variable_name in str_vals:
    var_name = "nlabel_" + variable_name
    globals()[var_name] = LabelEncoder()
    label_encoder_variables.append(globals()[var_name])


# In[19]:


for i in range(len(str_vals)):
    if str_vals[i] in df.columns:
        encoded_number = label_encoder_variables[i].fit_transform(df[str_vals[i]])
        df[str_vals[i] + "_n"] = encoded_number
        if str_vals[i] == 'winner_name' or str_vals[i] == 'loser_name':
            player_name_map.update(dict(zip(encoded_number, df[str_vals[i]]))) # pair encoder + winner_player_name


# In[20]:


# drop str value columns plus winner name and loser name
for col in str_vals: 
    if col in df.columns:
        df = df.drop(str_vals,axis='columns')
        temp_cols = ['winner_rank','loser_rank','score','Unnamed: 0.1','Unnamed: 0']
        for temp_cols1 in temp_cols:
            if temp_cols1 in df.columns:
                df = df.drop(['winner_rank','loser_rank','score','Unnamed: 0.1','Unnamed: 0'],axis='columns')
df.head()


# In[21]:


player_name_map


# In[22]:


# rank diff --> negative = loser rank points > winner rank points --> positive = winner rank points > loser rank points
df['rank_points_diff'] = df['winner_rank_points'] - df['loser_rank_points']
df


# In[23]:


from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import numpy as np
import warnings
import joblib
warnings.filterwarnings('ignore')


# In[24]:


df


# In[25]:


y = df['winner_name_n']
X = []
for column_name in list(df.columns):
    if column_name != 'winner_name_n' and column_name != 'loser_name_n':
        X.append(column_name)
X = df[X]
X


# In[26]:


def train_model():
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    random_forest_classifier = RandomForestClassifier(n_estimators=100,criterion='entropy',max_depth=13,n_jobs=1,random_state=42)
    random_forest_classifier.fit(X_train,y_train)
    joblib.dump(random_forest_classifier, 'rf_model.pkl')
    return random_forest_classifier


# In[ ]:


if __name__ == "__main__":
    train_model()


# In[ ]:


df.to_csv(singles_net_stats_path)


# In[ ]:





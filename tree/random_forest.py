#!/usr/bin/env python
# coding: utf-8

# In[42]:


import pandas as pd
import os

curr_dir = os.getcwd()

parent_dir = os.path.dirname(curr_dir) # gtes the name of the parent directory

singles_net_stats_path = os.path.join(parent_dir, 'stats', 'singles_net_stats', 'singles_net_stats2.csv')
df = pd.read_csv(singles_net_stats_path)


# In[43]:


from sklearn.preprocessing import LabelEncoder
from collections import defaultdict


# In[44]:


# columns that need to be encoded
str_vals = ['tourney_name', 'surface','tourney_level','winner_hand','winner_ioc','loser_hand','loser_ioc','round','winner_name','loser_name','winner_entry','loser_entry']
# array of encoded label encoder objs
label_encoder_variables = []
for variable_name in str_vals:
    var_name = "nlabel_" + variable_name
    globals()[var_name] = LabelEncoder()
    label_encoder_variables.append(globals()[var_name])


# In[45]:


label_encoder_variables


# In[46]:


# 1
def encode():
    for i in range(len(str_vals)):
        if str_vals[i] in df.columns:
            encoded_number = label_encoder_variables[i].fit_transform(df[str_vals[i]]) # encodes each needed column --> type df
            df[str_vals[i] + "_n"] = encoded_number
    df.to_csv(singles_net_stats_path)


# In[47]:


# 2
def build_player_name_map():
    player_name_map = defaultdict(int)

    winners = zip(df['winner_name'], df['winner_name_n'])
    losers = zip(df['loser_name'], df['loser_name_n'])

    for name, encoded in list(winners) + list(losers):
        player_name_map[name] = encoded

    return player_name_map


# In[48]:


encode()
build_player_name_map()


# In[49]:


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


# In[50]:


# rank diff --> negative = loser rank points > winner rank points --> positive = winner rank points > loser rank points
df['rank_points_diff'] = df['winner_rank_points'] - df['loser_rank_points']
df


# In[51]:


from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import numpy as np
import warnings
import joblib
warnings.filterwarnings('ignore')


# In[52]:


df = df.loc[:, ~df.columns.str.startswith('Unnamed')]
X = df.drop(columns=[*str_vals, 'winner_name_n', 'score', 'loser_name_n'], errors='ignore')
y = df['winner_p1']


# In[53]:


# 4
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
def train_model():
    global X
    global y
    random_forest_classifier = RandomForestClassifier(n_estimators=110,criterion='entropy',max_depth=15,n_jobs=1,random_state=42, oob_score=True)
    random_forest_classifier.fit(X_train,y_train)
    joblib.dump(random_forest_classifier, 'rf1_bin_model.pkl')

    return random_forest_classifier


# In[54]:


model = None
if __name__ == "__main__":
    encode()
    build_player_name_map()
    model = train_model()   
    oob_score = model.oob_score_
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)

    print(f'oob score {oob_score}')
    print(f'accuracy score {accuracy}') 


# In[55]:





# In[56]:


df


# In[ ]:





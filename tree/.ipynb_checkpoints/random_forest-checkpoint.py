#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd 

df = pd.read_csv('/Users/parth/coding/python/sportly/stats/tennis_atp/singles/atp_matches_net.csv')
df


# In[2]:


df.head()


# In[3]:


from sklearn.preprocessing import LabelEncoder
from collections import defaultdict


# In[4]:


str_vals = ['tourney_name', 'surface','tourney_level','winner_hand','winner_ioc','loser_hand','loser_ioc','round','winner_name','loser_name','winner_entry','loser_entry']
label_encoder_variables = []
player_name_map = defaultdict(int)
for variable_name in str_vals:
    var_name = "nlabel_" + variable_name
    globals()[var_name] = LabelEncoder()
    label_encoder_variables.append(globals()[var_name])


# In[5]:


for i in range(len(str_vals)):
    if str_vals[i] in df.columns:
        encoded_number = label_encoder_variables[i].fit_transform(df[str_vals[i]])
        df[str_vals[i] + "_n"] = encoded_number
        if str_vals[i] == 'winner_name' or str_vals[i] == 'loser_name':
            player_name_map.update(dict(zip(encoded_number, df[str_vals[i]]))) # pair encoder + winner_player_name


# In[6]:


# drop str value columns plus winner name and loser name
for col in str_vals: 
    if col in df.columns:
        df = df.drop(str_vals,axis='columns')
        temp_cols = ['winner_rank','loser_rank','score','Unnamed: 0.1','Unnamed: 0']
        for temp_cols1 in temp_cols:
            if temp_cols1 in df.columns:
                df = df.drop(['winner_rank','loser_rank','score','Unnamed: 0.1','Unnamed: 0'],axis='columns')
df.head()


# In[7]:


player_name_map


# In[8]:


# rank diff --> negative = loser rank points > winner rank points --> positive = winner rank points > loser rank points
df['rank_points_diff'] = df['winner_rank_points'] - df['loser_rank_points']
df


# In[9]:


from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import xgboost as xgb
import numpy as np
import warnings

warnings.filterwarnings('ignore')


# In[10]:


df


# In[11]:


y = df['winner_name_n']
X = []
for column_name in list(df.columns):
    if column_name != 'winner_name_n' and column_name != 'loser_name_n':
        X.append(column_name)
X = df[X]
X


# In[12]:


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
xgb_train = xgb.DMatrix(X_train, y_train, enable_categorical=True)
xgb_test = xgb.DMatrix(X_test, y_test, enable_categorical=True)


# In[20]:


random_forest_classifier = RandomForestClassifier(n_estimators=100,criterion='entropy',max_depth=12,n_jobs=1,random_state=42)


# In[21]:


X_train


# In[ ]:


random_forest_classifier.fit(X_train,y_train)


# In[16]:


y_pred_random_forest = random_forest_classifier.predict(X_test)


# In[17]:


y_pred_random_forest


# In[18]:


accuracy = accuracy_score(y_test, y_pred_random_forest)
classification_rep = classification_report(y_test,y_pred_random_forest)


# In[19]:


print('accuracy for random forest = ' + str(accuracy))
print('classification report' + str(classification_rep))
df.to_csv('/Users/parth/coding/python/sportly/stats/tennis_atp/singles/atp_matches_net.csv')


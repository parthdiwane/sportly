#!/usr/bin/env python
# coding: utf-8

# In[6]:


import pandas as pd 

df = pd.read_csv('/Users/parth/coding/python/sportly/stats/tennis_atp/singles/atp_matches_net.csv')
df


# In[7]:


df.head()


# In[8]:


from sklearn.preprocessing import LabelEncoder


# In[9]:


str_vals = ['tourney_name', 'surface','tourney_level','winner_hand','winner_ioc','loser_hand','loser_ioc','round','winner_name','loser_name','winner_entry','loser_entry']
label_encoder_variables = []
winner_name_map = {}
for variable_name in str_vals:
    var_name = "nlabel_" + variable_name
    globals()[var_name] = LabelEncoder()
    label_encoder_variables.append(globals()[var_name])


# In[10]:


for i in range(len(str_vals)):
    encoded_number = label_encoder_variables[i].fit_transform(df[str_vals[i]])
    df[str_vals[i] + "_n"] = encoded_number
    if str_vals[i] == 'winner_name' or str_vals[i] == 'loser_name':
        player_name_map = dict(zip(encoded_number, df[str_vals[i]])) # pair encoder + winner_player_name


# In[11]:


# drop str value columns plus winner name and loser name
df = df.drop(str_vals,axis='columns')
df = df.drop(['winner_rank','loser_rank','score','Unnamed: 0.1','Unnamed: 0'],axis='columns')
df.head()


# In[12]:


player_name_map


# In[13]:


# rank diff --> negative = loser rank points > winner rank points --> positive = winner rank points > loser rank points
df['rank_points_diff'] = df['winner_rank_points'] - df['loser_rank_points']
df


# In[14]:


from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import xgboost as xgb
import numpy as np
import warnings

warnings.filterwarnings('ignore')


# In[15]:


df
df.to_csv('/Users/parth/coding/python/sportly/stats/tennis_atp/singles/atp_matches_net.csv')


# In[16]:


y = df['winner_name_n']
X = []
for column_name in list(df.columns):
    if column_name != 'winner_name_n' and column_name != 'loser_name_n':
        X.append(column_name)
X = df[X]
X


# In[17]:


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
xgb_train = xgb.DMatrix(X_train, y_train, enable_categorical=True)
xgb_test = xgb.DMatrix(X_test, y_test, enable_categorical=True)


# In[18]:


random_forest_classifier = RandomForestClassifier(n_estimators=105,criterion='entropy',max_depth=12,n_jobs=1,random_state=42)


# In[19]:


X_train


# In[20]:


random_forest_classifier.fit(X_train,y_train)


# In[21]:


y_pred_random_forest = random_forest_classifier.predict(X_test)


# In[22]:


y_pred_random_forest


# In[23]:


accuracy = accuracy_score(y_test, y_pred_random_forest)
classification_rep = classification_report(y_test,y_pred_random_forest)


# In[24]:


print('accuracy for random forest = ' + str(accuracy))
print('classification report' + str(classification_rep))


import numpy as np
import pandas as pd 
from get_matches import *
import os 
from huggingface_hub import hf_hub_download
import joblib 

# for reading csv file
os.chdir('../')
os.chdir(os.getcwd() + '/stats/singles_net_stats')
csv_path = os.getcwd() + '/singles_net_stats.csv'


df = pd.read_csv(csv_path)

# back to cwd
for i in range(2):
    os.chdir('../')
os.chdir(os.getcwd() + '/scripts_main')

model_path = hf_hub_download(
    repo_id='parthdiwane/sportly-random-forest',
    filename='rf_model.pkl'
)

model = joblib.load(model_path)

def find_winner(p1: str, p2: str):
    arr = find_matches(p1,p2)
    df1, df2 = arr[0], arr[1]

    df1 = df1[model.feature_names_in_].fillna(0)
    df2 = df2[model.feature_names_in_].fillna(0)


    trained_feature_names = model.feature_names_in_
    print(df2[trained_feature_names].T)

    probability_p1 = model.predict_proba(df1[trained_feature_names])[0][1]
    probability_p2 = model.predict_proba(df2[trained_feature_names])[0][1]


    if probability_p1 > probability_p2:
        print(p1 + ": " + str(probability_p1))
    else:
        print(p2 + ": " + str(probability_p2))

find_winner('Roger Federer', 'Carlos Alcaraz')

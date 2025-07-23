import numpy as np
import pandas as pd 
from get_matches import find_matches
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
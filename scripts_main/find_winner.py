import numpy as np
import pandas as pd 
import os 
from huggingface_hub import hf_hub_download
import joblib 
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tree.random_forest import build_player_name_map


# for reading csv file
os.chdir('../')
os.chdir(os.getcwd() + '/stats/singles_net_stats')
csv_path = os.getcwd() + '/singles_net_stats2.csv'


df = pd.read_csv(csv_path)

# back to cwd
for i in range(2):
    os.chdir('../')
os.chdir(os.getcwd() + '/scripts_main')

model_path = hf_hub_download(
    repo_id='parthdiwane/sportly-random-forest',
    filename='rf_bin_model.pkl'
)

model = joblib.load(model_path)

def find_winner(p1: str, p2: str):
    trained_feature_names = model.feature_names_in_
    player_name_map = build_player_name_map()
    num_p1, num_p2 = player_name_map[p1], player_name_map[p2]


    print(df1)
   

find_winner('Carlos Costa', 'Thomas Muster')

import pandas as pd
import numpy as np
import joblib
import sys
import os 

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tree.random_forest import player_name_map

# load model
os.chdir('../')
os.chdir(os.getcwd() + '/tree')
model_path = os.getcwd()
model = joblib.load(model_path +'/' + 'rf_model.pkl')

# for loading df
os.chdir('../')
os.chdir(os.getcwd() + '/stats/singles_net_stats')

# read net csv file 
df = pd.read_csv(os.getcwd() + '/singles_net_stats.csv')

# cd back into proper dir
os.chdir('../')
os.chdir('../')
os.chdir(os.getcwd() + '/scripts_main')


# def find_matches(player1: str, player2: str):
#     p1 = player_name_map(player1)
#     p2 = player_name_map(player2)
    
#     player1_stats = df[(df['winner_name_n'] == p1) | (df['loser_name_n'] == p1)]
#     player2_stats = df[(df['winner_name_n'] == p2) | (df['loser_name_n'] == p2)]
    
#     head_to_head = df[
#         ((df['winner_name_n'] == p1) & (df['loser_name_n'] == p2)) |
#         ((df['winner_name_n'] == p2) & (df['loser_name_n'] == p1))
#     ]
    
#     return head_to_head

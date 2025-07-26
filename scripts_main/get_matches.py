import pandas as pd
import numpy as np
import joblib

import sys
import os 

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tree.random_forest import player_name_map

def find_matches(player1: str, player2: str):
    p1 = player_name_map[player1]
    p2 = player_name_map[player2]
    
    os.chdir('../')
    os.chdir(os.getcwd() + '/stats/singles_net_stats')
    singles_net_stats_path = os.getcwd() + '/singles_net_stats.csv'
    for i in range(2):
        os.chdir('../')
    os.chdir(os.getcwd() + '/scripts_main')

    df_net = pd.read_csv(singles_net_stats_path)
    df_player1 = pd.DataFrame()
    df_player2 = pd.DataFrame()

    player1_stats = df_player1[(df_net['winner_name_n'] == p1) | (df_net['loser_name_n'] == p1)]
    player2_stats = df_player2[(df_net['winner_name_n'] == p2) | (df_net['loser_name_n'] == p2)]
    
    
    
    return [df_player1,df_player2]


print(find_matches('Roger Federer', 'Carlos Alcaraz'))
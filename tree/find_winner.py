from random_forest_decision_tree import player_name_map
import pandas as pd
import numpy as np 

df = pd.read_csv('/Users/parth/coding/python/sportly/stats/tennis_atp/singles/atp_matches_net.csv')

def find_matches(player1: str, player2: str):
    p1 = player_name_map(player1)
    p2 = player_name_map(player2)
    
    player1_stats = df[(df['winner_name_n'] == p1) | (df['loser_name_n'] == p1)]
    player2_stats = df[(df['winner_name_n'] == p2) | (df['loser_name_n'] == p2)]
    
    head_to_head = df[
        ((df['winner_name_n'] == p1) & (df['loser_name_n'] == p2)) |
        ((df['winner_name_n'] == p2) & (df['loser_name_n'] == p1))
    ]
    
    return head_to_head

matches = find_matches('Roger Federer', 'Carlos Alcaraz')
print(matches)
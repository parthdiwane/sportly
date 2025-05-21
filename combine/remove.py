import pandas as pd

df = pd.read_csv('/Users/parth/coding/python/sportly/stats/tennis_atp/singles/atp_matches_net.csv')
 
df = df.drop(columns=['tourney_id','tourney_date','winner_id','loser_id','tourney_date','match_num'])
df.to_csv('/Users/parth/coding/python/sportly/stats/tennis_atp/singles/atp_matches_net.csv')
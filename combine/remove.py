# reminder : change ts to local not abs path 
import pandas as pd

df = pd.read_csv('/Users/parth/coding/sportly/stats/singles_net_stats/singles_net_stats2.csv') # net csv file for singles (no doubles files yet)
 
df = df.drop(columns=['tourney_id','tourney_date','winner_id','loser_id','tourney_date','match_num']) # get rid of unnecessary columns in df
df.to_csv('/Users/parth/coding/sportly/stats/singles_net_stats/singles_net_stats2.csv')
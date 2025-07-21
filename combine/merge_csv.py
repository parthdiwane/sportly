import pandas as pd

merge = pd.DataFrame()
for i in range(57):
    df = pd.read_csv('stats/tennis_atp/atp_matches_'+ str(1968 + i) + '.csv')
    
    merge = pd.concat([merge,df], ignore_index=True) # combines independent csv files into one data frame

merge.to_csv('/Users/parth/coding/sportly/stats/singles_net_stats/singles_net_stats.csv') # converts data frame into csv file for later use
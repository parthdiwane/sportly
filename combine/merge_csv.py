import pandas as pd

merge = pd.DataFrame()
for i in range(57):
    df = pd.read_csv('stats/tennis_atp-master_'+ str(1968 + i) + '.csv')
    
    merge = pd.concat([merge,df], ignore_index=True) # combines independent csv files into one data frame

merge.to_csv('/Users/parth/coding/python/sportly/stats/tennis_atp/singles/atp_matches_net.csv') # converts data frame into csv file for later use
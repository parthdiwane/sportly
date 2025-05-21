import pandas as pd

merge = pd.DataFrame()
for i in range(57):
    df = pd.read_csv('/Users/parth/coding/python/sportly/stats/tennis_atp/singles/atp_matches_'+ str(1968 + i) + '.csv')
    
    merge = pd.concat([merge,df], ignore_index=True)

merge.to_csv('/Users/parth/coding/python/sportly/stats/tennis_atp/singles/atp_matches_net.csv')

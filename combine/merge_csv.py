import pandas as pd

merge = pd.DataFrame()
for i in range(55):
    df = pd.read_csv('stats/tennis_atp/singles/atp_matches_'+ str(1968 + i) + '.csv')
    
    merge = pd.concat([merge,df], ignore_index=True)

merge.to_csv('stats/tennis_atp/singles/atp_matches_net.csv')

import os
import pandas as pd
os.chdir('../')
os.chdir(os.getcwd() + '/stats/singles_net_stats')
csv_path = os.getcwd() + '/singles_net_stats.csv'

os.chdir('../')
os.chdir('../')
os.chdir(os.getcwd() + '/scripts_main')

df = pd.read_csv(csv_path)
df = df.iloc[:,32:]
df.to_csv(csv_path)
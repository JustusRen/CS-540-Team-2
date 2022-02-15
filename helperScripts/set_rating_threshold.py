import pandas as pd
import os
import random

os.chdir('/Users/yui/Documents/SQL/ml-25m/')
df = pd.read_csv('ratings.csv')
df = df.drop(columns = ['timestamp'])

def categorise(row):
    if row['rating'] >= 3.5:
        return 1
    else:
        return 0

df['rating_binary'] = df.apply(lambda row:categorise(row), axis=1)

df.to_csv('rating.csv')
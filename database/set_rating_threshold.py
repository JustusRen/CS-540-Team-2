import pandas as pd
import os
import random

df = pd.read_csv('movieLens/raw/ratings.csv')
df = df.drop(columns = ['timestamp'])

def categorise(row):
    if row['rating'] >= 3.5:
        return 1
    else:
        return 0

df['rating_binary'] = df.apply(lambda row:categorise(row), axis=1)

df.to_csv('movieLens/processed/rating.csv')
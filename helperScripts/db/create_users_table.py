#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 10 20:50:24 2022

@author: bing
"""

import pandas as pd
import os
import random

df = pd.read_csv('movielens_data/ratings.csv')
df = df.drop_duplicates(subset = ['userId'])
df = df.drop(columns = ['movieId', 'rating', 'timestamp'])

usernames = []
for i in range(len(df)):
    names = 'user'+ str(i+1)
    usernames.append(names)
    
emails = []
for i in range(len(df)):
    mails = 'user'+ str(i+1) +'@buddies.com'
    emails.append(mails)
    
password = []
for i in range(len(df)):
    passw = 'password'+ str(i+1) 
    password.append(passw)
  
age = []
for i in range(len(df)):
    n = random.randint(18,50)
    age.append(n)

df['user_name'] = usernames
df['email'] = emails
df['password'] = password
df['age'] = age

df.to_csv('users.csv')
import mysql.connector
import os 
from . import sql_statements
import pandas as pd
from pandas.io import sql
import config
from sqlalchemy import create_engine
import time
import sys
import warnings

import pandas as pd 
from surprise import SVD
from surprise import Dataset
from surprise.model_selection import cross_validate
from collections import defaultdict
from surprise import Reader
from sqlalchemy import create_engine, update

from sqlalchemy.sql import select

class Database:
  def __init__(self, host, user, pwd):
    self.host = host
    self.user = user
    self.pwd = pwd

  def check_db_connection(self):
    try:
      mydb = mysql.connector.connect(
        host=self.host,
        user=self.user,
        password=self.pwd
      )
      print('SUCCESS: Database connection successful.')
    except:
      print('ERROR: Could not connect to database.')

  def create_db(self):
    try:
      mydb = mysql.connector.connect(
          host=self.host,
          user=self.user,
          password=self.pwd
        )
      cursor = mydb.cursor()
      cursor.execute(sql_statements.CREATE_DB)
      print('SUCCESS: Created database if it did not exist.')
    except:
      print('ERROR: Could not create or find database.')


  def create_tables(self):
    try:
      mydb = mysql.connector.connect(
          host=self.host,
          user=self.user,
          password=self.pwd
        )
      cursor = mydb.cursor()
      cursor.execute(
        sql_statements.USE_DB
      + sql_statements.CREATE_USER_TABLE
      + sql_statements.CREATE_MOVIE_TABLE
      + sql_statements.CREATE_GENRE_TABLE
      + sql_statements.CREATE_GENRE_RELATIONSHIP_TABLE
      + sql_statements.CREATE_RATING_TABLE
      + sql_statements.CREATE_RECOMMENDATION_TABLE 
      ) 
      print('SUCCESS: Create tables.')
    except:
      print('ERROR: Could not create table.')

  def insert_user_data(self, engine):
    df = pd.read_csv ('database/movieLens/processed/users.csv')
    df = df.drop(df.columns[0], axis=1)
    df.rename(columns = {'userId':'id', 'user_name':'first_name'}, inplace = True)
    time.sleep(0.1)
    try:
      df.to_sql('user', con=engine, if_exists='append', index= False)
      print("SUCCESS: User data inserted.")
    except: 
      print("WARNING: User data already exists")


  def insert_genre_data(self, engine):
    df = pd.read_csv('database/movieLens/processed/genre.csv')
    df.rename(columns = {'genre_id':'id'}, inplace = True)
    time.sleep(0.1)
    try:
      df.to_sql('genre', con=engine, if_exists='append', index=False)
      print("SUCCESS: Genre data inserted.")
    except:
      print("WARNING: Genre data already exists.")  
    
  def insert_movie_data(self, engine):   
    df = pd.read_csv("database/movieLens/raw/movies.csv")
    df = df.drop(df.columns[2], axis=1)
    df.rename(columns = {'movieId':'id'}, inplace = True)

    time.sleep(0.1)

    try:
      df.to_sql('movie', con=engine, if_exists='append', index=False)
      print("SUCCESS: Movie data inserted.")
    except: 
      print("WARNING: Movie data already exists.")

  def insert_movie_genre_relations(self, engine):

    if not sys.warnoptions:
      warnings.simplefilter("ignore")
    
    genre_relation_df = pd.read_csv("database/movieLens/raw/movies.csv")
    
    df = pd.DataFrame()
    id = 1
    # iterate through each dataframe
    for index, row in genre_relation_df.head(10).iterrows():
        #get each movie's genres, split by "|" and save in a list
        genres = genre_relation_df.iloc[[index]]['genres'].str.split('|').tolist() #[['Adventure', 'Animation', 'Children']]
        #covert a list of list to one list
        genres = [*genres[0]] #['Adventure', 'Animation', 'Children']
        #iterate through the genres list in that column
        for genre in genres:
          #insert into mysql
          #print(genre_relation_df.iloc[[index]]['movieId'].tolist()[0], genre)
          movie_id = genre_relation_df.iloc[[index]]['movieId'].tolist()[0]
          df_row = pd.DataFrame({ 'movie_id' : [movie_id], 'genre_id' : [genre], 'id' : [id] })
          df = df.append(df_row)
          id += 1

    cols = df.columns.tolist()
    cols = cols[-1:] + cols[:-1]
    df = df[cols]
    df = df.replace('Action', 1)
    df = df.replace('Adventure', 2)
    df = df.replace('Animation', 3)
    df = df.replace("Children", 4)
    df = df.replace('Comedy', 5)
    df = df.replace('Crime', 6)
    df = df.replace('Documentary', 7)
    df = df.replace('Drama', 8)
    df = df.replace('Fantasy', 9)
    df = df.replace('Film-Noir', 10)
    df = df.replace('Horror', 11)
    df = df.replace('Musical', 12)
    df = df.replace('Mystery', 13)
    df = df.replace('Romance', 14)
    df = df.replace('Sci-Fi', 15)
    df = df.replace('Thriller', 16)
    df = df.replace('War', 17)
    df = df.replace('Western', 18)
    df = df.replace('NoGenresListed', 19)

    time.sleep(0.1)
    df.to_sql('genre_relationship', con=engine, if_exists='append', index=False)

    try:
      print("SUCCESS: Genre_relationship data inserted.")
    except: 
      print("WARNING: Genre_relationship data already exists.")

  def insert_rating_data(self, engine):
    df = pd.read_csv ('database/movieLens/processed/rating.csv')
    df = df.drop(df.columns[0], axis=1)
    df = df.drop(df.columns[3], axis=1)
    df.rename(columns = {'userId':'user_id', 'movieId':'movie_id'}, inplace = True)
    df['id'] = df.index+1
    cols = df.columns.tolist()
    cols = cols[-1:] + cols[:-1]
    df = df[cols]
    time.sleep(0.1)
    try:
      df.to_sql('rating', con=engine, if_exists='append', index = False)
      print("SUCCESS: Rating data inserted.")
    except:
      print("WARNING: Rating data already exists.")

  def get_table(self, engine, table):
    query = 'SELECT * FROM ' + table
    data = pd.read_sql(query, engine)
    return data
  
  def drop_table(self, table):
    mydb = mysql.connector.connect(
        host=self.host,
        user=self.user,
        password=self.pwd
      )
    cursor = mydb.cursor()
    cursor.execute(
      "USE movie_buddy; DROP TABLE " + table, multi=True 
     
    ) 

  def top_n_to_db(self, engine):

    def get_top_n(predictions, n=10):
      top_n = defaultdict(list)
      for uid, iid, true_r, est, _ in predictions:
          top_n[uid].append((iid, est))

      for uid, user_ratings in top_n.items():
          user_ratings.sort(key=lambda x: x[1], reverse=True)
          top_n[uid] = user_ratings[:n]
      return top_n
    
    df_rec = pd.DataFrame()
    id = 1
    df_ratings = self.get_table(engine, "rating")

    reader = Reader(rating_scale=(1, 5.0))
    data = Dataset.load_from_df(df_ratings[['user_id', 'movie_id', 'rating']], reader)
    algo = SVD()

    trainset = data.build_full_trainset()
    algo.fit(trainset)
    users = list(set(df_ratings['user_id'].tolist()))
    for user_id in users:
      df_ratings_test = df_ratings[df_ratings['user_id'] == user_id]

      test = Dataset.load_from_df(df_ratings_test[['user_id', 'movie_id', 'rating']], reader)
      testset1 = test.build_full_trainset()
      testset = testset1.build_testset()

      predictions = algo.test(testset)

      top_n = get_top_n(predictions, n=3)
      for uid, user_ratings in top_n.items():
          result = [iid for (iid, _) in user_ratings]
      df_row = pd.DataFrame({ 'user_id' : [user_id], 'rec1' : [result[0]], 'rec2' : [result[1]], 'rec3' : [result[2]], 'id' : [id] })
      if not sys.warnoptions:
        warnings.simplefilter("ignore")
      df_rec = df_rec.append(df_row)
      id += 1
    cols = df_rec.columns.tolist()
    cols = cols[-1:] + cols[:-1]
    df_rec = df_rec[cols]
    time.sleep(0.1)
    df_rec.to_sql('recommendation', con=engine, if_exists='replace', index=False)

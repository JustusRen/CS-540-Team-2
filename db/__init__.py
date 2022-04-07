import mysql.connector
import os 
from . import sql_statements
import pandas as pd
from pandas.io import sql
import config
from sqlalchemy import create_engine


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
      + sql_statements.CREATE_BUDDIES_TABLE 
     )

      print('SUCCESS: Create tables.')
    except:
      print('ERROR: Could not create table.')

  def insert_user_data(self):
    df = pd.read_csv ('db/movieLens/processed/users.csv')
    df = df.drop(df.columns[0], axis=1)
    df.rename(columns = {'userId':'id', 'user_name':'first_name'}, inplace = True)

    engine = create_engine(f'mysql+pymysql://{config.DB_CONNECTION}', echo=False)
    try:
      df.to_sql('user', con=engine, if_exists='append', index= False)
      print("SUCCESS: User data inserted.")
    except: 
      print("WARNING: User data already exists")


  def insert_genre_data(self):
    df = pd.read_csv("db/movieLens/processed/genre.csv")
    df = df.drop(df.columns[0], axis=1)
    df.rename(columns = {'genre_id':'id'}, inplace = True)
    
    engine = create_engine(f'mysql+pymysql://{config.DB_CONNECTION}', echo=False)
    try:
      df.to_sql('genre', con=engine, if_exists='append', index=False)
      print("SUCCESS: Genre data inserted.")
    except:
      print("WARNING: Genre data already exists.")  
    
  def insert_movie_data(self):   
    df = pd.read_csv("db/movieLens/raw/movies.csv")
    df = df.drop(df.columns[2], axis=1)
    df.rename(columns = {'movieId':'id'}, inplace = True)

    engine = create_engine(f'mysql+pymysql://{config.DB_CONNECTION}', echo=False)

    try:
      df.to_sql('movie', con=engine, if_exists='append', index=False)
      print("SUCCESS: Movie data inserted.")
    except: 
      print("WARNING: Movie data already exists.")

  def insert_movie_genre_relations(self):
    genre_relation_df = pd.read_csv("db/movieLens/raw/movies.csv")
    #print(genre_relation_df)"""

    #####################  TEST with first 3 movies   #######################

    # iterate through each dataframe
    """for index, row in genre_relation_df.iterrows():
        #get each movie's genres, split by "|" and save in a list
        genres = genre_relation_df.iloc[[index]]['genres'].str.split('|').tolist() #[['Adventure', 'Animation', 'Children']]
        #covert a list of list to one list
        genres = [*genres[0]] #['Adventure', 'Animation', 'Children']
        #iterate through the genres list in that column
        for each_genres in genres:
            #insert into mysql
            print(genre_relation_df.iloc[[index]]['movieId'].tolist()[0], each_genres)
            # engine.execute(genre_relationship.insert(), movie_id = row.movie_id, genre_id = each_genres)
            """
    # result check
    """query = 'SELECT * FROM genre_relationship'
    data = pd.read_sql(query, engine)
    print(data)"""


    """
    ######################## REAL IMPLEMENTATION ##########################
    # but my mac is dying, it took her 30 mins and still running so I stopped it...
   
    # iterate through each dataframe
    for index, row in genre_relation_df.iterrows():
        #get each movie's genres, split by "|" and save in a list
        genres = genre_relation_df.iloc[[index]]['genres'].str.split('|').tolist() #[['Adventure', 'Animation', 'Children']]
        #covert a list of list to one list
        genres = [*genres[0]] #['Adventure', 'Animation', 'Children']
        #iterate through the genres list in that column
        for each_genres in genres:
            #insert into mysql
            engine.execute(genre_relationship.insert(), movie_id = row.movie_id, genre_id = each_genres)
    """

  def insert_rating_data(self):
    df = pd.read_csv ('db/movieLens/processed/rating.csv')
    df = df.drop(df.columns[0], axis=1)
    df = df.drop(df.columns[2], axis=1)
    df.rename(columns = {'rating_binary':'rating', 'userId':'user_id', 'movieId':'movie_id'}, inplace = True)
    df['id'] = df.index
    engine = create_engine(f'mysql+pymysql://{config.DB_CONNECTION}', echo=False)
    try:
      df.to_sql('rating', con=engine, if_exists='append', index = False)
      print("SUCCESS: Rating data inserted.")
    except:
      print("WARNING: Rating data already exists.")
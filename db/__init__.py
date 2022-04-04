import mysql.connector
import os 
from . import sql_statements
import pandas as pd
from pandas.io import sql

class database:
  def __init__(self, host, user, pwd):
    self.host = host
    self.user = user
    self.pwd = pwd

  def check_db_connection(self):
    print('Checking database connection:')
    try:
      mydb = mysql.connector.connect(
        host=self.host,
        user=self.user,
        password=self.pwd
      )
      print('SUCCESS: Connection successful.')
    except:
      print('ERR: Could not connect to database.')

  def create_db(self):
    mydb = mysql.connector.connect(
        host=self.host,
        user=self.user,
        password=self.pwd
      )
    cursor = mydb.cursor()
    cursor.execute(sql_statements.CREATE_DB)
    print('SUCCESS: Created database if it did not exist.')


  def create_tables(self):
    mydb = mysql.connector.connect(
        host=self.host,
        user=self.user,
        password=self.pwd
      )
    cursor = mydb.cursor()
    cursor.execute(
      sql_statements.CREATE_USER_TABLE 
    + sql_statements.CREATE_MOVIE_TABLE
    + sql_statements.CREATE_GENRE_TABLE
    + sql_statements.CREATE_GENRE_RELATIONSHIP_TABLE
    + sql_statements.CREATE_RATING_TABLE
    + sql_statements.CREATE_MATCH_TABLE, multi=True)

    print('SUCCESS: Create tables')

  def insert_user_data(self):
    mydb = mysql.connector.connect(
        host=self.host,
        user=self.user,
        password=self.pwd
      )
    cursor = mydb.cursor()
    df = pd.read_csv ('db/movieLens/processed/users.csv')
    df = df.drop(df.columns[0], axis=1)
    
    print(df)

  def insert_movie_genre_data(self):
    return 0
    # TO-DO: run Ke's script

  def insert_rating_data(self):
    df = pd.read_csv ('db/movieLens/processed/rating.csv')
    df = df.drop(df.columns[0], axis=1)
    print(df)
    return 0
    # TO-DO: write rating.csv to mySQL DB
# Connect to mysql
import pymysql
from sqlalchemy import create_engine
import pandas as pd
from config import config

# you need to change the password and database name
engine = create_engine(f'mysql+pymysql://{config.DB_CONNECTION}', echo=False)
connection = engine.raw_connection()
#cursor = connection.cursor()

#load gener.csv as dataframe
genre_df = pd.read_csv("movielens_data/raw/genre.csv")
# Create gener table
genre_df.to_sql(name='genre', con=engine, if_exists = 'append', index=False)
query = 'SELECT * FROM genre'
data = pd.read_sql(query, engine)
print(data)

#load movies.csv as dataframe
movie_df = pd.read_csv("movielens_data/movies.csv", usecols = ['movie_id','title'])
# Create movie table
movie_df.to_sql(name='movie', con=engine, if_exists = 'append', index=False)
query2 = 'SELECT * FROM movie'
data = pd.read_sql(query2, engine)
print(data)

#load id and genre column from movies.csv as dataframe
genre_relation_df = pd.read_csv("movielens_data/movies.csv", usecols = ['movie_id','genres'])
print(genre_relation_df)

#create genre_relationship table
from sqlalchemy import MetaData, Table, Column, Integer, String

meta = MetaData()

genre_relationship = Table(
   'genre_relationship', meta, 
   Column('movie_id', Integer), 
   Column('genre_id', String(20)), 
)
meta.create_all(engine)

#####################  TEST with first 3 movies   #######################

# iterate through each dataframe
for index, row in genre_relation_df.head(3).iterrows():
    #get each movie's genres, split by "|" and save in a list
    genres = genre_relation_df.iloc[[index]]['genres'].str.split('|').tolist() #[['Adventure', 'Animation', 'Children']]
    #covert a list of list to one list
    genres = [*genres[0]] #['Adventure', 'Animation', 'Children']
    #iterate through the genres list in that column
    for each_genres in genres:
        #insert into mysql
        engine.execute(genre_relationship.insert(), movie_id = row.movie_id, genre_id = each_genres)
        
# result check
query = 'SELECT * FROM genre_relationship'
data = pd.read_sql(query, engine)
print(data)


######################## REAL IMPLEMENTATION ##########################
# but my mac is dying, it took her 30 mins and still running so I stopped it...
"""
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
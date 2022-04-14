from db import Database
import config
from sqlalchemy import create_engine

engine = create_engine(f'mysql+pymysql://{config.DB_CONNECTION}', echo=False)

mydb = Database(config.HOST, config.USER, config.PWD)
mydb.check_db_connection()
mydb.create_db()
mydb.create_tables()
mydb.insert_user_data(engine)
mydb.insert_genre_data(engine)
mydb.insert_movie_data(engine)
mydb.insert_rating_data(engine)
mydb.insert_movie_genre_relations(engine)
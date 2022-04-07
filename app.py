from movie_buddy import create_app
from db import Database
import config

mydb = Database(config.HOST, config.USER, config.PWD)
mydb.check_db_connection()
mydb.create_db()
mydb.create_tables()
mydb.insert_user_data()

mydb.insert_genre_data()

mydb.insert_movie_data()

mydb.insert_rating_data()

app = create_app()

if __name__ == '__main__':
    pass


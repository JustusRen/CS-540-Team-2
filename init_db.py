from database import Database
import config
from sqlalchemy import create_engine

engine = create_engine(f'mysql+pymysql://{config.DB_CONNECTION}', echo=False)

database_manager = Database(config.HOST, config.USER, config.PWD)
database_manager.check_db_connection()
database_manager.create_db()
database_manager.create_tables()
database_manager.insert_user_data(engine)
database_manager.insert_genre_data(engine)
database_manager.insert_movie_data(engine)
database_manager.insert_rating_data(engine)
database_manager.insert_movie_genre_relations(engine)
database_manager.top_n_to_db(engine)
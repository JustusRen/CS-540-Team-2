from movie_buddy import create_app
from db import database
import config

print('---DATABASE CHECK-UP---')
mydb = database(config.HOST, config.USER, config.PWD)
mydb.check_db_connection()

app = create_app()

if __name__ == '__main__':
    pass


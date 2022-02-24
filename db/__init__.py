import mysql.connector

class database:
  def __init__(self, host, user, pwd):
    self.host = host
    self.user = user
    self.pwd = pwd

  def connect_to_db(self):
    mydb = mysql.connector.connect(
        host=self.host,
        user=self.user,
        password=self.pwd
      )
    return mydb

  def check_db_connection(self):
    print('Checking database connection:')
    try:
      mydb = connect_to_db()
      print('Connection successful.')
    except:
      print('ERR: Could not connect to database.')

  def create_db(self):
    mydb = connect_to_db()
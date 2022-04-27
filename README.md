# CS-540-Team-2
## Movie Buddy repository 
The project was implemented with Python 3.8.10. The test system ran Ubuntu 20.04.
### Get started:<br />
- Clone the repository by typing and executing
``` git clone https://github.com/JustusRen/CS-540-Team-2.git ``` in your terminal <br />
- Execute ``` cd CS-540-TEAM-2``` in your terminal to enter the projects directory<br />
- Create a new virtual environment by executing ``` python3 -m venv venv ```<br />
- Activate your venv by executing ``` source venv/bin/activate ```<br />
- Install needed packages from requirements.txt by executing ``` pip3 install -r requirements.txt ``` <br />
- Copy config_example.py and rename it to config.py<br />
The config.py file should stay private because it only applies to your system and contain information about your database connection. Therefore, it is ignored by git.<br />
- Change the strings in config.py to the values required on your system <br />
- Download the dataset from https://www.kaggle.com/datasets/rajmehra03/movielens100k
- Insert the data in the database/movieLens/raw folder. 
- Run the "create user" script by executing ``` python3 database/create_users_table.py ```
- Run the "set rating threshold" script by executing ``` python3 database/set_rating_threshold.py ```
- Run the script to initialize the database by executing ``` python3 init_db.py ```
- Execute ``` export FLASK_APP=app ``` in a terminal in the projects directory. This will let Flask know, where the application is stored<br />
- Run the local server with the command ``` flask run ```. This should start the server. Enter the IP shown in the terminal to access the webpage. <br />

Problems that can occure: 
- Sometimes requirements.txt doesn't install all modules. So you might have to install some modules manually by using ``` pip3 install [module_name] ```
- On some machines an error like this might appear: "mysql.connector, multi=True, sql variable assignment not working". To fix this add the multi=True when you try to execute a sql statment. This should look like ``` cursor.execute(query, multi=True) ```


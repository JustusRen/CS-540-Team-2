# CS-540-Team-2
## Movie Buddy repository
<br /><br />
### Get started:<br />
- Clone the repository by tying
``` git clone https://github.com/JustusRen/CS-540-Team-2.git ``` in your command line <br /><br />
- Execute ``` cd CS-540-TEAM-2``` in a terminal to enter the projects directory<br /><br />
- Create a new virtual environment by executing ``` venv -m venv venv ```<br />The project was implemented and tested on Python 3.8.10.<br /><br />
- Activate your venv by executing ``` source venv/bin/activate ```<br /><br />
- Install needed packages from requirements.txt by executing ``` pip3 install -r requirements.txt ``` <br /><br />
- Copy config_example.py and rename it to config.py<br />
This file contains important strings that should stay private. For example your database password. Therefore, it is ignored by git.<br /><br />
- Change the strings in config.py to the values required on your system <br /><br />
- Execute ``` export FLASK_APP=app ``` in a terminal in the projects directory. This will let Flask know, where the application is stored<br /><br />
- Run the local server with the command ``` flask run ```<br />
This should start the server, create the database and insert all necessary data<br />

Known bugs:
- Sometimes requirements.txt doesn't install all modules. So you might have to install some modules manually by using ``` pip3 install [module_name] ```

TO-DO:
- Import recommendation engine 
- Store likes and dislikes
- Show recommendation results
- Fix import of preprocessed data from MovieLens (more specific: find out why adding genres and ratings doesn't work, add movie_genre relationship data)
- Hash passwords from csv


use movie_buddy; 

create table match (
	id INT PRIMARY KEY AUTO_INCREMENT,
    user_1 INT NOT NULL,
    user_2 INT NOT NULL, 
    movie_id INT NOT NULL, 
    FOREIGN KEY(user_1) REFERENCES user(id), 
    FOREIGN KEY(user_2) REFERENCES user(id), 
    FOREIGN KEY(movie_id) REFERENCES movie(id), 
);

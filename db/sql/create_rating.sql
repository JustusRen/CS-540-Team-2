USE movie_buddy;

create table rating (
    id INT PRIMARY KEY AUTO_INCREMENT,
	user_id INT NOT NULL,
    movie_id INT NOT NULL,
    rating FLOAT NOT NULL,
    rating_binary INT NOT NULL,
    FOREIGN KEY(user_id) REFERENCES user(id),
    FOREIGN KEY(movie_id) REFERENCES movie(id)
);
    
    

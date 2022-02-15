USE movie_buddy;

create table ratings(
	user_id INT NOT NULL,
    movie_id INT NOT NULL,
    rating FLOAT NOT NULL,
    rating_binary INT NOT NULL,
    FOREIGN KEY(user_id) REFERENCES user(user_id),
    FOREIGN KEY(movie_id) REFERENCES movie(movie_id)
);
    
    

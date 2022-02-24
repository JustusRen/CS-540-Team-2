use movie_buddy; 

create table genre_relationship (
	id INT PRIMARY KEY AUTO_INCREMENT,
    movie_id INT NOT NULL,
    genre_id INT NOT NULL,
    FOREIGN KEY (movie_id) REFERENCES movie(id),
    FOREIGN KEY (genre_id) REFERENCES genre(id)
);

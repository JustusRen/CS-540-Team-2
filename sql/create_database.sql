DROP DATABASE movie_buddy;

CREATE DATABASE movie_buddy;

USE movie_buddy;

CREATE TABLE user(
	id INTEGER PRIMARY KEY AUTO_INCREMENT,
    email VARCHAR(255),
    first_name VARCHAR(15),
    password VARCHAR(255)
);
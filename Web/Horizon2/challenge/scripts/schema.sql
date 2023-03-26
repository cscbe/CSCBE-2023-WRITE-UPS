CREATE TABLE users (
    id INT NOT NULL auto_increment,
    username VARCHAR(64) NOT NULL,
    password VARCHAR(64) NOT NULL,
    PRIMARY KEY (id),
    UNIQUE (username(64))
);

CREATE TABLE photos (
    id int not null auto_increment,
    title VARCHAR(64) NOT NULL,
    url VARCHAR(64) NOT NULL,
    visible TINYINT NOT NULL,
    user_id INT NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

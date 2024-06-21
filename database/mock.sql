CREATE SCHEMA hello;
CREATE table IF NOT EXISTS hello.usernames(
   id SERIAL PRIMARY KEY,
   username TEXT NOT NULL UNIQUE,
   dateOfBirth DATE NOT NULL
);

INSERT INTO hello.usernames (username, dateOfBirth) VALUES ('Etevaldo', '7960-11-01');
INSERT INTO hello.usernames (username, dateOfBirth) VALUES ('John', '1990-01-01');
INSERT INTO hello.usernames (username, dateOfBirth) VALUES ('Mary', '1990-11-01');
INSERT INTO hello.usernames (username, dateOfBirth) VALUES ('Jane', '1990-01-21');

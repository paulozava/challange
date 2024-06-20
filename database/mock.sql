CREATE SCHEMA hello;
CREATE table IF NOT EXISTS hello.usernames(
   id SERIAL PRIMARY KEY,
   username TEXT NOT NULL UNIQUE,
   dateOfBirth DATE NOT NULL
);

INSERT INTO hello.usernames (username, dateOfBirth) VALUES ('etevaldo', '7960-11-01');

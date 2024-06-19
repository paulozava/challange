DROP SCHEMA IF EXISTS hello CASCADE;
CREATE SCHEMA hello;
CREATE table IF NOT EXISTS hello.usernames(
   id SERIAL PRIMARY KEY,
   username VARCHAR(200) NOT NULL,
   dateOfBirth DATE NOT NULL
);

INSERT INTO hello.usernames (username, dateOfBirth) VALUES ('etevaldo', '7960-11-01');

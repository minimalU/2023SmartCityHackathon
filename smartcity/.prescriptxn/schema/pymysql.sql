DROP SCHEMA IF EXISTS prescriptxn;
CREATE SCHEMA prescriptxn;
USE prescriptxn;

DROP TABLE IF EXISTS users;
CREATE TABLE users(
    userID SMALLINT NOT NULL AUTO_INCREMENT,
    firstName VARCHAR(50) NOT NULL,
    lastName VARCHAR(50) NOT NULL,
    gender VARCHAR(10) NOT NULL,
    birthday DATE NOT NULL,
    address VARCHAR(100) NOT NULL,
    city VARCHAR(50) NOT NULL,
    province VARCHAR(50) NOT NULL,
    postalCode VARCHAR(20) NOT NULL,
    email VARCHAR(100) NOT NULL,
    PRIMARY KEY(userID)
);

INSERT INTO users VALUES (1011, 'prescriptxn', 'FourY', 'other', '2023-05-01', 'Seneca Hill DR','North Yourk', 'ON','M2J 2X5', 'ekim2911@conestogac.on.ca');


select * from users;


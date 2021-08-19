CREATE DATABASE ethereum;

USE ethereum;

CREATE TABLE quotes (
  `datetime` DATETIME      PRIMARY KEY,
  quote      DECIMAL(8, 4) NOT NULL
);

CREATE USER 'ethereum' IDENTIFIED BY '135791';

GRANT ALL ON TABLE quotes TO 'ethereum';

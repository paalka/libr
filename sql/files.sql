CREATE SCHEMA libr;
SET SEARCH PATH TO libr;

CREATE TABLE category (
       id serial PRIMARY KEY NOT NULL,
       title varchar(40) NOT NULL,
       category SERIAL REFERENCES category(id)
);

CREATE TABLE file (
       id SERIAL PRIMARY KEY NOT NULL,
       date_added date NOT NULL DEFAULT CURRENT_DATE,

       title varchar(50) NOT NULL,
       filepath varchar(140) NOT NULL,

       category SERIAL REFERENCES category(id)
);

GRANT SELECT,INSERT ON ALL TABLES IN SCHEMA libr TO libr;

CREATE SCHEMA libr;
SET SEARCH_PATH TO libr;

CREATE TABLE category (
       id serial PRIMARY KEY NOT NULL,
       title varchar(40) NOT NULL
);

CREATE TABLE file (
       id SERIAL PRIMARY KEY NOT NULL,
       date_added date NOT NULL DEFAULT CURRENT_DATE,

       title varchar(50) NOT NULL,
       filepath varchar(140) NOT NULL,
       category int REFERENCES category(id),
       tags text
);

CREATE TABLE subcategory (
       parent int REFERENCES category(id),
       child int REFERENCES category(id)
);

GRANT USAGE ON SCHEMA libr TO libr;
GRANT SELECT,UPDATE ON file_id_seq TO libr;
GRANT SELECT,UPDATE,INSERT ON ALL TABLES IN SCHEMA libr TO libr;

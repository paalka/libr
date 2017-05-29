CREATE SCHEMA libr;
SET SEARCH_PATH TO libr;

CREATE TABLE category (
       id serial PRIMARY KEY NOT NULL,
       title text NOT NULL CONSTRAINT category_must_be_unique UNIQUE,
);

CREATE TABLE file (
       id SERIAL PRIMARY KEY NOT NULL,
       date_added date NOT NULL DEFAULT CURRENT_DATE,

       title text NOT NULL,
       filepath text NOT NULL,
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
GRANT SELECT,UPDATE ON libr.category_id_seq TO libr;

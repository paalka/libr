SET SEARCH_PATH TO libr;
BEGIN;
  ALTER TABLE libr.category ADD CONSTRAINT category_must_be_unique UNIQUE(title);
COMMIT;

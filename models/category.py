import db as db_helpers

def add_category(dbh, category_title):
    insert_query = """
                   INSERT INTO libr.category (title) VALUES (%s);
                   """

    db_helpers.execute_insert_query(dbh, insert_query, (category_title, ))

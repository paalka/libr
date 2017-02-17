import libr.db as db_helpers

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config.get("ALLOWED_EXTENSIONS")


def add_file(dbh, filename, tags, filepath, category_id):
    insert_query = """
                   INSERT INTO libr.file (title, filepath, tags, category) VALUES (%s, %s, %s, %s);
                   """

    db_helpers.execute_insert_query(dbh, insert_query, (filename, filepath, tags, category_id))


def update_file(dbh, filename, tags, filepath, category_id, file_id):
    update_query = """
                   UPDATE libr.file SET (title, filepath, tags, category) = (%s, %s, %s, %s) WHERE file.id = %s;
                   """

    db_helpers.execute_update_query(dbh, update_query, (filename, filepath, tags, category_id, file_id))


def find_matching_files(dbh, query):
    search_query = """
                   SELECT file.title, file.tags, file.filepath, category.title, file.id
                   FROM libr.file JOIN category ON file.category = category.id
                   WHERE file.title ILIKE %s OR file.tags ILIKE %s OR category.title ILIKE %s;
                   """
    user_query = "%" + query + "%"
    all_files = db_helpers.execute_select_query(dbh, search_query, (user_query, user_query, user_query))
    return all_files

def get_file_data(dbh, file_id):
    file_query = """
                 SELECT file.title, file.tags, file.filepath, category.title, category.id
                 FROM libr.file JOIN category ON file.category = category.id
                 WHERE file.id = %s;
                 """
    return db_helpers.execute_select_query_one(dbh, file_query, (file_id,))

def get_all_categories(dbh):
    category_query = """
                     SELECT * FROM category;
                     """
    return db_helpers.execute_select_query(dbh, category_query, ())

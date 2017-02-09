import psycopg2

def create_connection_string(db_host, db_name, db_user, db_passwd):
    return "host='{}' dbname='{}' user='{}' password='{}'".format(db_host, db_name, db_user, db_passwd)

def connect_to_db(db_config):
    db_host = db_config.get("DB_HOST")
    db_name = db_config.get("DB_NAME")
    db_user = db_config.get("DB_USER")
    db_passwd = db_config.get("DB_PASSWD")
    conn = psycopg2.connect(create_connection_string(db_host, db_name, db_user, db_passwd))
    return conn

def execute_select_query(db_handle, query, parms=None):
    cursor = db_handle.cursor()
    cursor.execute(query, parms)

    return cursor.fetchall()

def execute_insert_query(db_handle, query, parms=None):
    cursor = db_handle.cursor()
    cursor.execute(query, parms)
    db_handle.commit()

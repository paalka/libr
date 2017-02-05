import psycopg2
import config

def create_connection_string(db_host, db_name, db_user, db_passwd):
    return "host='{}' dbname='{}' user='{}' password='{}'".format(db_host, db_name, db_user, db_passwd)

def connect_to_db(db_config):
    db_host = db_config.get("DB_HOST")
    db_name = db_config.get("DB_NAME")
    db_user = db_config.get("DB_USER")
    db_passwd = db_config.get("DB_PASSWD")
    conn = psycopg2.connect(create_connection_string(db_host, db_name, db_user, db_passwd))
    print conn

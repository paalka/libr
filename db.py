import psycopg2
import config

def create_connection_string(db_host, db_name, db_user, db_passwd):
    return "host='{}' dbname='{}' user='{}' password='{}'".format(db_host, db_name, db_user, db_passwd)

def connect_to_db(db_host, db_name, db_user, db_passwd):
    conn = psycopg2.connect(create_connection_string(db_host, db_name, db_user, db_passwd))
    print conn

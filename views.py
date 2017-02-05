from flask import render_template
from flask import request
import json

from libr import app
from db import connect_to_db, execute_query

@app.route("/")
def index():
    return render_template("search.jinja2")

@app.route("/search/", methods=["POST"])
def search():
    query_dict = request.get_json()
    matching_files = find_matching_files(query_dict["query"])
    return json.dumps(matching_files)

def find_matching_files(query):
    db_handle = connect_to_db(app.config)
    search_query = """
                   SELECT file.title, category.title, file.filepath
                   FROM file JOIN category ON file.category = category.id
                   WHERE file.title ILIKE %s OR category.title ILIKE %s;
                   """
    user_query = "%" + query + "%"
    all_files = execute_query(db_handle, search_query, (user_query, user_query))
    return all_files

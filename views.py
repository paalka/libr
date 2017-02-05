from flask import render_template
from flask import request
from libr import app
from db import connect_to_db, execute_query

@app.route("/")
@app.route("/search/<query>", methods=["GET"])
def index(query=None):
    matching_files = {}
    if query != None:
        pass
    else:
        matching_files = find_matching_files(query)

    return render_template("search.jinja2", matching_files=matching_files)

@app.route("/search/", methods=["POST"])
def search():
    matching_files = find_matching_files(request.form.get("query"))
    return "hi"

def find_matching_files(query):
    db_handle = connect_to_db(app.config)
    search_query = """
                   SELECT file.title, category.title
                   FROM file JOIN category ON file.category = category.id
                   WHERE file.title ILIKE %s OR category.title ILIKE %s;
                   """
    user_query = "%" + query + "%"
    return execute_query(db_handle, search_query, (user_query, user_query))

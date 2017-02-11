from flask import render_template
from flask import request, redirect, url_for
import os
from werkzeug.utils import secure_filename

import json

from libr import app
from db import connect_to_db, execute_select_query, execute_insert_query

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config.get("ALLOWED_EXTENSIONS")

@app.route("/")
def index():
    return render_template("search.jinja2")

@app.route("/search/", methods=["POST"])
def search():
    query_dict = request.get_json()
    query = query_dict.get("query", "")
    matching_files = find_matching_files(query)
    return json.dumps(matching_files)

def find_matching_files(query):
    db_handle = connect_to_db(app.config)
    search_query = """
                   SELECT file.title, file.tags, file.filepath
                   FROM libr.file
                   WHERE file.title ILIKE %s OR file.tags ILIKE %s;
                   """
    user_query = "%" + query + "%"
    all_files = execute_select_query(db_handle, search_query, (user_query, user_query))
    return all_files

def add_file(filename, tags, filepath, category_id):
    db_handle = connect_to_db(app.config)
    insert_query = """
                   INSERT INTO libr.file (title, filepath, tags, category) VALUES (%s, %s, %s, %s);
                   """
    execute_insert_query(db_handle, insert_query, (filename, filepath, tags, category_id))


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':

        # check if the post request has the file part
        if 'file' not in request.files:
            return redirect(request.url)
        uploaded_file = request.files['file']
        file_title = request.form.get("title")
        category_id = request.form.get("category")
        tags = request.form.get("tags")

        # if user does not select file, browser also
        # submit a empty part without filename
        if uploaded_file.filename == '':
            return redirect(request.url)

        if uploaded_file and allowed_file(uploaded_file.filename):
            filepath = secure_filename(uploaded_file.filename)
            add_file(file_title, tags, filepath, category_id)
            uploaded_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filepath))
            return redirect(url_for('index'))

    db_handle = connect_to_db(app.config)
    all_categories = execute_select_query(db_handle, "SELECT * FROM category")
    return render_template("upload.jinja2", all_categories=all_categories)

from flask import render_template
from flask import request, redirect, url_for
import os
from werkzeug.utils import secure_filename

import json

from libr import app
from db import connect_to_db, execute_query

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
                   SELECT file.title, category.title, file.filepath
                   FROM file JOIN category ON file.category = category.id
                   WHERE file.title ILIKE %s OR category.title ILIKE %s;
                   """
    user_query = "%" + query + "%"
    all_files = execute_query(db_handle, search_query, (user_query, user_query))
    return all_files


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('index',
                                    filename=filename))
    return '''
<!doctype html>
<title>Upload new File</title>
<h1>Upload new File</h1>
<form method=post enctype=multipart/form-data>
<p><input type=file name=file>
    <input type=submit value=Upload>
</form>
'''

from flask import render_template
from flask import request, redirect, url_for
import os
from werkzeug.utils import secure_filename

import json

from libr import app
from models.file import add_file, update_file, find_matching_files, get_file_data, get_all_categories
from models.file import allowed_file

@app.route("/")
def index():
    return render_template("search.jinja2")

@app.route("/search/", methods=["POST"])
def search():
    query_dict = request.get_json()
    query = query_dict.get("query", "")
    matching_files = find_matching_files(query)
    return json.dumps(matching_files)



@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':

        errors = []

        # check if the POST request has the file part
        if 'file' not in request.files:
            errors.append("No file given!")
            return render_template("upload.jinja2", errors=errors)

        uploaded_file = request.files['file']
        file_title = request.form.get("title")
        category_id = request.form.get("category")
        tags = request.form.get("tags")

        if uploaded_file.filename == '':
            errors.append("The filename cannot be empty!")

        if not file_title:
            errors.append("The file must have a title!")

        if not category_id:
            errors.append("A category must be selected!")

        if len(errors) > 0:
            return render_template("upload.jinja2", errors=errors)

        if uploaded_file and allowed_file(uploaded_file.filename):
            filepath = secure_filename(uploaded_file.filename)
            add_file(file_title, tags, filepath, category_id)
            uploaded_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filepath))
            return render_template("upload.jinja2", successful=True)

    db_handle = connect_to_db(app.config)
    all_categories = execute_select_query(db_handle, "SELECT * FROM category")
    return render_template("upload.jinja2", all_categories=all_categories)

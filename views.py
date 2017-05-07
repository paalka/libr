import os
import json
from flask import request, redirect, url_for, g, render_template
from werkzeug.utils import secure_filename

from libr import app
from models.file import add_file, update_file, find_matching_files, get_file_data, get_all_categories, get_n_newest_files
from models.category import add_category
from forms import FileForm, CategoryForm

@app.route("/")
def index():
    newest_files = get_n_newest_files(g.psql_dbh, 25)
    return render_template("search.jinja2", files=newest_files)

@app.route("/search/", methods=["POST"])
def search():
    query_dict = request.get_json()
    query = query_dict.get("query", "")
    matching_files = find_matching_files(g.psql_dbh, query)

    html = render_template("search_results.jinja2", files=matching_files)
    return json.dumps({"html": html.strip()})


@app.route("/edit/<int:file_id>", methods=["GET", "POST"])
def edit(file_id):
    file_form = FileForm()
    all_categories = get_all_categories(g.psql_dbh)
    file_form.uploaded_file.validators = []
    file_form.categories.choices = all_categories

    file_data = get_file_data(g.psql_dbh, file_id)

    if request.method == 'POST' and file_form.validate_on_submit():
        uploaded_file = file_form.uploaded_file.data
        filepath = secure_filename(uploaded_file.filename)

        file_title = file_form.file_title.data
        tags = file_form.tags.data.lower()
        category_id = file_form.categories.data

        if filepath == '':
            uploaded_file = file_data[2]
        else:
            uploaded_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filepath))
            uploaded_file = filepath

        update_file(g.psql_dbh, file_title, tags, uploaded_file, category_id, file_id)
        return redirect("/edit/" + str(file_id))

    elif request.method == 'GET':
        file_form.file_title.data = file_data[0]
        file_form.categories.data = file_data[4]
        file_form.tags.data = file_data[1]
        file_form.uploaded_file.extra = "Current file: " + file_data[2]

    return render_template("edit.jinja2", form=file_form)


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    upload_form = FileForm()
    all_categories = get_all_categories(g.psql_dbh)
    upload_form.categories.choices = all_categories
    successful = None

    if request.method == 'POST' and upload_form.validate_on_submit():
        uploaded_file = upload_form.uploaded_file.data
        filepath = secure_filename(uploaded_file.filename)
        uploaded_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filepath))

        file_title = upload_form.file_title.data
        tags = upload_form.tags.data.lower()
        category_id = upload_form.categories.data

        add_file(g.psql_dbh, file_title, tags, filepath, category_id)

        successful = True

    return render_template("upload.jinja2", form=upload_form, successful=successful)

@app.route('/add_category', methods=['GET', 'POST'])
def category_add():
    category_form = CategoryForm()
    successful = None

    if request.method == 'POST' and category_form.validate_on_submit():
        category_title = category_form.category_title.data

        add_category(g.psql_dbh, category_title)
        successful = True

    return render_template("add_category.jinja2", form=category_form, successful=successful)

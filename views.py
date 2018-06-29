import os
import json
import pathlib
from flask import request, redirect, g, render_template, redirect
from werkzeug.utils import secure_filename

from libr import app
from forms import FileForm
from pdf import PDF, store_pdf, edit_pdf
from indexer import Index

@app.route("/")
def index():
    return render_template("search.jinja2", files=sorted(app.ind.entries.values(), key=lambda x: x.last_updated, reverse=True))

@app.route("/search/", methods=["POST"])
def search():
    query_dict = request.get_json()
    query = query_dict.get("query", "")
    if not app.ind:
        app.ind = Index()
        app.ind.index_documents(app.config["UPLOAD_FOLDER"])
    matching_files = app.ind.find(query)

    html = render_template("search_results.jinja2", files=matching_files)
    return json.dumps({"html": html.strip()})

@app.route("/edit/<string:file_id>", methods=["GET", "POST"])
def edit(file_id):
    file_form = FileForm()
    file_form.uploaded_file.validators = []
    successful = None

    doc = app.ind.entries.get(file_id)
    if not doc:
        return redirect("/")

    if request.method == 'POST' and file_form.validate_on_submit():
        file_title = file_form.file_title.data
        tags = file_form.tags.data.lower()
        tags = file_form.tags.data.lower()
        category = file_form.category.data.lower()

        new_pdf = edit_pdf(doc, file_title, tags, category)
        app.ind.index_documents(app.config["UPLOAD_FOLDER"])
        successful = True
        return redirect("/edit/" + new_pdf.checksum)
    elif request.method == 'GET':
        file_form.file_title.data = doc.title
        file_form.tags.data = doc.keywords
        file_form.category.data = doc.category
        file_form.uploaded_file.extra = "Current file: " + doc.title

    return render_template("edit.jinja2", form=file_form, successful=successful)

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    upload_form = FileForm()
    successful = None

    if request.method == 'POST' and upload_form.validate_on_submit():
        uploaded_file = upload_form.uploaded_file.data
        filepath = secure_filename(uploaded_file.filename)

        file_title = upload_form.file_title.data
        tags = upload_form.tags.data.lower()
        category = upload_form.category.data.lower()

        ext = pathlib.Path(filepath).suffix
        new_filename = secure_filename(file_title).lower() + ext

        output_filepath = os.path.join(app.config["UPLOAD_FOLDER"], new_filename)
        store_pdf(file_title, tags, category, uploaded_file.stream, output_filepath)

        app.ind.index_documents(app.config["UPLOAD_FOLDER"])
        successful = True

    return render_template("upload.jinja2", form=upload_form, successful=successful)

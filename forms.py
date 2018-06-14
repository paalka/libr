from wtforms import StringField, FileField, TextAreaField, SelectField, validators
from flask_wtf import Form
from flask_wtf.file import FileRequired

class FileForm(Form):
    file_title = StringField('Title', [validators.Length(min=4), validators.required()])
    uploaded_file = FileField("PDF file", [FileRequired()])
    category = StringField('Category', [validators.Length(min=2), validators.required()])
    tags = TextAreaField('Tags')

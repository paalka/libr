from wtforms import StringField, FileField, TextAreaField, SelectField, validators
from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired
from models.file import allowed_file

class FileForm(FlaskForm):
    file_title = StringField('Title', [validators.Length(min=4, max=70), validators.required()])
    categories = SelectField('Category', [validators.required()], coerce=int)
    uploaded_file = FileField("PDF file", [FileRequired()])
    tags = TextAreaField('Tags')

class CategoryForm(FlaskForm):
    category_title = StringField('Category', [validators.Length(min=2, max=70), validators.required()])

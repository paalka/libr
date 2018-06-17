from flask import Flask
from indexer import Index

app = Flask(__name__)
import views
app.config.from_object("settings.LocalConfig")
app.ind = Index()
app.ind.index_documents(app.config["UPLOAD_FOLDER"])

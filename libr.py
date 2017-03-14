from flask import Flask
from db import init_dbh

app = Flask(__name__)
import views
app.config.from_object("settings.LocalConfig")

init_dbh(app)

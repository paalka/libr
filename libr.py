from flask import Flask
from settings import CONFIG_DICT
from db import init_dbh

app = Flask(__name__)
import views
app.config.update(CONFIG_DICT)
init_dbh(app)

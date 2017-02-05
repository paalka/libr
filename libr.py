from flask import Flask
from settings import CONFIG_DICT

app = Flask(__name__)
import views
app.config.update(CONFIG_DICT)

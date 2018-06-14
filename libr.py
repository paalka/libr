from flask import Flask

app = Flask(__name__)
import views
app.config.from_object("settings.LocalConfig")
app.ind = None

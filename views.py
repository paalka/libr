from libr import app

@app.route("/")
def index():
    return "hi"

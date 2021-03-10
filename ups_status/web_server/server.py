from flask import Flask

app = Flask("Logging Web Server")


@app.route("/home")
def hello_world():
    return "Merge world"


@app.route("/about/<username>")
def about():
    return "About page"

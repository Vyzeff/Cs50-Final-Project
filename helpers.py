from flask import render_template

def error(message, code=400):
    return render_template("error.html", message=message, code=code)
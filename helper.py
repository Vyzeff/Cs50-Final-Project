from functools import wraps
from flask import redirect, render_template, session

"""
from https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
"""
def login_verify(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

def error(message):
    return render_template("error.html", message)


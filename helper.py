from functools import wraps
from flask import redirect, render_template, session


# From https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
# Redirects to login if not logged in
def login_verify(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

# Creates an error message
def error(message, code=400):
    return render_template("error.html", message=message, code=code)


from flask import render_template

def error(message, code=400):
    """Error

    Args:
        message (_type_): error message
        code (int, optional): A error code Defaults to 400.

    Returns:
        _type_: Simple error message generator.
    """
    return render_template("error.html", message=message, code=code)
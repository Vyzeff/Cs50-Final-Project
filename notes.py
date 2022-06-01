from flask import Blueprint

notes = Blueprint("notes", __name__, static_folder="static", template_folder="templates")
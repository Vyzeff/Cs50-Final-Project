from re import L
from flask import Flask, render_template, session, request
from flask_session import Session

from datetime import datetime
from helpers import error

from models import models
from todo import todo, todoHome, todoCreate
from user import user, login, logout, register

# Flask
## Configures the app
app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True

## Makes so data is saved in files
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite+pysqlite:///homebook.db"

## Defines flask session
Session(app)


user.register_blueprint(models, url_prefix="")
app.register_blueprint(user, url_prefix="")
app.register_blueprint(todo, url_prefix="")


@app.route("/")
def index():
    """    
    TODO
     Pagina base com a sidebar
     Um relogio
     themes: basic, cold, contrast, lofi and sakura 
     notas mais recentes
     """

    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def registerRoute():
    
    if request.method == "GET":
        return render_template("register.html")
    
    if request.method == "POST":
        if not request.form.get("username"):
            return render_template("register.html", invalid="1")
        if not request.form.get("password"):
            return render_template("register.html", invalid="2")
        if request.form.get("password") != request.form.get("confirm"):
            return render_template("register.html", invalid="3")
        username = request.form.get("username")
        password = request.form.get("password")
        register(username, password)
        return render_template("login.html", success=1)



@app.route("/login", methods=["GET", "POST"])
def loginRoute():
    
    session.clear()
    
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        if not request.form.get("username"):
                return render_template("login.html", invalid="1")
        if not request.form.get("password"):
            return render_template("login.html", invalid="1")
        username = request.form.get("username")
        password = request.form.get("password")

        if login(username, password) == False:
            return render_template("invalid.html")
        return render_template("index.html")

@app.route("/logout")
def logoutRoute():
    if request.method == "GET":
        logout()
        return render_template("index.html")
    return error("You should not be here, please retry")


@app.route("/notebook")
def notebook():
    """
    will let the user take notes in separate blocks which can be arranged
    will show all notes
    notas vao ter titulo, data e corpo
    """

    return error("TODO, NOTEBOOK")

@app.route("/clock")
def clocks():
    """
    timers e relogios
    eh possivel escolher relogios de outras regioes
    criar alarmes e timers
    multiplos relogios ao mesmo tempo
    """

    return error("TODO, CLOCK")

@app.route("/todo", methods=["GET", "POST", "PUT", "DELETE"])
def checklists():
    thisMethod = request.method
    todoHome(thisMethod)

@app.route("/todos", methods=["POST", "GET"])
def newTodos():
    thisMethod = request.method
    todoCreate(thisMethod)
           

@app.route("/water")
def waterBottle():
    """
        contador de agua
        meta diaria
        botao para tomar agua
        cicla entre imagens de uma garrafa de agua
        form com botao para tomar uma medida de agua definida pelo usuario
    """

    return error("TODO WATER")

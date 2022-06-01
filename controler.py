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


success = False
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
    thisMethod = request.method
    register(thisMethod)


@app.route("/login", methods=["GET", "POST"])
def loginRoute():
    thisMethod = request.method
    login(thisMethod)

@app.route("/logout")
def logoutRoute():
    logout()


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

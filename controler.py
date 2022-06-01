from flask import Flask, jsonify, make_response, redirect, render_template, session, request
from flask_session import Session

from helpers import error

from models import models
from todo import todo, todoCreate, todoUpdate, todoVerify
from user import user, login, logout, register
from notes import notes

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
app.register_blueprint(notes, url_prefix="")

@app.route("/")
def index():
    """Index

    Renders homepage.
    """
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def registerRoute():
    """Register Route

    Controls what happens when the register button is clicked, calls register().
    If sucessfull, renders login.html with success alert.
    """
    
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
    """Login Route

    Forgets any previous sessions, controls what happens when login button is clicked.
    Calls login(), if nothing happens, returns to index.
    """
    
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
    return error("You should not be here, please retry")


@app.route("/logout")
def logoutRoute():
    """Logout Route

    Logs user out by forgetting the session
    """
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
    if request.method == "GET":
        return render_template("notebook.html")
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
def todoRoute():
    """Chelist route

    Controls what happens when todo link is clicked. Calls various functions, todoVerify() verifies
    if there is any todo under that particular user session, todoUpdate() completes or deletes todos.
    """
    if request.method == "GET":
        todoList = todoVerify()
        if todoList == None:
            return render_template("todo.html", notodo="0")
        return render_template("todo.html", userTodos=todoList, notodo="1")
    
    if request.method == "POST":
        return redirect("/todos")

    if request.method == "PUT":
        updateId = request.get_json()
        todoUpdate(updateId, 1)
        return make_response(jsonify({"message": "to-do added"}))

    
    if request.method == "DELETE":
        updateId = request.get_json()
        todoUpdate(updateId, 2)
        return make_response(jsonify({"message": "to-do deleted"}))

@app.route("/todos", methods=["POST", "GET"])
def newTodosRoute():
    """New Todos Route

    Controls what happens when "create" button is clicked. Creates new todos with fetch from
    javascript and creates todos based on that input and todoCreate()
    """
    if request.method == "GET":
        return render_template("todos.html")

    if request.method == "POST":
        formInput = request.get_json()  
         
        if formInput == None or formInput == "400":
            return error("Please input valid text.")
        todoCreate(formInput)
        return make_response(jsonify({"message":"to-do added"}))


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

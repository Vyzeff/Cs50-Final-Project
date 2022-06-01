from flask import Flask, render_template, redirect, session, request, jsonify, make_response, Blueprint
from flask_session import Session

from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

from modules import modules, sqlChangeTodo, sqlCreateTodo, sqlCreateUser, sqlGetTodo, sqlGetUser
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

app.register_blueprint(modules, url_prefix="/")

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
def register():
    """
    will ask for an unused username
    will ask for a password ate least 8 digits long, together with 1 number and 1 symbol
    maybe implement captcha???
    must have invalid when input user already exists in db
    """
    if request.method == "POST":
        if not request.form.get("username"):
            return render_template("register.html", invalid="1")
        if not request.form.get("password"):
            return render_template("register.html", invalid="2")
        if request.form.get("password") != request.form.get("confirm"):
            return render_template("register.html", invalid="3")
        
        # lowercase username for consistensy
        userLow = request.form.get("username").lower()
        # username is already in use

        if sqlGetUser(userLow, 2) != 0:
            return render_template("register.html", invalid="4")
        
        # Hash password with sha256 and salt 8
        passHash = generate_password_hash(request.form.get("password"), "sha256", 8)
        
        # create a new user with the input values
        sqlCreateUser(userLow, passHash)
        success = True
        return render_template("login.html", success=1)

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login(): 
    """    
    will redirect to login page
    will take a username and password
    check if those things are in db
    either log in or error popup
    Forgets user
    when user and/or password go wrong, reload with invalid for html if
    """
    # forgets previous session
    session.clear()
    
    
    if request.method == "GET":
        if success == True:
            success == False
            return render_template("login.html", success="1")
        return render_template("login.html")
    
    #these will only happen if the method is post
    if not request.form.get("username"):
            return render_template("login.html", invalid="1")
    if not request.form.get("password"):
        return render_template("login.html", invalid="1")
    
    # query in sql in the user table where username = input in username, grab first
    # returns a dict
    
    userInput = sqlGetUser(request.form.get("username").lower(), 1)
    
    # check if there was a username like that and if the password is correct by the hash
    if userInput == None or not check_password_hash(userInput.hash, request.form.get("password")):
        return render_template("login.html", invalid="1")
    # remember the user id
    session["user_id"] = userInput.id
    
    return redirect("/")
@app.route("/logout")
def logout():
    """
    forgets user id and 'logs out'
    """
    session.clear()
    
    return redirect("/")

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
    """
    pagina de checklists.
    é nela onde se deleta e faz o update dos todos ja existentes
    redireciona para outra rota para criar todos
    """
   
    userTodos = sqlGetTodo(session["user_id"])
    
    if request.method == "GET":
        if sqlGetTodo(session["user_id"], 1) == None:
            return render_template("todo.html", notodo="0")
        return render_template("todo.html", userTodos=userTodos, notodo="1")
    
    if request.method == "POST":
        return redirect("/todos")
    
    if request.method == "PUT":
        updateId = request.get_json()
        
        sqlChangeTodo(updateId, 0)
        return make_response(jsonify({"message":"to-do completed"}))


    if request.method == "DELETE":
        deleteId = request.get_json()
        
        sqlChangeTodo(deleteId["input"], 1)
        
    return error("TODO TODOS")

@app.route("/todos", methods=["POST", "GET"])
def todos():
    """
    generates todos with fetch from input in javascript
    """
    
    if request.method == "GET":
        return render_template("todos.html")

    
    if request.method == "POST":
        formInput = request.get_json()  
         
        if formInput == None or formInput == "400":
            return error("Please input valid text.")
    # create a session with the input values
        nowDate = str(datetime.now())
        
        sqlCreateTodo(session["user_id"], formInput["input"], nowDate)
        
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

def error(message, code=400):
    return render_template("error.html", message=message, code=code)
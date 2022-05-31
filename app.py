from flask import Flask, render_template, redirect, session, request, jsonify, make_response
from flask_session import Session

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, MetaData
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import declarative_base, sessionmaker

from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
from helper import login_verify, error


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


#SQLAlchemy
## Orm SQLAlchemy stuff
metadata_obj = MetaData()
base = declarative_base()

## Creates engine for SQLAlchemy
engine = create_engine("sqlite+pysqlite:///homebook.db", echo=True, future=True, connect_args={'check_same_thread': False})

## If Database isn't present, create one
if not database_exists(engine.url):
    create_database(engine.url)


## Define classes do sqlalchemy
class Users(base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String(20), nullable=False)
    hash = Column(String, nullable=False)
    
    def __repr__(self):
        return f"User(id={self.id!r}, username={self.username!r}, hash={self.hash!r})"
class Todo(base):
    __tablename__ = "todo"
    
    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    todo_text = Column(String, nullable=False)
    date = Column(String, nullable=False)
    iscomplete = Column(Integer, nullable=False)
    
    def __repr__(self):
        return f"Todo(id={self.id!r}, user_id={self.user_id!r}, todo_text={self.todo_text!r}, iscomplete={self.iscomplete!r})"

# cria essas classes na db se não estiverem ja la.
base.metadata.create_all(engine)

sqlASession = sessionmaker(bind=engine)
sqlSession = sqlASession()


success = False
@app.route("/")
@login_verify
def index():
    #TODO
    # Pagina base com a sidebar, temperatura e dia.
    # Um relogio
    # themes: dark, light, gray, purple, orange and let the user customize the colors and font for themselves
    # notas mais recentes
    # uma checklist vai aparecer, a que tem a flag de "importante"
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    # will ask for an unused username
    # will ask for a password ate least 8 digits long, together with 1 number and 1 symbol
    # maybe implement captcha???
    # must have invalid when input user already exists in db
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
        if sqlSession.query(Users).filter_by(username=userLow).count() != 0:
            return render_template("register.html", invalid="4")
        
        # Hash password with sha256 and salt 8
        passHash = generate_password_hash(request.form.get("password"), "sha256", 8)
        
        # create a session with the input values
        newUser = Users(username=userLow, hash=passHash)
        sqlSession.add(newUser) 
        # commit values to database
        sqlSession.commit()
        success = True
        return redirect("/login")

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login(): 
    # will redirect to login page
    # will take a username and password
    # check if those things are in db
    # either log in or error popup
    # Forgets user
    # when user and/or password go wrong, reload with invalid for html if
    
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
    userInput = sqlSession.query(Users).filter_by(username=(request.form.get("username").lower())).first()
    
    # check if there was a username like that and if the password is correct by the hash
    if userInput == None or not check_password_hash(userInput.hash, request.form.get("password")):
        return render_template("login.html", invalid="1")
    # remember the user id
    session["user_id"] = userInput.id
    
    return redirect("/")
@app.route("/logout")
def logout():
    
    # forgets user id.
    session.clear()
    
    return redirect("/")

@app.route("/notebook")
def notebook():
    # will let the user take notes in separate blocks which can be arranged
    # will show all notes
    # notas vao ter titulo, data e corpo
    return error("TODO, NOTEBOOK")

@app.route("/clock")
def clocks():
    # timers e relogios
    # eh possivel escolher relogios de outras regioes
    # criar alarmes e timers
    # multiplos relogios ao mesmo tempo
    return error("TODO, CLOCK")

@app.route("/todo", methods=["GET", "POST", "PUT", "DELETE"])
def checklists():
    # pagina de checklists.
    # vai ser possivel criar uma ou mais checklists
    # uma delas pode ser dada como "importante" e vai aparecer na index
    # da mesma forma do notebook, elas podem ser arrastadas por ai
    userTodos = sqlSession.query(Todo).filter_by(user_id=session["user_id"])
    
    if request.method == "GET":
        if sqlSession.query(Todo).filter_by(user_id=session["user_id"]).first() == None:
            return render_template("todo.html", notodo="0")
        return render_template("todo.html", userTodos=userTodos, notodo="1")
    
    if request.method == "POST":
        return redirect("/todos")
    
    if request.method == "PUT":
        updateId = request.get_json()
        
        updateTodo = sqlSession.query(Todo).filter_by(id=updateId["input"]).first()
        updateTodo.iscomplete = 1
        sqlSession.commit() 
        
        return make_response(jsonify({"message":"to-do completed"}))


    if request.method == "DELETE":
        deleteId = request.get_json()

        deleteTodo = sqlSession.query(Todo).filter_by(id=deleteId["input"]).first()
        sqlSession.delete(deleteTodo)
        sqlSession.commit()
        
    return error("TODO TODOS")

@app.route("/todos", methods=["POST", "GET"])
def todos():
    
    if request.method == "GET":
        return render_template("todos.html")

    
    if request.method == "POST":
        formInput = request.get_json()  
         
        if formInput == None or formInput == "400":
            return error("Please input valid text.")
    # create a session with the input values
        nowDate = str(datetime.now())
        newTodo = Todo(user_id=session["user_id"], todo_text=formInput["input"], date=nowDate, iscomplete=0)
        sqlSession.add(newTodo) 
        # commit values to database
        sqlSession.commit()
        return make_response(jsonify({"message":"to-do added"}))
                

@app.route("/water")
def waterBottle():
    # contador de agua
    # meta diaria
    # botao para tomar agua
    # cicla entre imagens de uma garrafa de agua
    # form com botao para tomar uma medida de agua definida pelo usuario
    return error("TODO WATER")


'''
TABLES
CREATE TABLE users(
  id INT PRIMARY KEY NOT NULL,
  username STRING NOT NULL,
  hash STRING NOT NULL  
);
CREATE TABLE todo(
  id INT PRIMARY KEY NOT NULL,
  user_id INT NOT NULL,
  todo_text STRING NOT NULL,
  iscomplete INT NOT NULL,
  FOREIGN KEY(user_id) REFERENCES users (id)
);

'''
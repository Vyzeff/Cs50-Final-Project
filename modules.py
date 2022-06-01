from flask import Blueprint, render_template
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, MetaData
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import declarative_base, sessionmaker


modules = Blueprint("modules", __name__, static_folder="static", template_folder="templates")

## Creates engine for SQLAlchemy
engine = create_engine("sqlite+pysqlite:///homebook.db", echo=True, future=True, connect_args={'check_same_thread': False})


#SQLAlchemy
## Orm SQLAlchemy stuff
metadata_obj = MetaData()
base = declarative_base()

## If Database isn't present, create one
if not database_exists(engine.url):
    create_database(engine.url)



base.metadata.create_all(engine)


sqlASession = sessionmaker(bind=engine)
sqlSession = sqlASession()

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

def sqlGetUser (user, action=0):
    
    if action == 0:
        query = sqlSession.query(Users).filter_by(username=user)
    elif action == 1:
        query = sqlSession.query(Users).filter_by(username=user).first()
    elif action == 2:
        query = sqlSession.query(Users).filter_by(username=user).count()
    return query

def sqlCreateUser(username, hash):
    
    newUser = Users(username=username, hash=hash)
    sqlSession.add(newUser)
    sqlSession.commit()

def sqlGetTodo (todoId, action=0):
    
    if action == 0:
        query = sqlSession.query(Todo).filter_by(user_id=todoId)
    elif action == 1:
        query = sqlSession.query(Todo).filter_by(user_id=todoId).first()
    elif action == 2:
        query = sqlSession.query(Todo).filter_by(user_id=todoId).count()
    return query

def sqlCreateTodo(id, text, nowDate):
    newTodo = Todo(user_id=id, todo_text=text, date=nowDate, iscomplete=0)
    sqlSession.add(newTodo) 
    # commit values to database
    sqlSession.commit()
    
def sqlChangeTodo(todoId, action):
    
    todoChange = sqlSession.query(Todo).filter_by(id=todoId).first()
    if action == 0:
        todoChange.iscomplete = 1
        sqlSession.commit()
    if action == 1:
        sqlSession.delete(todoChange)
        sqlSession.commit()

    sqlSession.commit()

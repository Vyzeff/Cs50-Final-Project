from flask import Blueprint, session
from models import ChangeTodo, CreateTodo, GetTodo


from datetime import datetime
from helpers import error

todo = Blueprint("todo", __name__, static_folder="static", template_folder="templates")

def todoVerify():
    if GetTodo(session["user_id"], 1) == None:
        return None 
    return GetTodo(session["user_id"])


def todoUpdate(todoId, action):
    """
    pagina de checklists.
    é nela onde se deleta e faz o update dos todos ja existentes
    redireciona para outra rota para criar todos
    """
    if action == 1:
        ChangeTodo(todoId["input"], 0)

    if action == 2:        
        ChangeTodo(todoId["input"], 1)
        
    return error("TODO TODOS")

def todoCreate(formInput):
    """
    generates todos with fetch from input in javascript
    """  
    # create a session with the input values
    nowDate = str(datetime.now())
        
    CreateTodo(session["user_id"], formInput["input"], nowDate)
        
    
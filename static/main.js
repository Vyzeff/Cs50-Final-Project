function firstCreate() {
    //remove div that is telling user to create
    document.getElementById("removable").remove();

    document.getElementById("2removable").remove();

    var newForm = document.createElement("form");
    newForm.setAttribute("id","todoForm");
    newForm.setAttribute("action","/todo");
    newForm.setAttribute("method","post");
    document.getElementById("first").appendChild(newForm);

    //create new input for creating other lists
    var newInput = document.createElement("input");

    newInput.classList.add("mx-auto", "w-auto", "center");
    newInput.setAttribute("id", "todoInput");
    newInput.setAttribute("autocomplete", "off");
    newInput.setAttribute("placeholder", "Your To-Do");
    newInput.setAttribute("name", "todoInput");

    //insert input on main
    newForm.appendChild(newInput);

    newUl = document.createElement("ul");
    newUl.classList.add("mx-auto", "w-auto", "center");
    newUl.setAttribute("id", "todoList");
    newForm.appendChild(newUl);

    newSmall = document.createElement("small")
    newSmall.innerText = "Left Click to complete, Right click to delete"
    newSmall.classList.add("mx-auto", "w-auto", "center");
    newUl.appendChild(newSmall);

    const form = document.getElementById("todoForm");

    form.addEventListener("submit", todoChange())
}

function todoChange() {
    const input = document.getElementById("todoInput");
    const todoTxt = input.value;

    if (todoTxt) {
        const todoElement = document.createElement("li")
        todoElement.classList.add("center", "todoElement")
        todoElement.innerText = todoTxt
        document.getElementById("todoList").appendChild(todoElement)

        todoElement.addEventListener('click', () => {
            todoElement.classList.toggle("completed")
        })

        todoElement.addEventListener("contextmenu", (e) => {
            e.preventDefault()

            todoElement.remove()
        })
    } 
}



let switches = document.getElementsByClassName("switch");
let style = localStorage.getItem('style');

if (style == null) {
    setTheme('basic');
  } else {
    setTheme(style);
  }


for (let x of switches) {
    x.addEventListener('click', function () {
        let theme = this.dataset.theme;
        setTheme(theme);
    });
  }
  
  function setTheme(theme) {
    if (theme == 'basic') {
      document.getElementById('switcher-id').href = './static/basic.css';
    } else if (theme == 'cold') {
      document.getElementById('switcher-id').href = './static/cold.css';
    } else if (theme == 'contrast') {
      document.getElementById('switcher-id').href = './static/contrast.css';
    } else if (theme == 'sakura') {
        document.getElementById('switcher-id').href = './static/sakura.css';
    } else if (theme == 'lofi') {
      document.getElementById('switcher-id').href = './static/lofi.css';
    }
    localStorage.setItem('style', theme);
}
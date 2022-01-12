from flask import Flask,render_template,redirect,url_for,request
from flask_sqlalchemy import SQLAlchemy

#Db bağlama
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/w10/OneDrive - IZU/Masaüstü/Projects/Flask-TodoApp/todo.db'
db = SQLAlchemy(app)

@app.route("/")
def index():
    todos = Todo.query.all()
    return render_template("index.html" ,todos = todos)



@app.route("/add",methods=["POST"]) 
def addTodo():
    title = request.form.get("title")
    newTodo = Todo(title = title,complete = False)
    db.session.add(newTodo)#database ekle
    db.session.commit()#databasede değişiklik olduğu için

    return redirect(url_for("index"))

@app.route("/complete/<string:id>")
def completeTodo(id):
    todo = Todo.query.filter_by(id = id).first()
    """
    if todo.complete == True:
        todo.complete = False
    else:
        todo.complete = True
    """
    todo.complete = not todo.complete #true ise flase or false ise true olacak.

    db.session.commit()
    return redirect(url_for("index"))


@app.route("/delete/<string:id>")
def deleteTodo(id):
    todo = Todo.query.filter_by(id = id).first()
    db.session.delete(todo) 
    db.session.commit()
    return redirect(url_for("index"))


#Database
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    complete = db.Column(db.Boolean)

if __name__== "__main__": #server ayağa kaldırılıyor
    db.create_all()
    app.run(debug=True)

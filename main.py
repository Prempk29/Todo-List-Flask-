from flask import Flask, render_template,request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///site.db'
db=SQLAlchemy(app)

class List(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    todo= db.Column(db.String(500),nullable=False)
    
    def __repr__(self):
        return f"List('{self.todo}')"
    
@app.route("/")
@app.route("/home",methods=["GET","POST"])
def home():
    if request.method=="POST":
        item=request.form.get("todolist")
        listitem=List(todo=item)
        db.session.add(listitem)
        db.session.commit()    
    k=List.query.all() 
    return render_template("todolist.html",k=k)
@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    todo=List.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("home"))

@app.route("/update/<int:todo_id>",methods=["GET","POST"])
def update(todo_id):
    todo=List.query.filter_by(id=todo_id).first()
    if request.method=="POST":
        updated=request.form.get("updated")
        todo.todo=updated
        db.session.add(todo)
        db.session.commit()
        return redirect(url_for("home"))        
    return render_template("update.html",todo=todo)
    

if __name__=="__main__":
    app.run(port=7172,debug=True)


from flask import Flask ,render_template,request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///test.db"
db = SQLAlchemy(app)
class Todo(db.Model):
    id = db.Column(db.Integer,primary_key= True)
    content = db.Column(db.String(200),nullable=False)
    Date_created = db.Column(db.DateTime, default= datetime.utcnow)
    def __repr__(self):
        return "<task %r>" % self.id

 # Crud Op
@app.route("/",methods = ['POST','GET'])
def index():
    if request.method == "POST":
        task_content =request.form['content']
        new_task = Todo(content = task_content)
        try:
           db.session.add(new_task)
           db.session.commit() 
           return redirect('/')
        except:
            return 'There was an issue'
    else:
        tasks = Todo.query.order_by(Todo.Date_created),all()
        return render_template('index.html',tasks = tasks)
    
@app.route("/delete/<int:id>")
def delete(id):
    task_to_del = Todo.query.get_or_404(id)
    try:
        db.session.delete(task_to_del)
        db.session.commit()
        return redirect('/')
    except:
        return "there was a problem deteing that task"


@app.route("/update/<int:id>",methods= ['GET','POST'])
def update(id):
    task_to_update = Todo.query.get_or_404(id)
    if request.method == 'POST':
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')    
        except:
            pass

    else:
        return render_template('update.html',task = task_to_update)



if __name__ == "__main__":
    app.run(debug=True)
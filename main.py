from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
import pymysql

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blog:blog@localhost:8889/blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class BlogEntry(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    entry = db.Column(db.String(1000))
    #completed = db.Column(db.Boolean)

    def __init__(self, title, entry):
        self.title = title
        self.entry = entry
        #self.completed = False


@app.route('/add_a_new_post', methods=['POST'])
def add_a_new_post():

        if request.method == 'POST':
            entry_title = request.form['title']
            entry_text  = request.form['entry']
            new_post = BlogEntry(entry_title, entry_text)
            db.session.add(new_post)
            db.session.commit()

        return(render_template('add_a_new_post.html',title="Add a New Post"))



@app.route('/', methods=['POST', 'GET'])
def index():


    blogs = BlogEntry.query.all()
    #tasks = Task.query.filter_by(completed=False).all()
    #completed_tasks = Task.query.filter_by(completed=True).all()
    return render_template(
        blogs=blogs) #completed_tasks=completed_tasks)


# @app.route('/delete-task', methods=['POST'])
# def delete_task():
#
#     task_id = int(request.form['task-id'])
#     task = Task.query.get(task_id)
#     task.completed = True
#     db.session.add(task)
#     db.session.commit()
#
#     return redirect('/')

@app.route("/updatedb")
def update_DB():
    db.drop_all()
    db.create_all()
    return "updated db"
    #return redirect("/")

if __name__ == '__main__':
    #db.drop_all()
    #db.create_all()
    app.run()

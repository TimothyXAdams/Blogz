from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:build-a-blog@localhost:8889/build-a-blog'
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


@app.route('/', methods=['POST', 'GET'])
def index():

    if request.method == 'POST':
        entry_title = request.form['title']
        entry_text  = request.form['text']
        new_post = BlogEntry(entry_title, entry_text)
        db.session.add(new_post)
        db.session.commit()

    blogs = BlogEntry.query.all()
    #tasks = Task.query.filter_by(completed=False).all()
    #completed_tasks = Task.query.filter_by(completed=True).all()
    return render_template('add_a_new_post.html',title="Add a New Post",
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


if __name__ == '__main__':
app.run()

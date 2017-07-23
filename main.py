from flask import Flask, request, redirect, render_template, flash, session
from flask_sqlalchemy import SQLAlchemy
#import pymysql

app = Flask(__name__)
app.config['DEBUG'] = True
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:blogz@localhost:8889/blogz'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:blogz@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'hxixjx'


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    entry = db.Column(db.String(255))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, entry, owner):
        self.title = title
        self.entry = entry
        self.owner = owner

    def is_valid(self):
        if self.title and self.entry :
            return True
        else:
            return False


class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=False)
    password = db.Column(db.String(20))
    blogs = db.relationship('Blog', backref='owner')

    def __init__(self, username, password):
        self.username = username
        self.password = password


# class blog_entry(db.Model):
#         id = db.Column(db.Integer, primary_key=True)

@app.before_request
def require_login():
    allowed_routes = ['login', 'show_blogs', 'index', 'signup', 'updatedb', 'chkform']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')


@app.route('/add_a_new_post', methods=['POST', 'GET'])
def add_a_new_post():

        if request.method == 'POST':
            entry_title = request.form['title']
            entry_text  = request.form['entry']
            new_post = Blog(entry_title, entry_text, owner)

            if new_post.is_valid() == True:
                db.session.add(new_post)
                db.session.commit()
                url = "/blog?id=" + str(new_post.id)
                return redirect(url)
            else: #if the validation came up False
                flash("Error. Your blog entry requires a title and a text.")
                return render_template('add_a_new_post.html', title="Enter your blog here.", entry_title=entry_title, entry_text=entry_text)

        else: #it was a GET request, not a POST
            return render_template('add_a_new_post.html',title="Add a New Post")




@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template("index.html")
    #return redirect("/blog")


@app.route("/blog")
def show_blogs():

    blog_id = request.args.get('id')
    if blog_id: #if the blog isn't empty
        blog = Blog.query.get(blog_id)
        if blog:
        # return str(blog.title) + str(blog.entry)
            return render_template('blog.html', title=blog.title, blog=blog)
        else:
            flash("Invalid Blog ID")

    blogs = Blog.query.all()
    return render_template('all_blogs.html', title="entry_title", blogs=blogs) #completed_tasks=completed_tasks)


@app.route("/updatedb") #Initialize database
def updatedb():
    print("entering updatedb")
    db.drop_all()
    db.create_all()
    # testuser = User("Tim", "password")
    # testpost = Blog("A Blog Post", "This is the content", testuser)
    # db.session.add(testuser)
    # db.session.add(testpost)
    # db.session.commit()
    print("exiting updatedb")
    return redirect("/")



@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            session['username'] = username
            flash("Logged in")
            return redirect('/')
        else:
            if not user:
                flash('Username does not exist', 'error')
                #if not user, don't bother checking password
                #return render_template('login.html')
            if user.password != password:
                flash('Incorrect password', 'error')
                #return render_template('login.html')
    return render_template('login.html') #Fallthrough, or User arrived with GET request



@app.route("/signup")
def signup():

    return render_template('signup.html')


#Check username and password
@app.route("/chkform", methods=['POST'])
def chkform():
    username_error = "" #initialize error as empty string
    password_error = ""
    chkpwd_error   = ""
    email_error    = ""

    username = request.form["username"]
    if len(username) <3 or len(username) > 20:
    	username_error = "You must enter a valid user name"

    password  =request.form["password"]
    if len(password) <3 or len(password) > 20:
    	password_error = "Invalid password"

    chkpwd = request.form["chkpwd"]
    if chkpwd != password:
    	chkpwd_error = "Password mismatch"

    # emailaddr = request.form["emailaddr"]
    # if emailaddr: #If it's not empty, since it's optional
    #     if " " in emailaddr:
    #         email_error = "Email cannot contain spaces"
    #     if len(emailaddr) < 3 or len(emailaddr) >20:
    #         email_error = "Email must be 3 - 20 characters"
    #     if "@" not in emailaddr or "." not in emailaddr:
    #         email_error = "Make sure email address is valid"

    if username_error or password_error or chkpwd_error or email_error:
        return render_template("signup.html", username_error=username_error, password_error=password_error, chkpwd_error=chkpwd_error, email_error=email_error, username=username, password=password, emailaddr=emailaddr)
    else:
        new_user = User(username, password)
        db.session.add(new_user)
        db.session.commit()
        session['new_user.username'] = username

        return render_template("all_blogs.html", username=username)




@app.route("/logout", methods=['POST'])
def logout():
    '''
    Logout function handles a POST request to /logout and redirects the user to /blog after deleting the username from the session.
    '''
    del session['username']
    return redirect('/blog')


if __name__ == '__main__':
    #db.drop_all()
    #db.create_all()
    app.run()

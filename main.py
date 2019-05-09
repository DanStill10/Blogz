from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from helpers import user_name_check, password_check, confirm_password_check

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:Soniccolors1@localhost:3306/blogz'
app.config['SQLALCHEMY_ECHO'] = True
app.secret_key ='Nidazhongwoujeweishihoa'
db = SQLAlchemy(app)

class User(db.Model):

    id = db.Column(db.Integer, primary_key= True)
    username = db.Column(db.String(50), unique = True)
    password = db.Column(db.String(60))
    blogs = db.relationship('Blog', backref='user')

    def __init__(self, username, password):
        self.username = username
        self.password = password

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(40))
    content = db.Column(db.String(600))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    def __init__(self, title, content, user_id):
        self.title = title
        self.content = content
        self.user_id = user_id

def check_fields(entry):
    if entry == "":
        return "field may not be empty!" 
    return ''

@app.before_request
def need_login():
    locked_routes = ['logout','newpost']
    if request.endpoint in locked_routes and 'username' not in session:
        return redirect('/login')

@app.route('/', methods = ['POST', 'GET'])
def home():
    all_users = User.query.all()
    return render_template('home.html', all_users = all_users, username = session.get('username', ''))
        

@app.route('/login', methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username = username).first()
        if user and user.password == password:
            session['username'] = username
            session['user_id'] = user.id
            return redirect('/newpost')
        else:
            login_error = 'The username or password you submitted is incorrect!'
            return render_template('login.html', login_error = login_error, username = session.get('username', ''))
    return render_template('login.html', username = session.get('username', ''))

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/signup', methods = ['POST', 'GET'])
def signup():
    if request.method == 'POST': 
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        password_error = password_check(password)
        confirm_password_error = confirm_password_check(confirm_password, password)
        user_name_error = user_name_check(username)
        errors = [user_name_error, confirm_password_error, password_error]
        for error in errors:
            if error != "":
               return render_template('signup.html',user_name_error = user_name_error, confirm_password_error = confirm_password_error, password_error = password_error, username = session.get('username', ''))
        
        existing_user = User.query.filter_by( username = username).first()
        if not existing_user:
            new_user = User(username,password)
            db.session.add(new_user)
            db.session.commit()
            return redirect('/newpost')
        else:
            user_name_error = 'Unable to create your account, that username is already in use!'
            return render_template('signup.html', user_name_error = user_name_error, username = session.get('username', ''))
    return render_template('signup.html', username = session.get('username', ''))

@app.route('/blog', methods = ['POST','GET'])
def blog():
    request_check = request.args.get('id')
    if request_check != None :
        blog = Blog.query.get(request_check)
        blog_title = blog.title
        blog_content = blog.content
        blog_username = blog.user.username
        return render_template('single_post.html', blog_username = blog_username, blog_title = blog_title, blog_content = blog_content, username = session.get('username', ''))
    user_check = request.args.get('username')
    if user_check != None:
        user = User.query.filter_by( username = user_check).first()
        blogs = Blog.query.filter_by(user_id = user.id).all()
        return render_template('single_user.html', all_blogs = blogs, user = user.username, username = session.get('username', ''))
    all_blogs = Blog.query.all()
    return render_template('blog.html', all_blogs = all_blogs, username = session.get('username', ''))


@app.route('/newpost', methods = ['POST','GET'])
def newpost():
    if request.method == 'POST':
        title = request.form['post_title']
        content = request.form['post_content']
        user_id = session['user_id']
        title_check = check_fields(title)
        content_check = check_fields(content)
        errors = [title_check, content_check]
        for error in errors:
            if error != '':
                return render_template('new_post.html', error1 = title_check, error2 = content_check, username = session.get('username', '')) 
        new_post = Blog(title,content, user_id)
        db.session.add(new_post)
        db.session.commit()
        db.session.flush()
        blog_id = new_post.id
        return redirect('/blog?id=' + str(blog_id))
    return render_template('new_post.html', username = session.get('username', ''))







if __name__ == "__main__":
    app.run()
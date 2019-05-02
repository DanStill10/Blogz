from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:Soniccolors1@localhost:3306/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(40))
    content = db.Column(db.String(600))

    def __init__(self, title, content):
        self.title = title
        self.content = content

def check_fields(entry):
    if entry == "":
        return "field may not be empty!" 
    return ''

@app.route('/blog', methods = ['POST','GET'])
def home():
    request_check = request.args.get('id')
    if request_check != None :
        blog = Blog.query.get(request_check)
        blog_title = blog.title
        blog_content = blog.content
        return render_template('single_post.html', blog_title = blog_title, blog_content = blog_content)
    all_blogs = Blog.query.all()
    return render_template('blog.html', all_blogs = all_blogs)


@app.route('/new_post', methods = ['POST','GET'])
def create_a_post():
    if request.method == 'POST':
        title = request.form['post_title']
        content = request.form['post_content']
        title_check = check_fields(title)
        content_check = check_fields(content)
        errors = [title_check, content_check]
        for error in errors:
            if error != '':
                return render_template('new_post.html', error1 = title_check, error2 = content_check) 
        new_post = Blog(title,content)
        db.session.add(new_post)
        db.session.commit()
        db.session.flush()
        blog_id = new_post.id
        return redirect('/blog?id=' + str(blog_id))
    return render_template('new_post.html')







if __name__ == "__main__":
    app.run()
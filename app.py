from flask import Flask, render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_moment import Moment

app = Flask(__name__)
moment = Moment(app)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy(app)

class BlogPost(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    title = db.Column(db.String(100),nullable = False)
    body = db.Column(db.Text,nullable = False)
    author = db.Column(db.String(40),nullable = False, default = "Admin")
    created_at = db.Column(db.DateTime,nullable = False, default=datetime.utcnow)

    def __repr__(self):
        return 'Blog Post' + str(self.id)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/posts', methods=['GET'])
def all_posts():

    posts = BlogPost.query.all()
    return render_template('post.html',posts = posts)

@app.route('/post/delete/<int:id>')
def delete(id):
    post = BlogPost.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return redirect('/posts')

@app.route('/post/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    
    post = BlogPost.query.get_or_404(id)

    if request.method == 'POST':
        post.title = request.form['title']
        post.author = request.form['author']
        post.content = request.form['body']
        db.session.commit()
        return redirect('/posts')
    else:
        return render_template('edit.html', post=post)

@app.route('/post/new', methods=['GET', 'POST'])
def new_post():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        body = request.form['body']
        new_post = BlogPost(title=title, body=body, author=author)
        db.session.add(new_post)
        db.session.commit()
        return redirect('/posts')
    else:
        return render_template('new.html')

if __name__ == "__main__":
    app.run(debug=True)

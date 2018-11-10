from flask import Flask,render_template,url_for,flash,redirect
from forms import RegisterForm,LoginForm
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config['SECRET_KEY'] = 'aafa779f428333e6c6135430e70205d0'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(30),unique=True,nullable=False)
    password = db.Column(db.String(50),nullable=False)
    email = db.Column(db.String(100),unique=True,nullable=False)
    image_file = db.Column(db.String(50),default='default.jpg')
    posts = db.relationship('Post',backref='author',lazy=True)

    def __repr__(self):
        return f"User('{self.username}','{self.email}','{self.image_file}')"

class Post(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(100),nullable=False)
    content = db.Column(db.String(500),nullable=False)
    post_date = db.Column(db.Date,nullable=False,default=datetime.utcnow)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)

    def __repr__(self):
        return f"Post('{self.title}','{self.content}','{self.post_date}')"

datas = [
    {
        'title':'data1',
        'author':'John',
        'date':'2018/10/27',
        'content':'content1'
    },
    {
        'title':'data2',
        'author':'ryan',
        'date':'2018/10/27',
        'content':'content2'
    }
]

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html',posts=datas,title='home')

@app.route("/about")
def about():
    return render_template('about.html',title='about')

@app.route("/register" , methods=('GET','POST'))
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        flash(message='registered for '+ form.username.data,category='success')
        return redirect(url_for('home'))
    return render_template('register.html',title='register',form=form)

@app.route("/login" , methods=('GET','POST'))
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'jx830927@gmail.com' and form.password.data == 'aaa123aaa':
            flash('log in','success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html',title='login',form=form)

if __name__ == '__main__':
    app.run(debug=True)

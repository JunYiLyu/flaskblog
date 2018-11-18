from flaskblog import app,db,bcrypt
from flask import render_template,url_for,flash,redirect,request
from flaskblog.forms import RegisterForm,LoginForm
from flaskblog.models import User,Post
from flask_login import login_user,current_user,logout_user,login_required

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
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data,
                    email=form.email.data,
                    password=bcrypt.generate_password_hash(form.password.data).decode('utf-8'))
        db.session.add(user)
        db.session.commit()
        flash(message='registered for '+ form.username.data,category='success')
        return redirect(url_for('login'))

    return render_template('register.html',title='register',form=form)

@app.route("/login" , methods=('GET','POST'))
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user) # current_user = user
            flash('log in','success')
            next = request.args.get('next') #/login?next=%2Faccount, args is dictionary, next =/account
            return redirect(next) if next else redirect(url_for('home')) #ternary contion
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html',title='login',form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/account')
@login_required #__init___ login_manager.login_view = 'login'
def account():
    return render_template('account.html',title='login')

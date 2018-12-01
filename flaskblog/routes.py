from flaskblog import app,db,bcrypt
from flask import render_template,url_for,flash,redirect,request,abort
from flaskblog.forms import RegisterForm,LoginForm,UpdateAccountForm,CreatePostForm
from flaskblog.models import User,Post
from flask_login import login_user,current_user,logout_user,login_required
import secrets,os
from PIL import Image


@app.route("/")
@app.route("/home")
def home():
    posts = Post.query.all()
    return render_template('home.html',posts=posts,title='home')

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

def save_picture(picture):
    random_hex = secrets.token_hex(8)
    filename = random_hex + '-' + picture.filename
    path = os.path.join(app.root_path,'static/pictures',filename)
    image = Image.open(picture)
    image.thumbnail([200,200])
    image.save(path)
    return filename

@app.route('/account',methods=['GET','POST'])
@login_required #__init___ login_manager.login_view = 'login'
def account():
    pic = url_for('static',filename = 'pictures/' + current_user.image_file)
    form = UpdateAccountForm()

    if form.validate_on_submit():
        flash('Update Sucessfully','success')
        current_user.username = form.username.data
        current_user.email = form.email.data
        if form.picture.data:
            filename = save_picture(form.picture.data)
            current_user.image_file = filename
        db.session.commit()
        return redirect(url_for('account'))

    return render_template('account.html',title='account',pic=pic,form=form)

@app.route('/home/new',methods=['GET','POST'])
@login_required
def create_post():
    form = CreatePostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data,content=form.content.data,user_id=current_user.id)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('create_post.html',title='Create Post',form=form)

@app.route('/home/post/<int:post_id>',methods=['GET','POST'])
@login_required
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html',post=post)

@app.route('/home/post/<int:post_id>/update',methods=['GET','POST'])
@login_required
def update_post(post_id):
    form = CreatePostForm()
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    if form.validate_on_submit():
        post.title = form.title.data
        post.content =form.content.data
        db.session.commit()
        return redirect(url_for('post',post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html',title='Create Post',form=form)

@app.route('/home/post/<int:post_id>/delete',methods=['GET','POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('home'))

from flask import Flask,render_template,url_for,flash,redirect
from forms import RegisterForm,LoginForm

app = Flask(__name__)

app.config['SECRET_KEY'] = 'aafa779f428333e6c6135430e70205d0'

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

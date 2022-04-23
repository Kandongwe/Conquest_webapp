from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import pymysql
# from secret import dbhost, dbuser, dbname, dbpass

# instanstiating the app object
app = Flask(__name__)
app.config['SECRET_KEY'] = "Thisisasecretkey"
app.config['SQLALCHEMY_DATABASE_URI'] =("mysql+pymysql://{0}:{1}@{2}/{3}".format('kandongwe', 'grace123', '127.0.0.1:3306', 'csc420db'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

bootstrap = Bootstrap(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Creation of user Models to be user in the  database
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(200))
    
    def __repr__(self):
        return f'Model {self.model}'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Forms creation section beings here
class signUpForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('Remember me')

# Forms creation section ends here


# Route creation beings here
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    msg = None
    msg1 = None
    form = signUpForm()
    if form.validate_on_submit():
        username_exists = db.session.query(db.exists().where(User.username == form.username.data)).scalar()
        email_exists = db.session.query(db.exists().where(User.email == form.email.data)).scalar()
        if username_exists:
            msg = " Username invalid "
            if email_exists:
                msg1 = " Email invalid "

        elif email_exists:
            msg1 = "  Email invalid "
            if username_exists:
                msg = " Username invalid "

        else:
            hashed_password = generate_password_hash(form.password.data, method='sha256')
            new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()

            return redirect('/login')


    return render_template('signup.html', form=form, msg=msg, msg1=msg1)


@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    user = User.query.filter_by(username=form.username.data).first()
    msg = None
    msg1 = None
    if form.validate_on_submit():
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect('/main')
            else:
                msg = "Incorrect pasword !"
                return render_template('login.html', form=form, msg=msg)
                
        else:
            msg1 = "Incorrect username !"
            return render_template('login.html', form=form, msg1=msg1)

    return render_template('login.html', form=form)


@app.route('/meditation')
def meditation():
    return render_template('meditation.html')


@app.route('/study')
def study():
    return render_template('study.html')


@app.route('/journal')
def journal():
    return render_template('journal.html')
@app.route('/main')
@login_required
def main():
    return render_template('main.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('index.html')

# Route creation ends here

if __name__ == '__main__':
    app.run(debug=True)


import os

from flask import Flask, render_template, request

# import flask connector to connect to mysql database
import mysql.connector

# create a database variable for the local database
mydb = mysql.connector.connect(host='localhost', user='csc420', password='grace123', database='csc420db', auth_plugin="mysql_native_password")
cursor = mydb.cursor()

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass


    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/signup', methods=['POST', 'GET'])
    def signup():
        error = None
        msg = None
        if request.method == 'POST':
            uname = request.form.get('uname')
            username = request.form.get('username')
            password = request.form.get('pass')
            password2 = request.form.get('pass2')

            if len(uname) < 4:
                error = "Your name looks invalid"

            elif len(username) < 6:
                error = "Your username should have atleast 6 characters"

            elif len(password) < 6:
                error = "Your password should be atleast 6 characters long"

            elif password != password2:
                error = "Password not matched"

            else:
                query = "INSERT INTO csc420db.users(PersonID, PersonName, UserName, Password, date) VALUES (NULL, %s, %s, %s, NOW() )"
                cursor.execute(query, (uname, username, password))
                mydb.commit()
                msg = "Your account was successfully created you can now login to your account"

        return render_template('signup.html', error=error, msg=msg)


    @app.route('/login')
    def login():
        return render_template('login.html')

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
    def main():
        return render_template('main.html')

    return app


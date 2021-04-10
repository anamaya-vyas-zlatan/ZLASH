from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators,IntegerField,ValidationError,DateField, SubmitField
from passlib.hash import sha256_crypt
from functools import wraps
import mysql.connector
from flask_simplelogin import is_logged_in
# from werkzeug import secure_filename
# from werkzeug.utils import secure_filename
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage

import pandas as pd
from alpha_vantage.timeseries import TimeSeries
import time

import yfinance as yf

app = Flask(__name__)


app.config['MYSQL_HOST'] = 'remotemysql.com'
app.config['MYSQL_USER'] = 'hIFfyMbx3a'
app.config['MYSQL_PASSWORD'] = 'KOkXiSAEiR'
app.config['MYSQL_DB'] = 'hIFfyMbx3a'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'




mysql = MySQL(app)


# home page
@app.route('/')
def index():
    return render_template('homepage.html')


@app.route('/home')
def homepge():
    return render_template('home.html')






class ContactForm(Form):
    Name = StringField('Name', [validators.Length(min=1, max=30)])
    Phone_Number = IntegerField('Phone Number')
    Email = StringField('Email')
    Subject = StringField('Subject', [validators.Length(min=1, max=100)])
    Issue = TextAreaField('Issue', [validators.Length(min=30)])


# contactus page route
@app.route('/contactus', methods=['GET', 'POST'])
def contactus():
    form = ContactForm(request.form)
    if request.method == 'POST' and form.validate():
        Name = form.Name.data
        Phone_Number = form.Phone_Number.data
        Email = form.Email.data
        Subject = form.Subject.data
        Issue = form.Issue.data

        cur = mysql.connection.cursor()

        cur.execute("INSERT INTO cous(Name, Phone_Number, Email, Subject, Issue) VALUES(%s, %s, %s, %s, %s)",
                    (Name, Phone_Number, Email, Subject, Issue))

        mysql.connection.commit()

        cur.close()



        return redirect(url_for('contactus'))
    return render_template('contactus.html', form=form)


# about page
@app.route('/about')
def about():
    return render_template('about.html')


class RegisterForm(Form):
    First_Name = StringField('First_Name')
    Last_Name = StringField('Last_Name')
    Email = StringField('Email')
    Phone_Number = IntegerField('Phone_Number')
    DOB = DateField('DOB', format='%Y-%m-%d')
    Username = StringField('Username')
    Password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('confirm Password')


# register entrepreneur page route
@app.route('/register_et', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        First_Name = form.First_Name.data
        Last_Name = form.Last_Name.data
        Email = form.Email.data
        Phone_Number = form.Phone_Number.data
        DOB = form.DOB.data
        Username = form.Username.data
        Password = sha256_crypt.encrypt(str(form.Password.data))

        cur = mysql.connection.cursor()

        cur.execute(
            "INSERT INTO et(First_Name, Last_Name, Email, Phone_Number, DOB, Username, Password) VALUES(%s, %s, %s, %s, %s, %s, %s)",
            (First_Name, Last_Name, Email, Phone_Number, DOB, Username, Password))

        mysql.connection.commit()

        cur.close()

        flash('You are now registered and can log in ')

        return redirect(url_for('login_et'))
    return render_template('register_et.html', form=form)


# register investor page route
@app.route('/register_iv', methods=['GET', 'POST'])
def registeriv():  # this is being called in url_for
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        First_Name = form.First_Name.data
        Last_Name = form.Last_Name.data
        Email = form.Email.data
        Phone_Number = form.Phone_Number.data
        DOB = form.DOB.data
        Username = form.Username.data
        Password = sha256_crypt.encrypt(str(form.Password.data))

        cur = mysql.connection.cursor()

        cur.execute(
            "INSERT INTO iv(First_Name, Last_Name, Email, Phone_Number, DOB, Username, Password) VALUES(%s, %s, %s, %s, %s, %s, %s)",
            (First_Name, Last_Name, Email, Phone_Number, DOB, Username, Password))

        mysql.connection.commit()

        cur.close()

        flash('You are now registered and can log in ', 'success')

        return redirect(url_for('login_iv'))
    return render_template('register_iv.html', form=form)


# register public page route
@app.route('/register_pe', methods=['GET', 'POST'])
def registerpe():  # this is being called in url_for
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        First_Name = form.First_Name.data
        Last_Name = form.Last_Name.data
        Email = form.Email.data
        Phone_Number = form.Phone_Number.data
        DOB = form.DOB.data
        Username = form.Username.data
        Password = sha256_crypt.encrypt(str(form.Password.data))

        cur = mysql.connection.cursor()

        cur.execute(
            "INSERT INTO pe(First_Name, Last_Name, Email, Phone_Number, DOB, Username, Password) VALUES(%s, %s, %s, %s, %s, %s, %s)",
            (First_Name, Last_Name, Email, Phone_Number, DOB, Username, Password))

        mysql.connection.commit()

        cur.close()

        flash('You are now registered and can log in ')

        return redirect(url_for('registerpe'))
    return render_template('register_pe.html', form=form)

@app.route('/login_et', methods=['GET', 'POST'])
def login_et():
    if request.method == 'POST':
        # Get Form Fields
        username = request.form['username']
        password_candidate = request.form['password']

        # Create cursor
        cur = mysql.connection.cursor()

        # Get user by username
        result = cur.execute("SELECT * FROM et WHERE username = %s", [username])

        if result > 0:
            # Get stored hash
            data = cur.fetchone()
            password = data['Password']

            # Compare Passwords
            if sha256_crypt.verify(password_candidate, password):
                # Passed
                session['logged_in_et'] = True
                session['username'] = username

                flash('You are now logged in')
                return redirect(url_for('dashboard_et'))
            else:
                error = 'Invalid login'
                return render_template('login_et.html', error=error)
            # Close connection
            cur.close()
        else:
            error = 'Username not found'
            return render_template('login_et.html', error=error)

    return render_template('login_et.html')



@app.route('/login_iv', methods=['GET', 'POST'])
def login_iv():
    if request.method == 'POST':
        # Get Form Fields
        username = request.form['username']
        password_candidate = request.form['password']

        # Create cursor
        cur = mysql.connection.cursor()

        # Get user by username
        result = cur.execute("SELECT * FROM iv WHERE username = %s", [username])

        if result > 0:
            # Get stored hash
            data = cur.fetchone()
            password = data['Password']

            # Compare Passwords
            if sha256_crypt.verify(password_candidate, password):
                # Passed
                session['logged_in_iv'] = True
                session['username'] = username

                flash('You are now logged in')
                return redirect(url_for('dashboard_iv'))
            else:
                error = 'Invalid login'
                return render_template('login_iv.html', error=error)
            # Close connection
            cur.close()
        else:
            error = 'Username not found'
            return render_template('login_iv.html', error=error)

    return render_template('login_iv.html')



@app.route('/login_pe', methods=['GET', 'POST'])
def login_pe():
    if request.method == 'POST':
        # Get Form Fields
        username = request.form['username']
        password_candidate = request.form['password']

        # Create cursor
        cur = mysql.connection.cursor()

        # Get user by username
        result = cur.execute("SELECT * FROM pe WHERE username = %s", [username])

        if result > 0:
            # Get stored hash
            data = cur.fetchone()
            password = data['Password']

            # Compare Passwords
            if sha256_crypt.verify(password_candidate, password):
                # Passed
                session['logged_in_pe'] = True
                session['username'] = username

                flash('You are now logged in')
                return redirect(url_for('dashboard_pe'))
            else:
                error = 'Invalid login'
                return render_template('login_pe.html', error=error)
            # Close connection
            cur.close()
        else:
            error = 'Username not found'
            return render_template('login_pe.html', error=error)

    return render_template('login_pe.html')


def is_logged_in_pe(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in_pe' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login', 'danger')
            return redirect(url_for('index'))
    return wrap

# Check if user logged in
def is_logged_in_iv(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in_iv' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login', 'danger')
            return redirect(url_for('index'))
    return wrap

def is_logged_in_et(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in_et' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login', 'danger')
            return redirect(url_for('index'))
    return wrap


@app.route('/logoutpe')
@is_logged_in_pe
def logout_pe():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('index'))

@app.route('/logoutiv')
@is_logged_in_iv
def logout_iv():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('index'))

@app.route('/logoutet')
@is_logged_in_et
def logout_et():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('index'))



# @app.route('/dashboardet')
# def dashboard_et():
#     return render_template('dashboard_et.html')





@app.route('/dashboardet')
def dashboard_et():
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM post where Post_Author like %s order by Post_Id desc", (session['username'],))
    # result = cur.execute("Select * From Postpicture")
    myproblems = cur.fetchall()


    if result > 0:
        return render_template('dashboard_et.html', myproblems=myproblems)
    else:
        msg = 'No problems posted'
        return render_template('dashboard_et.html', msg=msg)
    cur.close()
    return render_template('dashboard_et.html')


@app.route('/dashboardiv')
def dashboard_iv():
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM post order by Post_Id desc")
    myproblems = cur.fetchall()

    if result > 0:
        return render_template('dashboard_iv.html', myproblems=myproblems)
    else:
        msg = 'No problems posted'
        return render_template('dashboard_iv.html', msg=msg)
    cur.close()
    return render_template('dashboard_iv.html')



# @app.route('/dashboardiv')
# def dashboard_iv():
#     return render_template('dashboard_iv.html')


@app.route('/dashboardpe')
def dashboard_pe():
    return render_template('dashboard_pe.html')





class ProblemForm(Form):
    Problem_Type = StringField('Problem_Type', [validators.Length(min=1, max=30)])
    Problem_Subject = StringField('Problem_Subject', [validators.Length(min=1, max=200)])
    Problem_Body = TextAreaField('Problem_Body', [validators.Length(min=30)])
#
@app.route('/postproblem',methods = ['GET', 'POST'])
def addproblem():
    form = ProblemForm(request.form)
    if request.method == 'POST' and form.validate():
        Problem_Type = form.Problem_Type.data
        Problem_Subject = form.Problem_Subject.data
        Problem_Body = form.Problem_Body.data

        cur = mysql.connection.cursor()

        cur.execute("INSERT INTO prob(Problem_Type, Problem_Subject, Problem_Author, Problem_Body) VALUES(%s, %s, %s, %s)", (Problem_Type, Problem_Subject, "anonymous", Problem_Body))

        mysql.connection.commit()

        cur.close()
        return redirect(url_for('addproblem'))

    return render_template('postproblem.html', form =form)



@app.route('/postproblemet',methods = ['GET', 'POST'])
@is_logged_in_et
def addproblemet():
    form = ProblemForm(request.form)
    if request.method == 'POST' and form.validate():
        Problem_Type = form.Problem_Type.data
        Problem_Subject =form.Problem_Subject.data
        Problem_Body = form.Problem_Body.data

        cur = mysql.connection.cursor()

        cur.execute("INSERT INTO prob(Problem_Type, Problem_Subject, Problem_Author, Problem_Body) VALUES(%s, %s, %s, %s)", (Problem_Type, Problem_Subject, session['username'], Problem_Body))

        mysql.connection.commit()

        cur.close()
        return redirect(url_for('addproblemet'))

    return render_template('postproblem.html', form =form)

@app.route('/postproblemiv',methods = ['GET', 'POST'])
@is_logged_in_iv
def addproblemiv():
    form = ProblemForm(request.form)
    if request.method == 'POST' and form.validate():
        Problem_Type = form.Problem_Type.data
        Problem_Subject =form.Problem_Subject.data
        Problem_Body = form.Problem_Body.data

        cur = mysql.connection.cursor()

        cur.execute("INSERT INTO prob(Problem_Type, Problem_Subject, Problem_Author, Problem_Body) VALUES(%s, %s, %s, %s)", (Problem_Type, Problem_Subject, session['username'], Problem_Body))

        mysql.connection.commit()

        cur.close()
        return redirect(url_for('addproblemiv'))

    return render_template('postproblem.html', form =form)

@app.route('/postproblempe',methods = ['GET', 'POST'])
@is_logged_in_pe
def addproblempe():
    form = ProblemForm(request.form)
    if request.method == 'POST' and form.validate():
        Problem_Type = form.Problem_Type.data
        Problem_Subject =form.Problem_Subject.data
        Problem_Body = form.Problem_Body.data

        cur = mysql.connection.cursor()

        cur.execute("INSERT INTO prob(Problem_Type, Problem_Subject, Problem_Author, Problem_Body) VALUES(%s, %s, %s, %s)", (Problem_Type, Problem_Subject, session['username'], Problem_Body))

        mysql.connection.commit()

        cur.close()
        return redirect(url_for('addproblempe'))

    return render_template('postproblem.html', form =form)




@app.route('/'
           ''
           ''
           '')
@is_logged_in_et
def viewmyproblemset():
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM prob where Problem_Author like %s order by Prob_Id desc", (session['username'],))
    myproblems = cur.fetchall()

    if result>0:
        return render_template('viewmyproblems.html', myproblems = myproblems)
    else:
        msg = 'No problems posted'
        return render_template('viewmyproblems.html',msg = msg)
    cur.close()



@app.route('/viewmyproblemsiv')
@is_logged_in_iv
def viewmyproblemsiv():
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM prob where Problem_Author like %s ", (session['username'],))
    myproblems = cur.fetchall()

    if result > 0:
        return render_template('viewmyproblems.html', myproblems = myproblems)
    else:
        msg = 'No problems posted'
        return render_template('viewmyproblems.html',msg = msg)
    cur.close()




@app.route('/viewmyproblemspe')
@is_logged_in_pe
def viewmyproblemspe():
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM prob where Problem_Author like %s order by Prob_Id desc", (session['username'],))
    myproblems = cur.fetchall()

    if result>0:
        return render_template('viewmyproblems.html', myproblems = myproblems)
    else:
        msg = 'No problems posted'
        return render_template('viewmyproblems.html',msg = msg)
    cur.close()



@app.route('/viewproblems',methods=['GET', 'POST'])
def viewproblems():
    if request.method == 'POST':
        Problem_Type = request.form['Problem_Type']
        cur = mysql.connection.cursor()
        result = cur.execute("SELECT * FROM prob where Problem_Type like %s order by Prob_Id desc", (Problem_Type,))
        myproblems = cur.fetchall()

        if result > 0:
            return render_template('viewproblems.html', myproblems=myproblems)
        else:
            msg = 'No problems posted'
            return render_template('viewproblems.html', msg=msg)
        cur.close()
    return render_template('viewproblems.html')










@app.route("/quote")
def display_quote():
  symbol = request.args.get('symbol', default="AAPL")

  quote = yf.Ticker(symbol)

  return quote.info


# API route for pulling the stock history
@app.route("/history")
def display_history():

    symbol = request.args.get('symbol', default="AAPL")
    period = request.args.get('period', default="1y")
    interval = request.args.get('interval', default="1mo")
    quote = yf.Ticker(symbol)
    hist = quote.history(period=period, interval=interval)
    data = hist.to_json()
    return data





@app.route('/stockmarket')
def stockmarkets():
    return render_template('stockmarket.html')


class PostForm(Form):
    Post_Type = StringField('Post Type', [validators.Length(min=1, max=30)])
    Post_Subject = StringField('Post Subject', [validators.Length(min=1, max=30)])
    Post_Contact = IntegerField('Post Contact')

    Post_Linkdin = StringField('Post_Linkdin',[validators.Length(min=1, max=100)])
    Post_Github = StringField('Post_Github', [validators.Length(min=1, max=500)])
    Post_Body = TextAreaField('Post_Body',[validators.Length(min=1)])
    Post_Imglink1 = TextAreaField('Post_Imglink1', [validators.Length(min=1)])
    Post_Imglink2 = TextAreaField('Post_Imglink2', [validators.Length(min=1)])
    Post_Imglink3 = TextAreaField('Post_Imglink3', [validators.Length(min=1)])

@app.route('/add_post',methods=['GET', 'POST'])
def add_post():
    form= PostForm(request.form)
    if request.method == 'POST' and form.validate():
        Post_Type = form.Post_Type.data
        Post_Subject = form.Post_Subject.data
        Post_Contact = form.Post_Contact.data
        Post_Linkdin = form.Post_Linkdin.data
        Post_Github = form.Post_Github.data
        Post_Body = form.Post_Body.data
        Post_Imglink1 = form.Post_Imglink1.data
        Post_Imglink2 = form.Post_Imglink2.data
        Post_Imglink3 = form.Post_Imglink3.data
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO post(Post_Type, Post_Subject,Post_Author, Post_Contact,Post_Linkdin, Post_Github, Post_Body, Post_Imglink1, Post_Imglink2, Post_Imglink3) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",(Post_Type, Post_Subject, session['username'], Post_Contact, Post_Linkdin, Post_Github, Post_Body, Post_Imglink1, Post_Imglink2, Post_Imglink3))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('add_post'))

    return render_template('add_post.html',form = form)


class CvForm(Form):
    Cv_Photo = StringField('Cv_Photo',)
    Cv_Full_Name = StringField('Cv_Full_Name', )
    Cv_Speciality = StringField('Cv_Speciality',)
    Address = StringField('Address', )
    Email = StringField('Email', )
    Contact = IntegerField('Contact')
    Linkdin = StringField('Linkdin',)
    Twitter = StringField('Twitter', )
    Github = StringField('Github', )
    Website = StringField('Website', )
    Profile = TextAreaField('Profile',)
    Skills = TextAreaField('Skills',)
    Languages = StringField('Languages',)
    Software = StringField('Software',)
    Experience = TextAreaField('Experience',)
    Qualification =TextAreaField('Education',)
    Certification = TextAreaField('Certification',)



@app.route('/cv',methods=['GET', 'POST'])
def cv():
    ct = mysql.connection.cursor()
    result = ct.execute("SELECT * FROM cv where Cv_Author like %s",(session['username'],))
    get = ct.fetchall()
    if (result == 0) :
        at = True
        form = CvForm(request.form)
        if request.method == 'POST' and form.validate():
            Cv_Photo = form.Cv_Photo.data
            Cv_Full_Name = form.Cv_Full_Name.data
            Cv_Speciality = form.Cv_Speciality.data
            Address = form.Address.data
            Email = form.Email.data
            Contact = form.Contact.data
            Linkdin = form.Linkdin.data
            Twitter = form.Twitter.data
            Github = form.Github.data
            Website = form.Website.data
            Profile = form.Profile.data
            Skills = form.Skills.data
            Languages = form.Languages.data
            Software = form.Software.data
            Experience =form.Experience.data
            Qualification = form.Qualification.data
            Certification = form.Certification.data


            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO cv(Cv_Photo, Cv_Full_Name, Cv_Speciality, Cv_Author, Address, Email, Contact, Linkdin, Twitter, Github, Website, Profile, Skills, Languages, Software, Experience, Qualification, Certification) VALUES(%s, %s, %s, %s, %s, %s, %s, %s ,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",(Cv_Photo, Cv_Full_Name, Cv_Speciality, session['username'], Address, Email, Contact, Linkdin, Twitter, Github, Website, Profile, Skills, Languages, Software, Experience, Qualification, Certification))
            mysql.connection.commit()
            cur.close()
            return redirect(url_for('cv'))
        return render_template('cv.html', form =form,at=at)
    return render_template('cv.html', get=get)
    ct.close()


class ReportPost(Form):
    Report_Person = StringField('Report_Person')
    Report_Issue = TextAreaField('Report_Issue', [validators.Length(min= 10)])


@app.route('/viewcv')
def viewcv(a):
    cur = mysql.connection.cursor()
    # result = cur.execute("SELECT * FROM cv where Cv_Author = %s",[a, ])
    # result = cur.execute("select* from post inner join cv on post.Post_Author = cv.Cv_Author where Post_Author = %s;", [a, ])
    result = cur.execute("select * from post inner join cv on post.Post_Author = cv.Cv_Author where Post_Author = %s",[a, ])
    get = cur.fetchall()

    if result > 0:
        return render_template('viewcv.html', get=get,)
    else:
        msg = 'No problems posted'
        return render_template('viewcv.html', msg=msg)
    cur.close()

@app.route('/findstartup',methods = ['GET', 'POST'])
@is_logged_in_iv
def findstartup():
    if request.method == 'POST':
        username = request.form['username']

        cur =mysql.connection.cursor()
        result = cur.execute("SELECT * FROM et WHERE username = %s", [username])
        if result > 0:
            cur.fetchone()
            # viewcv(username)

            return viewcv(username)
        else:
           error = 'Username not found'
           return render_template('findstartup.html', error=error)
        cur.close()
    return render_template('findstartup.html')

@app.route('/report',methods = ['GET', 'POST'])
@is_logged_in_iv
def report():
    form = ReportPost(request.form)
    if request.method == 'POST' and form.validate():
        Report_Person = form.Report_Person.data
        Report_Issue = form.Report_Issue.data
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO report(Report_Person, Report_Issue, Report_Author) VALUES(%s, %s, %s)", (Report_Person, Report_Issue, session['username']))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('report'))
    return render_template('report.html',form = form)



@app.route('/login_admin', methods=['GET', 'POST'])
def login_admin():
    if request.method == 'POST':
        # Get Form Fields
        username = request.form['username']
        password_candidate = request.form['password']

        # Create cursor
        cur = mysql.connection.cursor()

        # Get user by username
        result = cur.execute("SELECT * FROM admin WHERE username = %s", [username])

        if result > 0:
            # Get stored hash
            data = cur.fetchone()
            password = data['password']

            # Compare Passwords
            if (password_candidate == password):

                session['logged_in'] = True
                session['username'] = username

                flash('You are now logged in')
                return redirect(url_for('dashboard_admin'))
            else:
                error = 'Invalid login'
                return render_template('login_admin.html', error=error)
            # Close connection
            cur.close()
        else:
            error = 'Username not found'
            return render_template('login_admin.html', error=error)

    return render_template('login_admin.html')


@app.route('/dashboard_admin')
def dashboard_admin():
    return render_template('dashboard_admin.html')


def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login', 'danger')
            return redirect(url_for('index'))
    return wrap

@app.route('/logout_admin')
@is_logged_in
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('index'))

@app.route('/viewet')
@is_logged_in
def viewet():
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM et")
    myproblems = cur.fetchall()

    if result > 0:
        return render_template('viewet.html', myproblems=myproblems)
    else:
        msg = 'No problems posted'
        return render_template('viewet.html', msg=msg)
    cur.close()
    return render_template('viewet.html')


@app.route('/viewiv')
@is_logged_in
def viewiv():
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM iv")
    myproblems = cur.fetchall()

    if result > 0:
        return render_template('viewiv.html', myproblems=myproblems)
    else:
        msg = 'No problems posted'
        return render_template('viewiv.html', msg=msg)
    cur.close()
    return render_template('viewiv.html')

@app.route('/viewreports')
@is_logged_in
def viewreports():
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM report")
    myproblems = cur.fetchall()

    if result > 0:
        return render_template('viewreports.html', myproblems=myproblems)
    else:
        msg = 'No reports posted'
        return render_template('viewreports.html', msg=msg)
    cur.close()
    return render_template('viewreports.html')









if __name__ == '__main__':
    app.secret_key = 'secret123'
    app.run(debug=True)

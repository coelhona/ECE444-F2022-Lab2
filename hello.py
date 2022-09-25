from email.message import EmailMessage
from flask import Flask, render_template, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, EmailField
from wtforms.validators import DataRequired
app = Flask(__name__)
app.config["SECRET_KEY"] = 'wagwan'

bootstrap = Bootstrap(app)
moment = Moment(app)



class UofTForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    email = EmailField('What is your UofT Email Address?', validators=[DataRequired()])
    submit = SubmitField('Submit')

@app.route('/', methods=['GET', 'POST'])
def index():
    form = UofTForm()
    if form.validate_on_submit():
        prev_name = session.get('name')
        prev_email = session.get('email')

        if prev_name is not None and prev_name != form.name.data: 
            flash('Wow look who got a name change!') #flashing alert that name has been changed
        
        if prev_email is not None and prev_email != form.email.data:
            flash('Wow look who got an email change!') #flashing alert that email has been changed
        
        session['name'] = form.name.data #storing name in user sessions so that it is remembered after the request has been made

        if "utoronto" in form.email.data:
            session['email'] = form.email.data
        else:
            session['email'] = None
        
        return redirect(url_for('index')) #calling redirect to avoid refresh confirmation warning from a repeat POST request
    return render_template('index.html', form=form, name=session.get('name'), email=session.get('email'))

@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)
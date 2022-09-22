from contextlib import redirect_stderr
from tkinter.tix import Form
from unicodedata import name
from flask import Flask, render_template, request,flash,redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


#CONFIGURACION DEL SERVIDOR 
app = Flask(__name__)
#Add Database 
##app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

##app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+mysqlconnector://root:''@localhost/cliente"

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+mysqldb://root@127.0.0.1/cliente"
# "mysql+mysqldb://scott:tiger@192.168.0.134/test"
app.config['SECRET_KEY']='My super secret that no one is supposed to know'
#Initialize the Database
db =SQLAlchemy(app)
#creacion de la tabla  model y cliente
#tabla cliente
class cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    password = db.Column(db.String(128))

#Create Model
#tabla users
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

#Create a String
    def __repr__(self):
        return '<Name: %s>' % self.name
#cracion de un formaulario
#Create form class
class UserForm(FlaskForm):
    name=StringField('Name', validators=[DataRequired()])
    email=StringField('Email', validators=[DataRequired()])
    submit=SubmitField('Submit')
#Create a form class
class NamerForm(FlaskForm):
    name=StringField('What is your name', validators=[DataRequired()])
    submit=SubmitField('Submit')

@app.route('/')

def index():
    first_name = 'Jonathan trabajo en abancay'
    favorites_pizza = ['Peperony','Hawaiana','Americana','Triplequeso']
    return render_template("name.html",
    first_name = first_name, 
    favorites_pizza=favorites_pizza)


@app.route('/name',methods=['GET','POST'])
def name():
    name = None
    form=NamerForm(request.form)
    #Validate form
    if form.validate_on_submit():
        name = form.name.data
        form.name.data =''
        # flash('')
    return render_template('user.html',name=name,form=form)

@app.route('/user/add',methods=['GET','POST'])

def add_user():
    name = None
    form = UserForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email = form.email.data).first()
        if user is None:
            user = Users(name = form.name.data, email = form.email.data)
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        form.name.data = ''
        form.email.data = ''
        flash("Usuario añadido con exito")
    our_users = Users.query.order_by(Users.date_added)

    return render_template('add_user.html',
            form = form,
            name = name,
            our_users= our_users)

@app.route('/user',methods=['GET'])
def CRUD():
    users = Users.query.order_by(Users.date_added)
    return render_template("users/index.html", users=users)

@app.route('/user/edit/<id>',methods=['GET'])
#funcion  editar 
def edit(id):
    user = Users.query.filter_by(id = id).first()
    form = UserForm()
    form.name.data = user.name
    form.email.data = user.email
    return render_template("users/edit.html", form=form, id=user.id)

@app.route('/user/edit/<id>',methods=['POST'])
#funcion actualizar 
def update(id):
    form = UserForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(id = id).first()
        user.name = form.name.data
        user.email = form.email.data
        db.session.commit()
        flash("Usuario actualizado")
    return redirect(url_for('CRUD'))
#funcion para eliminar 
@app.route('/user/delete/<id>',methods=['POST'])
def delete(id):
    user = Users.query.filter_by(id = id).first()
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('CRUD'))
#funcion usuario
@app.route('/user/<name>')
def user(name):
    return render_template('user.html', names=name)















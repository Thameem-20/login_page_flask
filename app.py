from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'thisisasecretkey'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)

class Registerform(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder":"username"})
    password = PasswordField(validators=[InputRequired(),Length(min=8, max=20)], render_kw={"placeholder": "password"})
    submit = SubmitField("Register")

    def validate_username(self, username):
        existing_user_username = User.query.filter_by(username = username.data).first()
        
        if existing_user_username:
            raise ValidationError(
                "This username already exist!, please try a different one ")
            
class Loginform(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder":"username"})
    password = PasswordField(validators=[InputRequired(),Length(min=8, max=20)], render_kw={"placeholder": "password"})
    submit = SubmitField("login")


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods = ['GET','POST'])
def login():
    form = Loginform()
    return render_template('login.html', form=form)

@app.route('/register', methods = ['GET','POST'])
def register():
    form = Registerform()
    return render_template('register.html', form=form)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

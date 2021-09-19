from flask_app.config.mysqlconnection import connectToMySQL
from flask import Flask, flash, session
import re
from flask_bcrypt import Bcrypt
app = Flask(__name__)
bcrypt = Bcrypt(app)
DATABASE = "floral_schema"
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'^[a-zA-Z]\S*$')

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @classmethod
    def select(cls, type='id', data=None):
        if data:
            query = f"SELECT * FROM users WHERE users.{type} = %({type})s"
            results = connectToMySQL(DATABASE).query_db(query, data)
            user = cls(results[0])
            return user
        else:
            query = "SELECT * FROM users"
            results = connectToMySQL(DATABASE).query_db(query)
            users = []
            for user in results:
                users.append(cls(user))
            return users

    @classmethod
    def check_login(cls, data):
        query = "SELECT * FROM users WHERE users.email = %(email)s"
        results = connectToMySQL(DATABASE).query_db( query, data )
        user = cls(results[0])
        if user.email == data['email'] and bcrypt.check_password_hash(user.password, data['password']):
            session['uuid'] = user.id
            return True
        else:
            flash("Incorrect email/password try again", 'login_email')
            return False

    @classmethod
    def registration(cls, data):
        data['password'] = bcrypt.generate_password_hash(data['password'])
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s)"
        results = connectToMySQL(DATABASE).query_db(query, data)
        if query:
            session['uuid'] = results
        return results


    @staticmethod #login validation
    def validate_login(data):
        is_valid = True
        query1 = "select * from users where users.email = %(email)s"
        if not connectToMySQL(DATABASE).query_db(query1, data):
            flash("Email doesn't exist", 'login_email')
            is_valid = False
        if len(data['email']) < 7:
            flash('Email must be at least 7 characters', 'login_email')
            is_valid = False
        if not EMAIL_REGEX.match(data['email']):
            flash("Invalid Email Address!", 'login_email')
            is_valid = False
        if len(data['password']) < 8:
            flash('Password must be at least 8 characters', 'login_password')
            is_valid = False
        str1 = data['password']
        digits = 0
        uppers = 0
        for i in str1:
            if i.isdigit():
                digits += 1
            if i.isupper():
                uppers += 1
        if digits == 0:
            flash ('Password MUST contain at least one number!', 'login_password')
            is_valid = False
        if uppers == 0:
            flash ('Password MUST contain at least ONE capital letter!', 'login_password')
            is_valid = False
        return is_valid

    @staticmethod #registration validation
    def validate_register(data):
        is_valid = True
        if not data['password_confirmation'] == data['password']:
            flash('Passwords Do Not Match', 'password')
            is_valid = False
        if not NAME_REGEX.match(data['first_name']):
            flash ("First Name can only contain letters", 'first_name')
        if not NAME_REGEX.match(data['last_name']):
            flash ("Last Name can only contain letters", 'last_name')
        if len(data['email']) < 7:
            flash('Email must be at least 7 characters', 'email')
            is_valid = False
        if not NAME_REGEX.match(data['first_name']):
            flash ("first_name can only contain letters", 'first_name')
        if len(data['first_name']) < 2:
            flash("First Name MUST be at least 5 characters long", 'first_name')
            is_valid = False
        if not NAME_REGEX.match(data['last_name']):
            flash ("last_name can only contain letters", 'last_name')
        if len(data['last_name']) < 2:
            flash("First Name MUST be at least 5 characters long", 'last_name')
            is_valid = False
        if not EMAIL_REGEX.match(data['email']):
            flash("Invalid Email Address!", 'email')
            is_valid = False
        query1 = "select * from users where users.email = %(email)s"
        if connectToMySQL(DATABASE).query_db(query1, data):
            flash("Email already exists, please Login, if you forgot your password TOUGH", 'email')
            is_valid = False
        if len(data['password']) < 8:
            flash('Password must be at least 8 characters', 'password')
            is_valid = False
        str1 = data['password']
        digits = 0
        uppers = 0
        for i in str1:
            if i.isdigit():
                digits += 1
            if i.isupper():
                uppers += 1
        if digits == 0:
            flash ('Password MUST contain at least one number!', 'password')
            is_valid = False
        if uppers == 0:
            flash ('Password MUST contain at least ONE capital letter!', 'password')
            is_valid = False
        return is_valid
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import recipe
import re


EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__(self,data):
        self.id = data["id"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.email = data["email"]
        self.password = data["password"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

    @classmethod
    def save(cls,data):
        query = """INSERT INTO users (first_name, last_name, email, password, created_at, updated_at)
            VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, NOW(), NOW());
            """
        return connectToMySQL('recipes_schema').query_db(query,data)

    @classmethod
    def get_by_email(cls,data):
        query = """SELECT * from users
            WHERE email = %(email)s;
            """
        result = connectToMySQL('recipes_schema').query_db(query,data)
        if len(result) < 1:
            return False
        return cls(result[0])

    @classmethod
    def get_by_id(cls,data):
        query = """SELECT * from users
            WHERE id = %(id)s;
            """
        result = connectToMySQL('recipes_schema').query_db(query,data)
        return cls(result[0])

    @staticmethod
    def validate_login(user):
        is_valid = True
        if len(user['first_name']) < 1:
            flash("Missing first name")
            is_valid = False
        if len(user['last_name']) < 1:
            flash("Missing last name")
            is_valid = False
        if len(user['password']) < 1:
            flash("Missing password")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid email address!")
            is_valid = False
        return is_valid

    @staticmethod
    def validate_user( user ):
        is_valid = True
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid email address!")
            is_valid = False
        return is_valid
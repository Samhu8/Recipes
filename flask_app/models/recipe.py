from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user
from flask import flash


DB = "recipes_schema"
class Recipe:
    def __init__(self,data):
        self.id = data["id"]
        self.name = data["name"]
        self.description = data["description"]
        self.instructions = data["instructions"]
        self.date = data["date"]
        self.under = data["under"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.user_id = data["user_id"]
        self.user = None

    @classmethod
    def save(cls,data):
        query = """INSERT INTO recipes (name, description, instructions, date, under, user_id)
            VALUES (%(name)s, %(description)s, %(instructions)s, %(date)s, %(under)s, %(user_id)s);
            """
        result = connectToMySQL('recipes_schema').query_db(query,data)
        return result

    @classmethod
    def show_all_recipes(cls):
        query = """SELECT * FROM recipes
                LEFT JOIN users
                ON recipes.user_id = users.id;
                """
        results = connectToMySQL('recipes_schema').query_db(query)
        all_recipes = []
        for row_in_db in results:
            recipe_info = cls(row_in_db)
            user_data = {
                "id": row_in_db["users.id"],
                "first_name": row_in_db["first_name"],
                "last_name" : row_in_db["last_name"],
                "email" : row_in_db["email"],
                "password" : None,
                "created_at" : row_in_db["users.created_at"],
                "updated_at" : row_in_db["users.updated_at"]
            }
            recipe_info.user = user.User(user_data)
            all_recipes.append(recipe_info)
        return all_recipes

    @classmethod
    def show_one(cls,id):
        query = """SELECT * from recipes
            WHERE id = %(id)s;
            """
        data = {'id' : id}
        results = connectToMySQL('recipes_schema').query_db(query,data)
        return cls(results[0])

    @classmethod
    def edit_recipe(cls,data):
        query = """UPDATE recipes
        SET name = %(name)s, description = %(description)s, instructions = %(instructions)s, date = %(date)s, under = %(under)s
        WHERE id = %(id)s;"""
        results = connectToMySQL('recipes_schema').query_db(query,data)
        return results

    @classmethod
    def show_one(cls,id):
        query = """SELECT * FROM recipes
                JOIN users on recipes.user_id = users.id
                WHERE recipes.id = %(id)s;"""
        data = {
            "id" : id
        }
        results = connectToMySQL(DB).query_db(query,data)[0]
        recipe_obj = Recipe(results)
        user_info = user.User({
            "id" : results["users.id"],
            "first_name" : results["first_name"],
            "last_name" : results["last_name"],
            "email" : results["email"],
            "password" : results["password"],
            "created_at" : results["users.created_at"],
            "updated_at" : results["users.updated_at"]
        })
        recipe_obj.user = user_info
        print(user_info.first_name)
        return recipe_obj

    @classmethod
    def delete_recipe(cls,id):
        query = """ DELETE FROM recipes
        WHERE id = %(id)s;
        """
        data = {"id" : id}
        return connectToMySQL(DB).query_db(query,data)

    @staticmethod
    def validate_recipe(recipe):
        is_valid = True
        if len(recipe['name']) < 3:
            flash("Name must be at least 3 characters")
            is_valid = False
        if len(recipe['description']) < 3:
            flash("Description must be at least 3 characters")
            is_valid = False
        if len(recipe['instructions']) < 3:
            flash("Instructions must be at least 3 characters")
            is_valid = False
        return is_valid
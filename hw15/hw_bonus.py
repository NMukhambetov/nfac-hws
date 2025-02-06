"""
💎 Exercise 1: User Management System

Design a User Management System for an application. 
The User class should have details such as name and email. 
he User Management System should allow users to register, 
delete their account, and update their information.
"""

class User:
    def __init__(self, name, email):
        pass

class UserManagementSystem:
    def register(self, user):
        pass

    def delete_account(self, user):
        pass

    def update_info(self, user, new_info):
        pass

"""
💎 Exercise 2: Quiz Application

Create a Quiz class that has a list of Questions. 
Each Question has a question, a list of options and a correct answer. 
The Quiz should allow questions to be added, and it should calculate the 
score of a user based on the answers they provide.
"""

class Question:
    def __init__(self, question, options, correct_answer):
        pass

class Quiz:
    def add_question(self, question):
        pass

    def calculate_score(self, user_answers):
        pass

"""
💎 Exercise 3: Recipe Management System

Design a Recipe Management System. The Recipe class should have a name, 
a list of ingredients and the preparation steps. 
The Recipe Management System should allow recipes to be added, removed, 
and searched by ingredient.
"""

class Recipe:
    def __init__(self, name, ingredients, steps):
        pass

class RecipeManagementSystem:
    def add_recipe(self, recipe):
        pass

    def remove_recipe(self, recipe):
        pass

    def search_by_ingredient(self, ingredient):
        pass

"""
💎 Exercise 4: Online Shopping System

Create a ShoppingCart class for an online shopping system. 
The Product class represents a product with name and price. 
The ShoppingCart should allow products to be added, removed, 
and it should calculate the total price of the products in the cart.
"""

class Product:
    def __init__(self, name, price):
        pass

class ShoppingCart:
    def add_product(self, product):
        pass

    def remove_product(self, product):
        pass

    def calculate_total(self):
        pass

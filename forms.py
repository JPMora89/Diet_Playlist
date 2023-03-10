from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, PasswordField, SelectField
from wtforms.validators import DataRequired, Email, Length
from wtforms_sqlalchemy.fields import QuerySelectField
from models import db, connect_db, User, Food, Diets

class CreateUserForm(FlaskForm):
    """form to create a users."""

    username = StringField('Username', 
        validators=[DataRequired()])
    password = PasswordField('Password', 
        validators=[DataRequired(), Length(min=6)])
    email = StringField('E-mail',
        validators=[DataRequired(), Email()])
    firstname = StringField('First Name',
        validators=[DataRequired()])
    lastname = StringField('Last Name',
        validators=[DataRequired()])

class LoginForm(FlaskForm):
    """Login form."""

    username = StringField('Username', 
        validators=[DataRequired()])
    password = PasswordField('Password', 
        validators=[Length(min=6)])

class FoodSearchForm(FlaskForm):
    "food search form, user inputs ingredients and qty"

    food = StringField('Name',
        validators=[DataRequired()])
    quantity = IntegerField('Quantity',
        validators=[DataRequired()])

# class MealTypeForm(FlaskForm):
#     meal_type = SelectField(
#         'Meal Type',  
#         choices= [('breakfast', 'Breakfast'), ('lunch', 'Lunch'), ('dinner', 'Dinner'), ('snack', 'Snack')])

class MakeOwnDietPlanForm(FlaskForm):
    diet_name = StringField('Diet Name', validators=[DataRequired()])
    diet_type = SelectField('Type of Diet', 
    choices= [('weight loss', 'Weight Loss'), ('bulking', 'Bulking'), ('maintain', 'Maintain')])


def DietQuery():
    return Diets.query

class ChooseDietForm(FlaskForm):
    options = SelectField("User Diets")
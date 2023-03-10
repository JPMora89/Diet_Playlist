import json
import requests
import os
from flask import Flask, render_template, request, flash, redirect, session, g
from flask_debugtoolbar import DebugToolbarExtension
# from wtforms_sqlalchemy.fields import QuerySelectField

from sqlalchemy.exc import IntegrityError

from forms import CreateUserForm, LoginForm, MakeOwnDietPlanForm, ChooseDietForm
from models import db, connect_db, User, Food, Diets

CURR_USER_KEY = "curr_user"
app = Flask(__name__)
app.app_context().push()



app.config['SQLALCHEMY_DATABASE_URI'] = (os.environ.get('DATABASE_URL', 'postgresql:///diet_playlist'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = True
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "ManchesterUnited")
app.debug = True
toolbar = DebugToolbarExtension(app)
connect_db(app)

db.create_all()



food_data_list = []
DEFAULT_IMAGE = "https://media.istockphoto.com/id/1190330112/photo/fried-pork-and-vegetables-on-white-background.jpg?s=612x612&w=0&k=20&c=TzvLLGGvPAmxhKJ6fz91UGek-zLNNCh4iq7MVWLnFwo="
app.config['SECRET_KEY'] = "Manchester United"



@app.before_request
def add_user_to_global():
    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])
    
    else:
        g.user = None

def user_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.id

def user_logout():
    "Logout user."

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]

def get_food_data(ingredient):
    food_data_list.clear()
    app_id = '87acc9c6'
    app_key = '18926addc269b99d7f700292aefdcf5d'
    
    url = 'https://api.edamam.com/api/food-database/parser?ingr=' + ingredient + '&app_id=' + app_id + '&app_key=' + app_key
    response = requests.get(url)
    return response.json()

@app.route('/signup', methods=["GET", "POST"])
def signup():
    """Handle user signup."""


    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]

    form = CreateUserForm()

    if form.validate_on_submit():
        try:
            user = User.signup(
                username=form.username.data,
                password=form.password.data,
                email=form.email.data,
                firstname=form.firstname.data,
                lastname=form.lastname.data
            )
            
            db.session.commit()

        except IntegrityError:
            flash("Username already exist.", 'danger')
            return render_template('users/signup.html', form=form)
        
        user_login(user)

        return redirect("/")
    
    else: 
        return render_template('users/signup.html', form=form)

@app.route('/login', methods=["GET", "POST"])
def login():
    """Handle user login"""

    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data,
                                form.password.data)
            
        if user:
            user_login(user)
            flash(f"Welcome, {user.username}", 'success')
            return redirect("/")
        flash("Invalid password", 'danger')

    return render_template('users/login.html', form=form)

@app.route('/logout')
def logout():
    """Handle logout user."""

    user_logout()
    flash("Success log out!", 'success')

    return redirect("/login") 




@app.route('/search_food', methods=['GET', 'POST'])
def food_search():
    # Searching for food
    if g.user is None or not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/login")
    
    else:
        ingredient = request.args.get('q')
        data = get_food_data(ingredient)

        '''save the data from API to an array'''
        for a_hints in data['hints']:
            '''get the image_url or return default image'''
            image_url = a_hints['food'].get('image') if a_hints['food'].get('image') else DEFAULT_IMAGE

            '''get the nutrition list and return a single item in nutrition'''
            nutritions = a_hints['food'].get('nutrients')
            nutrition_list = []
            for nutrient_name, nutrient_value in nutritions.items():
                nutrition_list.append({'name': nutrient_name, 'value': round(nutrient_value, 2)})

            food_data_list.append({'api_id': a_hints['food'].get('foodId'),
                            'label': a_hints['food'].get('label'),
                            'image_url': image_url,
                            'nutrition': nutrition_list})
            
            user_id = g.user.id
    
    form = ChooseDietForm()
    diet_from_db = db.session.query(Diets.diet_name)

    form.options.choices = diet_from_db
    # food_likes = [food.api_id for food in User.query.get(user_id).foods]
    
    return render_template('search_food.html', food_list=food_data_list, user_id= user_id, form=form, diet_from_db=diet_from_db)




@app.route('/', methods=['GET', 'POST'])
def meals():
    form = MakeOwnDietPlanForm()

    if form.validate_on_submit():
        # I tried getting the data using form.diet_name.data also but was not working either.
        diet_name = request.form['diet_name']
        diet_type = request.form['diet_type']

        result = request.form
        flash('New diet created successfully!', 'success')
        return redirect('display_diet.html', diet_name=diet_name, diet_type=diet_type, result=result)

    return render_template('create_diet.html', form=form)


@app.route('/display_diets/<int:user_id>')
def display_diets(user_id):
    user_diets = Diets.query.filter_by(user_id=user_id).all()
    result = request.form

    return render_template('display_diets.html', diets=user_diets, result=result)



# @app.route('/create_diet', methods=['GET, POST'])
# def create_diet():
#     form= MakeOwnDietPlanForm()
#     diet_name = form.diet_name.data
#     diet_type = form.diet_type.data
#     # user_id = request.json.get('userId')
#     new_diet = Diets(diet_name=diet_name, diet_type=diet_type)
#     db.session.add(new_diet)
#     db.session.commit()

@app.route('/display_diets', methods=['GET', 'POST'])
def show_user_diets():
    form = MakeOwnDietPlanForm()
    diet_name = form.diet_name.data
    diet_type = form.diet_type.data
    result = request.form        
    user_id=g.user.id
    new_diet = Diets(diet_name=diet_name, diet_type=diet_type, user_id=user_id)
    db.session.add(new_diet)        
    db.session.commit()

    # api_id = request.json.get('apiId')
    # user_id = request.json.get('userId')
    # new_diet = Diets(diet_name=diet_name, diet_type=diet_type, user_id=user_id)
    # db.session.add(new_diet)
    # db.session.commit()
    diets = Diets.query.all()
    return render_template('display_diets.html', form=form, result=result, diet_name=diet_name, diet_type=diet_type, diets=diets)



    

@app.errorhandler(404)
def page_not_found(e):
    """404 NOT FOUND page"""

    return render_template('404.html'),  404

 

@app.after_request
def add_header(req):
    """Add non-caching headers on every request."""

    req.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    req.headers["Pragma"] = "no-cache"
    req.headers["Expires"] = "0"
    req.headers['Cache-Control'] = 'public, max-age=0'
    return req
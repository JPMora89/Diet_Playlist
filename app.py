import json
import requests
import os
from flask import Flask, render_template, request, flash, redirect, session, g
from flask_debugtoolbar import DebugToolbarExtension
# from wtforms_sqlalchemy.fields import QuerySelectField
from sqlalchemy.exc import IntegrityError

from forms import CreateUserForm, LoginForm, MakeOwnDietPlanForm, ChooseDietForm
from models import db, connect_db, User, Food, Diets, FoodinDiet

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
            print(food_data_list)

        
        food_to_add = [food.api_id for food in User.query.get(user_id).foods]

            
        form = ChooseDietForm()
        # diet_from_db = db.session.query(Diets.id, Diets.diet_name)
        # form.diet_options.choices = diet_from_db
        form.diet_options.choices = [(g.id, g.diet_name) for g in Diets.query.order_by('diet_name')]

        diet_id = [(g.id) for g in Diets.query.order_by('diet_name')]


        
        return render_template('search_food.html', food_list=food_data_list, user_id= user_id, form=form, diet_id=diet_id)
    
# use PUT method to create logic for the submit button

# @app.route('/search_food', methods=['PUT'])
# def addFoodtoDiet():
#     user_id= g.user.id
#     ingredient = request.args.get('q')
#     data = get_food_data(ingredient)

#     for a_hints in data['hints']:
#             '''get the image_url or return default image'''
#             image_url = a_hints['food'].get('image') if a_hints['food'].get('image') else DEFAULT_IMAGE

#             '''get the nutrition list and return a single item in nutrition'''
#             nutritions = a_hints['food'].get('nutrients')
#             nutrition_list = []
#             for nutrient_name, nutrient_value in nutritions.items():
#                 nutrition_list.append({'name': nutrient_name, 'value': round(nutrient_value, 2)})

#             food_data_list.append({'api_id': a_hints['food'].get('foodId'),
#                             'label': a_hints['food'].get('label'),
#                             'image_url': image_url,
#                             'nutrition': nutrition_list})


#     food_id = a_hints['food'].get('foodId')
#     new_food = FoodinDiet(food_id=food_id , user_id=g.user.id)
#     db.session.add(new_food)
#     db.session.commit()

#     return render_template('display_user_diets.html' )

 
# @app.route('diets/<int:id>')
# def add_food_to_diet(id):
#     new_food = 
# @app.route('/search_food', methods=['GET', 'POST'])

    
#     # specific_diet = 
#     # # form.diet_options.choices = diet_from_db
#     # # diet_from_db
#     # user_foods = [food.api_id for food in User.query.get(user_id).foods]
    
#     return render_template('search_food.html', diet=diet, form=form)




@app.route('/', methods=['GET', 'POST'])
def diets():
    form = MakeOwnDietPlanForm()

    if form.validate_on_submit():
        diet_name = request.form['diet_name']
        diet_type = request.form['diet_type']

        result = request.form
        flash('New diet created successfully!', 'success')
        return redirect('/diets', diet_name=diet_name, diet_type=diet_type, result=result)

    return render_template('create_diet.html', form=form)



@app.route('/diets', methods=['GET', 'POST'])
def show_user_diets():
    if request.method == 'POST':
        form = MakeOwnDietPlanForm()
        diet_name = form.diet_name.data
        diet_type = form.diet_type.data
        result = request.form        
    
    
        user_id = g.user.id
        new_diet = Diets(diet_name=diet_name, diet_type=diet_type, user_id=user_id)
        db.session.add(new_diet) 
        db.session.commit()
        print(food_data_list)

        diets = Diets.query.all()
        return render_template('display_diets.html', form=form, result=result, diet_name=diet_name, diet_type=diet_type, diets=diets)
    else:
        diets = Diets.query.all()
        return render_template('display_diets.html', diets=diets)

# update diet with selected foods
@app.route('/diets/update/<int:id>', methods=['PUT'])
def add_food_to_diet(id):
    diet_to_update = Diets.query.get_or_404(id)
    if request.method == 'POST':
        diet_to_update
    
    user_id = g.user.id

    return render_template('display_diets.html', diets=diets)

# delete selected diets

@app.route('/diets/delete/<int:id>', methods=['DELETE'])

def delete_user_diets(id):
    diet_to_delete = Diets.query.get_or_404(id)
    # console.log to see if function is being called
    try:
        db.session.delete(diet_to_delete)
        db.session.commit()
        diets = Diets.query.all()
        return render_template ('display_diets.html', diets=diets)
    except:  
        return flash("There was a problem deleting the diet")
# flash error message



@app.route('/diets/<int:id>', methods=['GET'])
def display_diets(id):
    user_id = g.user.id
    # diets = Diets.query.get_or_404(id)
    result = request.form
    diet = Diets.query.get(id)
    diet_name = diet.diet_name
    return render_template('display_user_diets.html', diets=diets, result=result, diet_name=diet_name)


# Showing foods in specific diets
@app.route('/diets/<int:id>', methods=['POST'])
def add_food_to_diets(id):
    user_id = g.user.id
    # new_foods = FoodinDiet(food_id= , diet_id = )
    user_diets = Diets.query.filter_by(user_id=user_id).all()
    result = request.form
    diet_name = user_diets.get('diet_name')
    api_id = request.json.get('apiId')
    user_id = request.json.get('userId')
    new_food = Food()

    return render_template('display_user_diets.html', user_diets=user_diets, result=result, diet_name=diet_name)

# deleting foods from a specific diet
# @app.route('/diets/delete/<int:id>', methods=['GET'])
# def delete(id):
#     user_id = g.user.id
#     user_diets = Diets.query.filter_by(user_id=user_id).all()
#     result = request.form

#     return render_template('display_user_diets.html', user_diets=user_diets, result=result)

@app.route('/diets/<int:id>', methods=['PUT'])
def update_diets(id):
    user_id = g.user.id
    diets = Diets.query.filter_by(user_id=user_id).all()
    result = request.form
    diet = [diet for diet in diets if diet.id == diet.id]
    return render_template('display_user_diets.html', diets=diets, result=result, diet=diet)


    

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

# import json
# import requests
# import os
# from flask import Flask, render_template, request, flash, redirect, session, g
# from flask_debugtoolbar import DebugToolbarExtension
# # from wtforms_sqlalchemy.fields import QuerySelectField
# from sqlalchemy.exc import IntegrityError

# from forms import CreateUserForm, LoginForm, MakeOwnDietPlanForm, ChooseDietForm
# from models import db, connect_db, User, Food, Diets

# CURR_USER_KEY = "curr_user"
# app = Flask(__name__)
# app.app_context().push()



# app.config['SQLALCHEMY_DATABASE_URI'] = (os.environ.get('DATABASE_URL', 'postgresql:///diet_playlist'))
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SQLALCHEMY_ECHO'] = True
# app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = True
# app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "ManchesterUnited")
# app.debug = True
# toolbar = DebugToolbarExtension(app)
# connect_db(app)

# db.create_all()



# food_data_list = []
# DEFAULT_IMAGE = "https://media.istockphoto.com/id/1190330112/photo/fried-pork-and-vegetables-on-white-background.jpg?s=612x612&w=0&k=20&c=TzvLLGGvPAmxhKJ6fz91UGek-zLNNCh4iq7MVWLnFwo="
# app.config['SECRET_KEY'] = "Manchester United"



# @app.before_request
# def add_user_to_global():
#     if CURR_USER_KEY in session:
#         g.user = User.query.get(session[CURR_USER_KEY])
    
#     else:
#         g.user = None

# def user_login(user):
#     """Log in user."""

#     session[CURR_USER_KEY] = user.id

# def user_logout():
#     "Logout user."

#     if CURR_USER_KEY in session:
#         del session[CURR_USER_KEY]

# def get_food_data(ingredient):
#     food_data_list.clear()
#     app_id = '87acc9c6'
#     app_key = '18926addc269b99d7f700292aefdcf5d'
    
#     url = 'https://api.edamam.com/api/food-database/parser?ingr=' + ingredient + '&app_id=' + app_id + '&app_key=' + app_key
#     response = requests.get(url)
#     return response.json()

# @app.route('/signup', methods=["GET", "POST"])
# def signup():
#     """Handle user signup."""


#     if CURR_USER_KEY in session:
#         del session[CURR_USER_KEY]

#     form = CreateUserForm()

#     if form.validate_on_submit():
#         try:
#             user = User.signup(
#                 username=form.username.data,
#                 password=form.password.data,
#                 email=form.email.data,
#                 firstname=form.firstname.data,
#                 lastname=form.lastname.data
#             )
            
#             db.session.commit()

#         except IntegrityError:
#             flash("Username already exist.", 'danger')
#             return render_template('users/signup.html', form=form)
        
#         user_login(user)

#         return redirect("/")
    
#     else: 
#         return render_template('users/signup.html', form=form)

# @app.route('/login', methods=["GET", "POST"])
# def login():
#     """Handle user login"""

#     form = LoginForm()

#     if form.validate_on_submit():
#         user = User.authenticate(form.username.data,
#                                 form.password.data)
            
#         if user:
#             user_login(user)
#             flash(f"Welcome, {user.username}", 'success')
#             return redirect("/")
#         flash("Invalid password", 'danger')

#     return render_template('users/login.html', form=form)

# @app.route('/logout')
# def logout():
#     """Handle logout user."""

#     user_logout()
#     flash("Success log out!", 'success')

#     return redirect("/login") 




# @app.route('/search_food', methods=['GET', 'POST'])
# def food_search():
#     # Searching for food
#     if g.user is None or not g.user:
#         flash("Access unauthorized.", "danger")
#         return redirect("/login")
    
#     else:
#         ingredient = request.args.get('q')
#         data = get_food_data(ingredient)

#         '''save the data from API to an array'''
#         for a_hints in data['hints']:
#             '''get the image_url or return default image'''
#             image_url = a_hints['food'].get('image') if a_hints['food'].get('image') else DEFAULT_IMAGE

#             '''get the nutrition list and return a single item in nutrition'''
#             nutritions = a_hints['food'].get('nutrients')
#             nutrition_list = []
#             for nutrient_name, nutrient_value in nutritions.items():
#                 nutrition_list.append({'name': nutrient_name, 'value': round(nutrient_value, 2)})

#             food_data_list.append({'api_id': a_hints['food'].get('foodId'),
#                             'label': a_hints['food'].get('label'),
#                             'image_url': image_url,
#                             'nutrition': nutrition_list})
            
#             user_id = g.user.id
        
#         # diet = Diets.query.all()
#         # form = ChooseDietForm(request.POST, obj=diet)
        
            
#         form = ChooseDietForm()
#         # diet_from_db = db.session.query(Diets.id, Diets.diet_name)
#         # form.diet_options.choices = diet_from_db
#         form.diet_options.choices = [(g.id, g.diet_name) for g in Diets.query.order_by('diet_name')]

#         diet_id = [(g.id) for g in Diets.query.order_by('diet_name')]
#         # diet_id = request._load_form_data
#         # for diet in Diets.query.order_by('diet_name'):
#         #     for g.id in diet:
            
#         #         diet_id = g.id 
# # def select_diet(request, id): 
        
        
#         return render_template('search_food.html', food_list=food_data_list, user_id= user_id, form=form, diet_id=diet_id)
    


# # @app.route('/search_food', methods=['GET', 'POST'])

    
# #     # specific_diet = 
# #     # # form.diet_options.choices = diet_from_db
# #     # # diet_from_db
# #     # user_foods = [food.api_id for food in User.query.get(user_id).foods]
    
# #     return render_template('search_food.html', diet=diet, form=form)




# @app.route('/', methods=['GET', 'POST'])
# def diets():
#     form = MakeOwnDietPlanForm()

#     if form.validate_on_submit():
#         diet_name = request.form['diet_name']
#         diet_type = request.form['diet_type']

#         result = request.form
#         flash('New diet created successfully!', 'success')
#         return redirect('/diets', diet_name=diet_name, diet_type=diet_type, result=result)

#     return render_template('create_diet.html', form=form)





# # @app.route('/create_diet', methods=['GET, POST'])
# # def create_diet():
# #     form= MakeOwnDietPlanForm()
# #     diet_name = form.diet_name.data
# #     diet_type = form.diet_type.data
# #     # user_id = request.json.get('userId')
# #     new_diet = Diets(diet_name=diet_name, diet_type=diet_type)
# #     db.session.add(new_diet)
# #     db.session.commit()

# @app.route('/diets', methods=['GET', 'POST'])
# def show_user_diets():
#     form = MakeOwnDietPlanForm()
#     diet_name = form.diet_name.data
#     diet_type = form.diet_type.data
#     result = request.form        
    
    
#     user_id = g.user.id
#     new_diet = Diets(diet_name=diet_name, diet_type=diet_type, user_id=user_id)
#     db.session.add(new_diet)        
#     db.session.commit()
#     print(food_data_list)
    
#     diets = Diets.query.all()
#     return render_template('display_diets.html', form=form, result=result, diet_name=diet_name, diet_type=diet_type, diets=diets)

# # bring user back to create diet form and let them update
# @app.route('/diets/update/<int:id>', methods=['GET','POST'])
# def update_user_diets(id):
#     diet_to_update = Diets.query.get_or_404(id)
#     if request.method == 'POST':
#         diet_to_update
    
#     user_id = g.user.id

#     return render_template('display_diets.html', diets=diets)

# @app.route('/diets/delete/<int:id>', methods=['DELETE'])

# def delete_user_diets(id):
#     diet_to_delete = Diets.query.get_or_404(id)
    
#     try:
#         db.session.delete(diet_to_delete)
#         db.session.commit()
#         return render_template ('display_diets.html', diet_to_delete=diet_to_delete)
#     except:  
#         return "There was a problem deleting the diet"  
# # flash error message



# @app.route('/diets/<int:id>')
# def display_diets(id):
#     user_id = g.user.id
#     user_diet = Diets.query.get_or_404(id)
#     result = request.form
    

#     return render_template('display_user_diets.html', user_diet=user_diet, result=result)


# # Showing foods in specific diets
# @app.route('/diets/<int:id>', methods=['POST'])
# def add_food_to_diets(id):
#     user_id = g.user.id
#     user_diets = Diets.query.filter_by(user_id=user_id).all()
#     result = request.form

#     return render_template('display_user_diets.html', user_diets=user_diets, result=result)

# # deleting foods from a specific diet
# # @app.route('/diets/delete/<int:id>', methods=['GET'])
# # def delete(id):
# #     user_id = g.user.id
# #     user_diets = Diets.query.filter_by(user_id=user_id).all()
# #     result = request.form

# #     return render_template('display_user_diets.html', user_diets=user_diets, result=result)

# @app.route('/diets/<int:diet_id>', methods=['PUT'])
# def update_diets(diet_id):
#     user_id = g.user.id
#     diets = Diets.query.filter_by(user_id=user_id).all()
#     result = request.form
#     diet = [diet for diet in diets if diet.id == diet_id]
#     return render_template('display_user_diets.html', diets=diets, result=result, diet=diet)


    

# @app.errorhandler(404)
# def page_not_found(e):
#     """404 NOT FOUND page"""

#     return render_template('404.html'),  404

 

# @app.after_request
# def add_header(req):
#     """Add non-caching headers on every request."""

#     req.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
#     req.headers["Pragma"] = "no-cache"
#     req.headers["Expires"] = "0"
#     req.headers['Cache-Control'] = 'public, max-age=0'
#     return req
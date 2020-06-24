from flask import Flask, request, redirect, render_template, url_for, session, flash, json, g
from models import db, connect_db, User, UserFoods, Food
from forms import UserAddForm, LoginForm
from sqlalchemy.exc import IntegrityError
from datetime import datetime

from get_data_from_api import get_data_api
from parse_food_response import parse_food

# from flask_debugtoolbar import DebugToolbarExtension
import os 

CURR_USER_KEY = "curr_user"

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgresql:///food_tracker')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', '123default89754key')
# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False


# toolbar = DebugToolbarExtension(app)
connect_db(app)

##############################################################################
# User signup/login/logout


@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None


def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.id


def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]
    
def authorize(f):
    def unauth():
        flash("Access unauthorized.", "danger")
        return render_template("home-anon.html")
    def wrapper(*args, **kwargs):
        f(*args, **kwargs)
    if g:
        return wrapper
    else:
        return unauth
        
@app.route('/signup', methods=["GET", "POST"])
def signup():
    """Handle user signup.

    Create new user and add to DB. Redirect to home page.

    If form not valid, present form.

    If the there already is a user with that username: flash message
    and re-present form.
    """
    form = UserAddForm(request.form)
    if form.validate_on_submit():
        try:
            user = User.signup(
                username=form.username.data,
                password=form.password.data
            )
            db.session.commit()

        except IntegrityError:
            flash("Username already taken", 'danger')
            return render_template('signup.html', form=form)

        do_login(user)

        return redirect("/")

    else:
        return render_template('signup.html', form=form)


@app.route('/login', methods=["GET", "POST"])
def login():
    """Handle user login."""
    form = LoginForm()
    if form.validate_on_submit():
        user = User.authenticate(form.username.data,
                                 form.password.data)

        if user:
            do_login(user)
            flash(f"Hello, {user.username}!", "info")
            return redirect("/")
        flash("Invalid credentials.", 'danger')    
    
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    """Handle logout of user."""
    do_logout()
    return redirect(url_for("login"))



@app.route("/")
def homepage():
    """Load homepage"""
    return render_template("home.html")


@app.route("/get_started")
def getstarted():
    """Load get started page"""
    return render_template("getstarted.html")


@app.route("/get_food_api", methods=["POST"])
def get_food_api():
    
    # get food query from javascript file
    food_choice = request.get_json("food")
    
    # get data from API
    resp = get_data_api(food_choice["food"])
    
    """If resp has data, then parse raw data.
       parsed_food: Dictionary {food_id, {description, {nutrient, value}}}
       food_id: int related to API id
       prod: str description or food title
       value: float in grams"""
    if resp is not None:
        parsed_food = parse_food(resp)
        user_choices = {}
        g_cache = {}
        for row in parsed_food:
            g_cache[str(row["fdcId"])] = {"description": row["description"], "nutrients": row["nutrients"]}
            user_choices[row["fdcId"]] = row["description"]
        
        session["G_CACHE"] = g_cache   
        return user_choices            
            
    else:
        flash("Error, please recheck inputs for spelling.", 'danger')
        return redirect(url_for("getstarted"))


@app.route("/get_food_by_id", methods=["POST"])
def get_food_by_id():
    """returns value of food data"""
    data = request.get_json("data")
    food = Food.get_food_by_id(data["food_id"])
    return food


@app.route("/get_food_cache", methods=["POST"])
def get_food_cache():
    """returns value of cached food key"""
    key = request.get_json("food_id")
    return session["G_CACHE"].get(key['food_id'])
    

@app.route("/user")
def do_user():
    """User/Guest page, if user is not signed in they can save data to the guest account"""
    if g.user:        
        date_string = {x.id : x.date_string for x in g.user.foods}
        return render_template("user.html", timestamps=date_string)
    
    else:        
        guest = User.query.filter_by(username="Guest").first() 
        date_string = {x.id : x.date_string for x in guest.foods}
        return render_template("user.html", timestamps=date_string)
    
@app.route("/save_data", methods=["POST"])
def do_save():
    """User/Guest page, if user is not signed in they can save data to the guest account"""
    food_data = request.get_json("data")
    
    if g.user:
        Food.add_food(g.user.id, food_data["food"], food_data["menuName"])
        return "true"
    
    else:
        guest = User.query.filter_by(username="Guest").first()
        Food.add_food(guest.id, food_data["food"], food_data["menuName"])
        return "true"
 
@app.route("/delete_food_by_id", methods=["POST"]) 
def delete_food():
    """Delete food from database"""
    data = request.get_json("data")
    Food.delete_food_by_id(data["food_id"])  
    return "true"

@app.route("/about")
def about():
    """Load about page"""
    return render_template("about.html")


@app.after_request
def add_headers(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    return response

if __name__ == '__main__':
    app.run(debug=True)
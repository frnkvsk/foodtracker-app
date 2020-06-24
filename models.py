"""SQLAlchemy models for Food Tracker"""

from datetime import datetime, date
from flask import json
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
bcrypt = Bcrypt()
db = SQLAlchemy()


class UserFoods(db.Model):
    """Food used by system users"""
    
    __tablename__ = 'userfoods'
    
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='CASCADE'),
        primary_key=True
    )
    food_id = db.Column(
        db.Integer,
        db.ForeignKey('foods.id', ondelete='CASCADE'),
        primary_key=True
    )
    
    
class User(db.Model):
    """User of the system"""
    
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False, unique=True)
    foods = db.relationship("Food", backref='users', lazy=True) 
    
    @classmethod
    def signup(cls, username, password):
        """Sign up user.

        Hashes password and adds user to system.
        """
        if username and password:
            hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

            user = User(
                username=username,
                password=hashed_pwd
            )

            db.session.add(user)
            return user
        else:
            return None
        
    @classmethod
    def authenticate(cls, username, password):
        """Find user with `username` and `password`.

        This is a class method (call it on the class, not an individual user.)
        It searches for a user whose password hash matches this password
        and, if it finds such a user, returns that user object.

        If can't find matching user (or if password is wrong), returns False.
        """

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False    
    
    # @classmethod
    # def get_food(cls, user_id):
    #     user = cls.query.filter_by(id=user_id).first()
    #     return user.foods
    
class Food(db.Model):
    """Food used by system users"""
    
    __tablename__ = 'foods'
    
    id = db.Column(db.Integer, primary_key=True)    
    data = db.Column(db.Text, nullable=False)
    # I used Text for date so I can add a menu title to the date.
    date_string = db.Column(db.Text, nullable=False)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='CASCADE'),
        nullable=False
    )
    
    @classmethod
    def get_food_by_id(cls, food_id):
        food = cls.query.filter_by(id=food_id).first()
        if food:
            return food.data
        return None
    
    @classmethod
    def add_food(cls, user_id, food_list, menu_name):
        """Add food dictionary to the database as a string object."""
        yyyy_mm_dd = str(datetime.utcnow()).split(" ")[0]
        food = cls(data=json.dumps(food_list), user_id=user_id, date_string=(yyyy_mm_dd+" "+menu_name))
        db.session.add(food)
        db.session.commit()
        user_food = UserFoods(user_id=user_id, food_id=food.id)
        db.session.add(user_food)
        db.session.commit()
        
    @classmethod
    def delete_food_by_id(cls, food_id):
        food = cls.query.filter_by(id=food_id).first()
        db.session.delete(food)
        db.session.commit()
    
    
def connect_db(app):
    """Connect this database to provided Flask app.
    You should call this in your Flask app.
    """
    db.app = app
    db.init_app(app)
    
    
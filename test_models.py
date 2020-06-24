"""Test models.py"""

# to run this test
#   python -m unittest test_models.py

import os
from unittest import TestCase

from models import db, User, UserFoods, Food
from flask_bcrypt import Bcrypt
from flask import json
bcrypt = Bcrypt()

os.environ['DATABASE_URL'] = "postgresql:///food_tracker_test"

from app import app

db.create_all()

class ModelTestCase(TestCase):    
    
    def setUp(self):
        """Create test client, add clear database tables"""
        User.query.delete()
        Food.query.delete()
        UserFoods.query.delete()
        
        self.client = app.test_client()
        
    def test_user_model(self):
        
        """Test user signup"""
        # hashed_pw = bcrypt.generate_password_hash("test_pw1").decode('UTF-8')
        User.signup("test_username1", "test_pw1")
        test_user1 = db.session.query(User).filter_by(username="test_username1").first()
        
        self.assertEqual("test_username1", test_user1.username)
        
        """Test authenticate"""
        # test positive
        isUser = User.authenticate("test_username1", "test_pw1")
        
        self.assertTrue(isUser)
        
        # test negative username
        isNotUser = User.authenticate("test_username2", "test_pw1")
        
        self.assertFalse(isNotUser)
        
        # test negative password
        isNotUser = User.authenticate("test_username1", "test_pw2")
        
        self.assertFalse(isNotUser)
        
    def test_food_model(self):
        
        """Test add_food"""
        User.signup("test_username1", "test_pw1")
        test_user1 = db.session.query(User).filter_by(username="test_username1").first()
        Food.add_food(test_user1.id, {"food1":{"test":"food"}}, "lunch")
        
        self.assertEqual(1, len(test_user1.foods))
        
        """Test get_food_by_id"""        
        # test positive
        test_id = test_user1.foods[0].id 
        test_food = json.loads(Food.get_food_by_id(test_id))
        
        self.assertEqual(test_food["food1"]["test"], "food")
        
        # test negative
        test_id2 = 1000
        test_food2 = Food.get_food_by_id(test_id2)
        
        self.assertEqual(test_food2, None)
        
        
        """Test delete_food_by_id"""
        Food.delete_food_by_id(test_id)
        
        self.assertEqual(0, len(test_user1.foods))
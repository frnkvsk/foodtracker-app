"""Test app.py"""

# to run this test
#   python -m unittest test_app.py

import os
from unittest import TestCase
from models import db, connect_db, User, Food, UserFoods
from flask import json
os.environ['DATABASE_URL'] = "postgresql:///food_tracker_test"

from app import app, CURR_USER_KEY, g

db.create_all()

app.config['WTF_CSRF_ENABLED'] = False

class AppTestCase(TestCase): 
    
    def setUp(self):
        """Create test client, add clear database tables"""
        User.query.delete()
        Food.query.delete()
        UserFoods.query.delete()
        
        self.client = app.test_client()
        # set up a signed in user
        tempuser = User.signup(username="testuser",
                                    password="testuser")
        
        db.session.commit()
        self.testuser = db.session.query(User).first()
        
        # set up the Guest user
        Guest = User.signup(username="Guest",
                                    password="Guestpassword")

        db.session.commit()
        
        # insert test food item into database
        food = Food(data="testfood", date_string="10-10-10 lunch", user_id=self.testuser.id)
        db.session.add(food)
        db.session.commit()
        self.food = db.session.query(Food).first()
        
        
    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()
            
    def test_add_user_to_g(self):
        with app.test_client() as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id
                
            """Test before request"""
            resp = c.get("/")
            self.assertEqual(self.testuser.id, g.user.id)
            
    def test_signup(self):
        with app.test_client() as c:
            # with c.session_transaction() as sess:
            #     sess[CURR_USER_KEY] = self.testuser.id
                
            """Test if user in setUp was successfully inserted int User db"""
            user = db.session.query(User).first()
            self.assertEqual("testuser", user.username)
            
    def test_logout_login(self):
        with app.test_client() as c:
            # with c.session_transaction() as sess:
            #     sess[CURR_USER_KEY] = self.testuser.id
                
            """Test user logout"""
            resp = c.get("/logout")  
            """Make sure it redirects"""
            self.assertEqual(resp.status_code, 302)
            """Follow redirect"""
            resp = c.get("/logout", follow_redirects=True)   
            self.assertEqual(resp.status_code, 200) 
            """Test redirected page"""    
            html = resp.get_data(as_text=True)            
            self.assertIn('<h2 class="form-title">Welcome back</h2>', html)
            """Test if user is logged out"""
            self.assertEqual(None, g.user)
            
            """Log user in"""
            resp = c.post("/login", data={"username": "testuser", "password": "testuser"}, follow_redirects=True) 
            self.assertEqual(resp.status_code, 200) 
            """Test redirected page"""    
            html = resp.get_data(as_text=True)            
            self.assertIn('<p>Track you dietary intake nutrients</p>', html)
    
    def test_homepage(self):
        with app.test_client() as c:
            # with c.session_transaction() as sess:
            #     sess[CURR_USER_KEY] = self.testuser.id
                
            resp = c.get("/")             
            self.assertEqual(resp.status_code, 200)            
            html = resp.get_data(as_text=True)            
            self.assertIn('<p>Track you dietary intake nutrients</p>', html)
                   
    def test_getstarted(self):
        with app.test_client() as c:
            resp = c.get("/get_started")             
            self.assertEqual(resp.status_code, 200)            
            html = resp.get_data(as_text=True)            
            self.assertIn('<label for="add-weight">Enter weight of ingredient in grams:</label>', html)
            
    def test_get_food_api(self):
        with app.test_client() as c:
            """Mock a javascript Axios post request and test to see if it successfully gets data from the API, processes the data, then returns a dictionary of food API keys with food choice values {fdcId: "food description"}"""
            
            """I comment this out while building my other tests so that it doesn't keep making unnecessary requests to the API"""
            # d = json.dumps({"food": "broccoli"})
            # resp = c.post("/get_food_api", data=d, content_type='application/json')
            # resp_dict = [x for x in json.loads(resp.get_data(as_text=True)).keys()]
            # self.assertEqual(resp.status_code,200)
            # # make sure the response returns and dictionary with integer keys
            # self.assertTrue(type(int(resp_dict[0])) is int)
            
            
    def test_get_food_by_id(self):
        with app.test_client() as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id
            
            
            
            # food = db.session.query(Food).first()   
            d = json.dumps({ "food_id": self.food.id })
            resp = c.post("/get_food_by_id", data=d, content_type='application/json')
            
            self.assertEqual(resp.status_code,200)
            # make sure the response returns the data we added
            self.assertEqual("testfood", resp.data.decode("utf-8"))

    def test_get_food_cache(self):
        with app.test_client() as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id
           
            """I comment this out while building my other tests so that it doesn't keep making unnecessary requests to the API"""
            
            """query API, render data, save data to session to use in this test"""
            # d = json.dumps({"food": "broccoli"})
            # resp = c.post("/get_food_api", data=d, content_type='application/json')
            # resp_dict = [x for x in json.loads(resp.get_data(as_text=True)).keys()]
            
            """use food id from API post response""" 
            # food_id = resp_dict[0]
            # d = json.dumps({ "food_id": food_id })
            
            """now we have the necessary data and the session variable is active"""
            # resp = c.post("/get_food_cache", data=d, content_type='application/json')
            
            # self.assertEqual(resp.status_code,200)
            """make sure response dictionary contains"""
            # self.assertEqual("Broccoli, raw", json.loads(resp.data)["description"])
    
    def test_do_user_nosession(self):
            
        """Connect to session. 
           Test if user is sent to user page with testuser data access"""
        with app.test_client() as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id
            resp = c.get("/user")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("<strong>Saved Menus</strong></p>", html)
            
    def test_do_user_withsession(self):  
            
        """Connect to session. 
           Test if user is sent to user page with testuser data access"""
        with app.test_client() as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id
            resp = c.get("/user")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("<strong>Saved Menus</strong></p>", html)
                 
    def test_do_save_nosession(self):
        
        """No session connection.
           Test if user is sent to user page with Guest data access"""
        with app.test_client() as c:
            d = json.dumps({ "food": "testfood", "menuName": "testlunch" })
            resp = c.post("/save_data", data=d, content_type='application/json')
            resp_str = resp.get_data(as_text=True)
            
            self.assertEqual(resp.status_code, 200)
            # make sure we get a "true" string response
            self.assertEqual("true", resp_str)
        
        
    def test_do_save_withsession(self):        
        
        """Connect to session. 
           Test if user is sent to user page with testuser data access"""
        with app.test_client() as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id
            d = json.dumps({ "food": "testfood", "menuName": "testlunch" })
            resp = c.post("/save_data", data=d, content_type='application/json')
            resp_str = resp.get_data(as_text=True)
            
            self.assertEqual(resp.status_code, 200)
            # make sure we get a "true" string response
            self.assertEqual("true", resp_str)   
    

    def test_delete_food(self):        
        
        """Test if user can delete food with the correct food id"""
        with app.test_client() as c:
            
            d = json.dumps({ "food_id": self.food.id })
            resp = c.post("/delete_food_by_id", data=d, content_type='application/json')
            resp_str = resp.get_data(as_text=True)            
            
            self.assertEqual(resp.status_code, 200)
            # make sure we get a "true" string response
            self.assertEqual("true", resp_str)   
        
    def test_about(self):
        with app.test_client() as c:
            resp = c.get("/about")
            html = resp.get_data(as_text=True)            
            
            self.assertEqual(resp.status_code, 200)
            self.assertIn("<h1>About Food Tracker</h1>", html)   
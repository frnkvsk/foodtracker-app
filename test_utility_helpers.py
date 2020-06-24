# to run these tests:
#    python -m unittest test_utility_helpers.py

from unittest import TestCase
from flask import json
from get_data_from_api import get_data_api
from parse_food_response import parse_food
from test_data import broccoli



class UtilityHelperTestCase(TestCase):
    
    def test_get_data_api(self):
        """First test a response that will generate zero results"""
        query_str = "nothing"
        resp = get_data_api(query_str)
        self.assertEqual(len(resp["foods"]), 0)
        
        """Test a response that will generate one result"""
        query_str = "broccoli"
        resp = get_data_api(query_str)
        self.assertEqual(len(resp["foods"]), 1)
    
    def test_parse_food_response(self):
        json_acceptable_string = broccoli.replace("'", "\"")
        resp = json.loads(json_acceptable_string)
        """First test that un-parsed response contains unwanted data"""
        foodNutrients = [foodNutrients for foodNutrients in resp["foods"]][0]["foodNutrients"]
        lst = [nn["nutrientName"] for nn in foodNutrients]
        self.assertTrue("15:1" in lst)
        
        """Test parsed response does not contain unwanted data"""
        parsed_food = parse_food(resp)
        lst = [x[0] for x in parsed_food[0]["nutrients"]]
        self.assertFalse("15:1" in lst)
        
    
    
"""parse_food takes the raw data from the API and 
   strips away only the data required for this app
"""

def parse_food(food_dict):
    """Return dictionary of {nutrientName, value} filtering out any non-word nutrient names"""
    n_name = None
    n_value = None
    index = 0
    choices = []
    
    for elem in food_dict["foods"]:
        description = elem["description"]
        fdcId = elem["fdcId"]
        nutrients = {}
        for data_row in elem["foodNutrients"]:
            if not any(x.isdigit() for x in data_row["nutrientName"]):
                nutrients[data_row["nutrientName"]] = [data_row["value"], data_row["unitName"]]
                
        choices.append(
            {
                "fdcId": fdcId,
                "description": description,                
                "nutrients": nutrients
            }
        )
        
    return choices   
            
        
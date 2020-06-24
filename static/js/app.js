/**
 * ingredientDeleteButtonHandler - deletes menu item from display and also from cache collection
 */
const ingredientDeleteButtonHandler = (prod, amt) => {
    // remove ingredient values from cache
    cache.remove(amt, prod);
    // get updated cache
    const food = cache.get();
    // update the UI to display updated charted ingredients  
    doNutrientTableDisplay(food, 0);
}

/**
 * get_started - creates/updates the Nutrient Table and Food List on the getstarted page
 */
async function get_started() {
    const amt = document.getElementById("add-weight").value;
    const prod = document.getElementById("add-product").value;
    
    if(amt.length && prod.length) {
        let formError = document.querySelector(".form-error");
        if(!formError.classList.contains("hidden"))
            formError.classList.add("hidden");
        if(!cache.hasKey((prod+amt).toUpperCase())) {
            // wait for response from the server
            const resp = await getFoodFromServer(prod);//{"amt":amt, "prod":prod});
            // resp data contains a list of food descriptions
            let foodID = 0;
            let text = "";
            if(resp.status == 200) {
                let choices = Object.entries(resp.data);        
                if(choices.length > 1) {
                    // list of food descriptions contains more than one choice
                    // use a Modal to offer the user a choice between food titles
                    // wait for user to confirm selection
                    foodID = await foodChoiceModal(choices); 
                    text = `${amt}   -   ${resp.data[foodID]}`;           
                } else {
                    text = `${amt}   -   ${Object.values(resp.data)[0]}`;
                    foodID = Object.keys(resp.data)[0]
                }                  
            }
            if(foodID) {
                // after food choice is confirmed, get the food data from the server
                const food_nutrients = await getFoodFromServerCache(foodID);
                // cache the food nutrient data to a local cache food object
                cache.put(amt, prod, food_nutrients.data.nutrients)
                const food = cache.get();
                // update the UI to display charted ingredients
                doNutrientTableDisplay(food, 0);
                // update the UI to display new menu ingredient
                // updateFoodListDisplay(text, amt);
                doIngredientListDisplay(prod, amt);
                // clear user inputs
                clearInputs();    
                
            }
        } else {
            if(formError.classList.contains("hidden"))
                formError.classList.remove("hidden");
            clearInputs();
        }
    }   
    
}

const formControl = document.getElementById("control-form");
const formControlSave = document.getElementById("control-form-save");
const savedMenus = document.querySelector(".saved-menus");
const chart = document.querySelector(".control-chart");

/**
 * call the get_started() when "Add Ingredient" button is clicked
 */
if(formControl) {
    formControl.addEventListener("click", async e => {
        
        e.preventDefault();
        
        if(e.target.id == 'add-food-button') {        
            get_started();
        }
        if(chart.childElementCount > 1 && e.target.classList.contains("commit-food-button")){        
            formControl.classList.toggle("hidden");
            formControlSave.classList.toggle("hidden");
        }
    });
}

/**
 * call commitFoodToDB(food, menuName) when the "Save Recipe" button is clicked
 * commits the menu to the database
 */
if(formControlSave) {    
    formControlSave.addEventListener("click", async e => {
        e.preventDefault();
        if(e.target.classList.contains("commit-food-button")) {  
            let name = document.getElementById("add-menu-name");
            let res = await commitFoodToDB(cache.get(), name.value);
            cache = new FoodCache();

            const ul = document.querySelector(".control-display");
            while(ul.childElementCount > 1) {
                ul.removeChild(ul.lastChild);
            }
            while(chart.childElementCount > 1) {
                chart.removeChild(chart.lastChild);
            }
            formControl.classList.toggle("hidden");
            formControlSave.classList.toggle("hidden"); 
        }
    });
}

/**
 * removes item from the database
 */
if(savedMenus) {
    savedMenus.addEventListener("click", async e => {
        if(e.target.classList.contains("del-date")) {
            
            if(e.target.parentElement.firstChild.nextSibling.checked) {
                food = await getFoodFromServerById(e.target.id);
                
                cache.remove(0,0,food.data); 
                doNutrientTableDisplay(cache.get(), 0);
            }
            e.target.parentElement.remove();
            deleteFoodFromServerById(e.target.id)
        } else if(e.target.classList.contains("control-checkbox")) {
            food = await getFoodFromServerById(e.target.id);
            if(e.target.checked) {                
                cache.put(0,0,food.data);                
            } else {
                cache.remove(0,0,food.data);                
            }
            doNutrientTableDisplay(cache.get(), 0);
        }
    });
}

/**
 * Give the Nutrient table sort functionality
 */
let nutrientDir, weightDir = 0;
if(chart) {
    chart.addEventListener("click", e => {
        if(e.target.id == "nutrient" && listFood) {
            if(nutrientDir) {
                doNutrientTableDisplay(listFood, 0);
                nutrientDir = 0;
            } else {
                doNutrientTableDisplay(listFood, 1);
                nutrientDir = 1;
            }
        }
        if(e.target.id == "weight" && listFood) {
            if(weightDir) {
                doNutrientTableDisplay(listFood, 2);
                weightDir = 0;
            } else {
                doNutrientTableDisplay(listFood, 3);
                weightDir = 1;
            }
        }
    });
}


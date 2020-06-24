
/**
 * Create or update Menu Ingredients list
 */
const doIngredientListDisplay = (text, portion) => {
    const ul = document.querySelector(".control-display")
    let li = document.createElement("LI");
    let span = document.createElement("SPAN");
    let p1 = document.createElement("P");
    let p2 = document.createElement("P");
    let button = document.createElement("BUTTON");
    let toolTip = document.createElement("SPAN");

    span.className = "control-li";
    p1.className = "control-item";
    p2.className = "control-weight";
    button.className = "control-del";
    toolTip.className = "tooltiptext";

    p1.innerText = text.slice(text.indexOf('-')+1).toUpperCase().trim();
    p2.innerText = portion;
    button.innerText = "X";
    toolTip.innerText = "Delete Item";
    
    button.append(toolTip);
    span.append(p1);
    span.append(p2);
    span.append(button);
    li.append(span);
    ul.append(li);
    button.addEventListener("click", e => {
        const prod = e.target.parentElement.firstChild.innerText;
        const amt = e.target.previousSibling.innerText;
        ingredientDeleteButtonHandler(prod, amt)
        e.target.parentElement.remove();
    });
}

/**
 * Create or update Nutrient table
 */
let listFood = null;
const doNutrientTableDisplay = (food, sortDir) => {
    listFood = food;
    // remove all table elements
    while(chart.childElementCount > 1) {
        chart.removeChild(chart.lastChild);
    }
    let arr = Object.entries(food);
    // sort table (asc/desc) by name or value
    if(sortDir == 0) arr.sort();
    if(sortDir == 1) arr.sort().reverse();
    if(sortDir == 2) arr.sort((a,b) => standardizeUnit(...a[1])[0] - standardizeUnit(...b[1])[0]);
    if(sortDir == 3) arr.sort((a,b) => standardizeUnit(...b[1])[0] - standardizeUnit(...a[1])[0]);
    // add values to the table
    for([key, value] of arr) {
        let tr = document.createElement("TR");
        let d1 = document.createElement("TD");
        let d2 = document.createElement("TD");
        d2.className = "table-data-grams";
        d1.innerText = key;
        let [k, v] = standardizeUnit(...value);
        d2.innerText = k + " - " + v;
        // d2.innerText = value[0] + " - " + value[1];
        tr.append(d1);
        tr.append(d2);
        tr.id = "chart-row";
        chart.append(tr);
    }
}

const clearInputs = () => {
    document.querySelector("#add-weight").value = "";
    document.querySelector("#add-product").value = "";
}

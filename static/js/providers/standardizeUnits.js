/**
 * Standardize units of measure for display purposes only
 * Units will be set to mg for simplicity
 * Future improvements should add more complexity to units to include grams 
 */
const standardizeUnit = (value, unit) => {
    let UNIT = unit.toUpperCase();
    if(UNIT == "KG") value *= 1_000_000;
    else if(UNIT == "G") value *= 1_000;
    else if(UNIT == "UG") value /= 1_000;
    else if(UNIT != "MG")  return [parseFloat((+value).toFixed(4)), unit]
    return [parseFloat((+value).toFixed(4)), "mg"]
}
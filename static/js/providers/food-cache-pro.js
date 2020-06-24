
/**
 * FoodCache is a local temporary storage for front end display access
 */
class FoodCache {
    constructor() {
        this.cache = {
            each: {},
            all: {}
        };
    }
    hasKey(key) {
        return this.cache.each.hasOwnProperty(key);
    }
    get() {
        return this.cache.all;
    }
    put(amt, prod, values) {
        
        if(amt) {
            const key = (prod+amt).toUpperCase();
            this.cache.each[key] = values;
            for(let prop in values) {
                if(!this.cache.all.hasOwnProperty(prop)) {
                    this.cache.all[prop] = [0, values[prop][1]];
                }
                this.cache.each[key][prop][0] *= (amt/100);
                this.cache.all[prop][0] = (+this.cache.all[prop][0] + this.cache.each[key][prop][0]);
            }
        } else {
            for(let prop in values) {
                if(!this.cache.all.hasOwnProperty(prop)) {
                    this.cache.all[prop] = [0, values[prop][1]];
                }
                this.cache.all[prop][0] = (+this.cache.all[prop][0] + values[prop][0]);
            }
        }  
    }
    remove(amt, prod, values) {
        if(+amt > 0) {
            const key = (prod+amt).toUpperCase();
            delete this.cache.each[key];
            this.cache.all = {};
            for(let prop in this.cache.each) {
                for(let key in this.cache.each[prop]) {
                    if(!this.cache.all.hasOwnProperty(key)) {
                        this.cache.all[key] = [0, this.cache.each[prop][key][1]];
                    }
                    this.cache.all[key][0] += +this.cache.each[prop][key][0];
                }                            
            }          
        } else {
            for(let prop in values) {
                if(this.cache.all.hasOwnProperty(prop)) {
                    this.cache.all[prop][0] = (+this.cache.all[prop][0] - +values[prop][0]);
                    if(+this.cache.all[prop][0] < 0.0001 || isNaN(+this.cache.all[prop][0]))
                    delete this.cache.all[prop];
                }                
            }
        }        
    }
}
let cache = new FoodCache();
/** Interacts with the server to get/store/remove data */

const commitFoodToDB = (food, menuName) => {
    return new Promise((resolve, reject) => {
        axios({
            method: "post",
            url: "/save_data",
            data: { "food": food, "menuName": menuName }
        }).then(response =>{
            resolve(response);
        }).catch(error => {
            reject(error);
        });  
    });
}

const getFoodFromServer = food => { 
    return new Promise((resolve, reject) => {
        axios({
            method: "post",
            url: "/get_food_api",
            data: { "food": food }
        }).then(response =>{
            resolve(response);
        }).catch(error => {
            reject(error);
        });  
    });
}

const getFoodFromServerCache = food_id => {
    return new Promise((resolve, reject) => {
        axios({
            method: "post",
            url: "/get_food_cache",
            data: { "food_id": food_id }
        }).then(response =>{
            resolve(response);
        }).catch(error => {
            reject(error);
        });  
    });
}

const getFoodFromServerById = food_id => {
    return new Promise((resolve, reject) => {
        axios({
            method: "post",
            url: "/get_food_by_id",
            data: { "food_id": food_id }
        }).then(response =>{
            resolve(response);
        }).catch(error => {
            reject(error);
        });
    });
}

const deleteFoodFromServerById = food_id => {
    return new Promise((resolve, reject) => {
        axios({
            method: "post",
            url: "/delete_food_by_id",
            data: { "food_id": food_id }
        }).then(response =>{
            resolve(response);
        }).catch(error => {
            reject(error);
        });
    });
}

/**
 * foodChoiceModal is a popup Modal used when the API returns multiple food choices
 * foodList: Array of food choices/names
 */

const foodChoiceModal = foodList => {
    const optionsModal = document.querySelector("#options-modal");
    const modalUL = document.querySelector(".modal-ul");
    return new Promise((resolve, reject) => {
        while(modalUL.firstChild) {
            modalUL.removeChild(modalUL.lastChild);
        }
        for(let i in foodList) {
            const text = foodList[i][1];
            let li = document.createElement("LI");
            li.className = "modal-anchor";
            li.id = foodList[i][0];
            li.innerText = text;        
            modalUL.append(li);
            li.addEventListener("click", () =>{
                optionsModal.classList.toggle("hidden");
                resolve(foodList[i][0]);
            });
        }
        optionsModal.classList.toggle("hidden");    
    });

};

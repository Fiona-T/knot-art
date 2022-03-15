/**
 * If select box exists, then listen for change on this element
 * On change, get the current URL, get the value from the select option
 * If the value isn't 'reset', then get the sort and direction from select option value
 * And set these into the search parameters on the url, then put new url into window
 * Otherwise, clear any sort and direction so that all results will be shown
 * Credit: initial code from Code Institute, amended/refactored
 *  */ 

function selectBoxSorting() {
    if(document.getElementById("sorting-selector")) {
        document.getElementById("sorting-selector").addEventListener("change", function() {
            let currentUrl = new URL(window.location);
            if(this.value != "reset"){
                currentUrl.searchParams.set("sort", this.value.split("_")[0]);
                currentUrl.searchParams.set("direction", this.value.split("_")[1]);
                window.location.replace(currentUrl)
            } else {
                currentUrl.searchParams.delete("sort");
                currentUrl.searchParams.delete("direction");
                window.location.replace(currentUrl);
            }
        });
    }
}

/**
 * Listen for click event on btn_qty.
 * On click, prevent default, get the data-item_id from the element, and get
 * the direction (increment or decrement) from the id of the element.
 * Call changeInputValue function, passing itemId and direction of change.
 *  */ 
function quantityButtons() {
    if(document.querySelectorAll(".btn-qty")){
        let quantityBtns = document.querySelectorAll(".btn-qty");
        quantityBtns.forEach(btn => btn.addEventListener("click", function(event) {
            event.preventDefault();
            let itemId = this.getAttribute("data-item_id");
            let direction = this.getAttribute("id").split("-")[0];
            changeInputValue(itemId, direction);
        }));
    }
}

/**
 * Change the value in the input box, either up or down depending on direction
 * @param {string} itemId the id of the product, to get the relevant input element
 * @param {string} direction - direction of change, either increment or decrement
 */
function changeInputValue(itemId, direction) {
    let inputElement = document.getElementById(`id_qty_${itemId}`);
    let oldValue = parseInt(inputElement.value);
    if(direction === "decrement") {
        inputElement.value = -- oldValue;
    } else if(direction === "increment") {
        inputElement.value = ++ oldValue;
    }
}


/** initialise the sorting options in select dropdown on products page, 
 * and quantity buttons in product details/cart */
document.addEventListener("DOMContentLoaded", function () {
    selectBoxSorting();
    quantityButtons();
});
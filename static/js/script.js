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
 * If btn_qty exists, then listen for click on either increment or decrement btns.
 * On click, prevent default, then get the data-item_id from the element, use this id
 * to get the input element by id (each input/button has the product id on it)
 * Increase or decrease the current value by 1.
 * Credit: initial code from Code Institute, amended/refactored.
 *  */ 
function quantityButtons() {
    if(document.querySelectorAll(".btn-qty")){
        let incrementBtn = document.querySelectorAll(".increment-qty");
        incrementBtn.forEach(button => button.addEventListener("click", function (event) {
            event.preventDefault();
            let item_id = this.getAttribute("data-item_id");
            let input_element = document.getElementById(`id_qty_${item_id}`)
            let old_value = parseInt(input_element.value);
            input_element.value = ++ old_value;
        }));

        let decrementBtn = document.querySelectorAll(".decrement-qty");
        decrementBtn.forEach(button => button.addEventListener("click", function (event) {
            event.preventDefault();
            let item_id = this.getAttribute("data-item_id");
            let input_element = document.getElementById(`id_qty_${item_id}`)
            let old_value = parseInt(input_element.value);
            input_element.value = -- old_value;
        }));
    }
}

/** initialise the sorting options in select dropdown on products page, 
 * and quantity buttons in product details/cart */
document.addEventListener("DOMContentLoaded", function () {
    selectBoxSorting();
    quantityButtons();
});
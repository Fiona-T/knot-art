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

/** initialise the sorting options in select dropdown on products page */
document.addEventListener("DOMContentLoaded", function () {
    selectBoxSorting();
});
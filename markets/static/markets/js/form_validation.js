/**
 * This file contains functions to validate the date and time inputs on the MarketForm
 */

/**
 * Listen for change on date input, if it is earlier than today then add invalid class.
 * Else, remove invalid class (so previous errors are cleared)
 */
function checkMarketDate() {
    document.getElementById("id_date").addEventListener("change", function() {
        let form_date = this.value;
        let today = new Date().toISOString().slice(0, 10)
        if (form_date < today) {
            addInvalidClasses("id_date");
        } else {
            removeInvalidClasses("id_date");
        }
    });
}

/**
 * Listen for change on time inputs, if values in both, check if start time later than end time.
 * If it is, add invalid class, else, remove invalid class (so previous errors are cleared)
 */
function checkStartAndEndTimes() {
    let timeInputs = document.querySelectorAll(".time-input")
    for (let input of timeInputs) {
        input.addEventListener("change", function() {
            let start_time = document.getElementById("id_start_time").value;
            let end_time = document.getElementById("id_end_time").value;
            if (start_time && end_time) {
                if (start_time > end_time) {
                    addInvalidClasses("id_start_time", "id_end_time");
                } else {
                    removeInvalidClasses("id_start_time", "id_end_time");
                }
            }
        })
    }
}

/**
 * Add invalid class to each input + helptext for the ids passed in (and remove text muted so helptext can be bolded)
 * Helptext will exist on form before sending to server but is removed if errors on server side validation,
 * hence the need to check if helptext exists. 
 * @param  {...any} fieldIds the ids of the inputs, to get the relevant input element + the associated helptext
 */
function addInvalidClasses(...fieldIds) {
    fieldIds.forEach(fieldId => {
        document.getElementById(`${fieldId}`).classList.add("is-invalid");
        if(document.getElementById(`hint_${fieldId}`)) {
            document.getElementById(`hint_${fieldId}`).classList.add("invalid-text");
            document.getElementById(`hint_${fieldId}`).classList.remove("text-muted");
        }
    });
}

// remove invalid class from Input and Helptext if it exists (so errors go away after updating)
/**
 * Remove invalid classes from each input + helptext for the ids passed in (so errors go away after updating).
 * Helptext will exist on form before sending to server but is removed if errors on server side validation,
 * hence the need to check if helptext exists. 
 * @param  {...any} fieldIds the ids of the inputs, to get the relevant input element + the associated helptext
 */
function removeInvalidClasses(...fieldIds) {
    fieldIds.forEach(fieldId => {
        document.getElementById(`${fieldId}`).classList.remove("is-invalid");
        if(document.getElementById(`hint_${fieldId}`)) {
            document.getElementById(`hint_${fieldId}`).classList.remove("invalid-text")
            document.getElementById(`hint_${fieldId}`).classList.add("text-muted")
        }
    });
}

/** initialise the form inputs to listen for change events
*/
document.addEventListener("DOMContentLoaded", function () {
    checkMarketDate();
    checkStartAndEndTimes();
});
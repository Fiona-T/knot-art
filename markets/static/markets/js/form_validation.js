        // listen for change on market date field, check if earlier than today, add invalid class or remove it
        document.getElementById("id_date").addEventListener("change", function() {
            let form_date = this.value;
            let today = new Date().toISOString().slice(0, 10)
            if (form_date < today) {
                addInvalidClasses("id_date");
            } else {
                removeInvalidClasses("id_date");
            }
        });
        // listen for change on time inputs, check if both times exist, and if start time later than end time, add invalid class or remove it
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

        // add invalid class to Input and to Helptext if it exists
        function addInvalidClasses(...fieldIds) {
            console.log("inside new function");
            fieldIds.forEach(fieldId => {
                document.getElementById(`${fieldId}`).classList.add("is-invalid");
                if(document.getElementById(`hint_${fieldId}`)) {
                    document.getElementById(`hint_${fieldId}`).classList.add("invalid-text")
                    document.getElementById(`hint_${fieldId}`).classList.remove("text-muted")
                }
            });
        }

        // remove invalid class from Input and Helptext if it exists (so errors go away after updating)
        function removeInvalidClasses(...fieldIds) {
            console.log("inside new remove function");
            fieldIds.forEach(fieldId => {
                document.getElementById(`${fieldId}`).classList.remove("is-invalid");
                if(document.getElementById(`hint_${fieldId}`)) {
                    document.getElementById(`hint_${fieldId}`).classList.remove("invalid-text")
                    document.getElementById(`hint_${fieldId}`).classList.add("text-muted")
                }
            });
        }
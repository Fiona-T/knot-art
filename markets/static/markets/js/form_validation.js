        // listen for change on market date field, check if earlier than today, add invalid class or remove it
        document.getElementById("id_date").addEventListener("change", function() {
            let form_date = this.value;
            let today = new Date().toISOString().slice(0, 10)
            if (form_date < today) {
                addInvalid(this, "id_date");
            } else {
                removeInvalid(this, "id_date");
            }
        });
        // listen for change on start time, check if end time, and if later than end time, add invalid class or remove it
        document.getElementById("id_start_time").addEventListener("change", function() {
            let start_time = this.value;
            if (document.getElementById("id_end_time").value) {
                let end_time = document.getElementById("id_end_time").value;
                if (start_time > end_time) {
                    addInvalid(this, "id_start_time");
                } else {
                    removeInvalid(this, "id_start_time");
                }
            } 
        });
        // listen for change on end time, check if start time, and if earlier than start time, add invalid class or remove it
        document.getElementById("id_end_time").addEventListener("change", function() {
            let end_time = this.value;
            if(document.getElementById("id_start_time").value) {
                let start_time = document.getElementById("id_start_time").value;
                if(start_time > end_time) {
                    addInvalid(this, "id_end_time");
                } else {
                    removeInvalid(this, "id_end_time");
                }
            } 
        });

        // add invalid class to Input and to Helptext if it exists
        function addInvalid(element, fieldId) {
            element.classList.add("is-invalid");
                if(document.getElementById(`hint_${fieldId}`)) {
                    document.getElementById(`hint_${fieldId}`).classList.add("invalid-text");
                    document.getElementById(`hint_${fieldId}`).classList.remove("text-muted");
                }
        }

        // remove invalid class from Input and Helptext if it exists (so errors go away after updating)
        function removeInvalid(element, fieldId) {
            element.classList.remove("is-invalid");
                if(document.getElementById(`hint_${fieldId}`)) {
                    document.getElementById(`hint_${fieldId}`).classList.remove("invalid-text");
                    document.getElementById(`hint_${fieldId}`).classList.add("text-muted");
                }
        }
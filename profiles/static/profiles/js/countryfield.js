// get value of country field when page loads
let countrySelected = $('#id_default_country').val();
// it will be emtpy string (false) if first option is selected
// if it's false, set it to grey placeholder color
if(!countrySelected) {
    $('#id_default_country').css('color', '#6c757d');
};
// capture the change event, when it changes, get the value
$('#id_default_country').change(function() {
    countrySelected = $(this).val();
    // if it's false then set to grey placeholder, otherwise to black
    if(!countrySelected) {
        $(this).css({'color': '#6c757d', 'font-weight': '100', 'font-size': '90%'});
    } else {
        $(this).css({'color': '#000', 'font-weight': '400', 'font-size': '1rem'});
    }
});
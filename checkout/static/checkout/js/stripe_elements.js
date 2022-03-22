/*
    Core logic/payment flow comes from:
    https://stripe.com/docs/payments/accept-a-payment
    Options for style object from: https://stripe.com/docs/js/appendix/style
    Credit to Code Institute for form submit part.
*/

// get the text from the script elements, and slice off the quotation marks
const stripePublicKey = $("#id_stripe_public_key").text().slice(1, -1);
const clientSecret = $("#id_client_secret").text().slice(1, -1);

// create instance of stripe using public key
const stripe = Stripe(stripePublicKey);

// create instance of stripe elements
const elements = stripe.elements();

// set the style in style object
const style = {
    base: {
        color: "#000",
        iconColor: '#ff8881',
        fontFamily: "Overpass, sans-serif",
        fontWeight: '100',
        fontSmoothing: "antialiased",
        fontSize: '15px',
        '::placeholder': {
            color: "#6c757d",
        }
    },
    invalid: {
        color: '#dc3545',
        iconColor: '#dc3545'
    }
};
// create a card element (in stripe docs referred to as paymentElement)
const card = elements.create('card', {style: style});
// mount the card element to the div in the checkout.html file
card.mount('#card-element');

// handle realtime validation errors on the card element & display errors in card-errors div
card.addEventListener('change', function(event) {
    let errorDiv = document.getElementById('card-errors');
    if (event.error) {
        let html = `
        <span role="alert">
            <i class="bi bi-x-lg" aria-hidden="true"></i>
        </span>
        <span>${event.error.message}</span>
        `;
        $(errorDiv).html(html);
    } else {
        errorDiv.textContent = '';
    }
});

// Handle form submit
const form = document.getElementById('payment-form');
form.addEventListener('submit', function(ev) {
    ev.preventDefault();
    // disable card element and submit btn to prevent multiple submissions
    card.update({ 'disabled': true});
    $('#submit-button').attr('disabled', true);
    // fade out the form and trigger the overlay
    $('#payment-form').fadeToggle(100);
    $('#loading-overlay').fadeToggle(100);

    // get Boolean value of savinfo box by looking at its checked attribute
    let saveInfo = Boolean($('#id-save-info').attr('checked'));
    // Get value of csrf token from using {% csrf_token %} in the form
    let csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
    // info to post to the cache_checkout_data view, at the url below
    let postData = {
        'csrfmiddlewaretoken': csrfToken,
        'client_secret': clientSecret,
        'save_info': saveInfo,
    };
    // posting here triggers the cache_checkout_data view to add cart to meta data
    let url = '/checkout/cache_checkout_data/';
    // after posting to cache_checkout_data, wait for 200 response from the view
    $.post(url, postData).done(function() {
        // then call confirm card payment method, providing the card + form details to stripe,
        // then executethe function on the result
        stripe.confirmCardPayment(clientSecret, {
            payment_method: {
                card: card,
                billing_details: {
                    name: $.trim(form.full_name.value),
                    phone: $.trim(form.phone_number.value),
                    email: $.trim(form.email.value),
                    address:{
                        line1: $.trim(form.street_address1.value),
                        line2: $.trim(form.street_address2.value),
                        city: $.trim(form.town_or_city.value),
                        country: $.trim(form.country.value),
                        state: $.trim(form.county.value),
                    }
                }
            },
            shipping: {
                name: $.trim(form.full_name.value),
                phone: $.trim(form.phone_number.value),
                address: {
                    line1: $.trim(form.street_address1.value),
                    line2: $.trim(form.street_address2.value),
                    city: $.trim(form.town_or_city.value),
                    country: $.trim(form.country.value),
                    postal_code: $.trim(form.postcode.value),
                    state: $.trim(form.county.value),
                }
            },
        }).then(function(result) {
            // show errors
            if (result.error) {
                let errorDiv = document.getElementById('card-errors');
                let html = `
                    <span class="icon" role="alert">
                    <i class="bi bi-x-lg" aria-hidden="true"></i>
                    </span>
                    <span>${result.error.message}</span>`;
                $(errorDiv).html(html);
                // fade in the form again and remove overlay so errors can be fixed
                $('#payment-form').fadeToggle(100);
                $('#loading-overlay').fadeToggle(100);
                // re-enable the card element and the submit btn so error can be fixed
                card.update({ 'disabled': false});
                $('#submit-button').attr('disabled', false);
            } else {
                // payment successful, submit the form (prevented above)
                if (result.paymentIntent.status === 'succeeded') {
                    form.submit();
                }
            }
        });
    }).fail(function() {
        // if cache_checkout_data view returns 400 response - reload page
        location.reload();
    })
});

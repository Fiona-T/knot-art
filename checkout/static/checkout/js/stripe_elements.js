/*
    Core logic/payment flow comes from:
    https://stripe.com/docs/payments/accept-a-payment
    Options for style object from: https://stripe.com/docs/js/appendix/style
    Also credit to Code Institute.
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

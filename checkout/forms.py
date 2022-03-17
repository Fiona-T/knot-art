"""Order form for checkout app"""
from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    """form for customer details, delivery details"""
    class Meta:
        """
        Form based on Order model, but only need to display the fields
        the user must complete. The others are calculated automatically.
        """
        model = Order
        fields = ('full_name', 'email', 'phone_number',
                  'street_address1', 'street_address2',
                  'town_or_city', 'postcode', 'country',
                  'county',)
        labels = {
            'street_address1': 'Street address 1',
            'street_address2': 'Street address 2',
        }

    def __init__(self, *args, **kwargs):
        """
        Override init method to add placeholders for some fields
        add class for CSS, set autofocus on first field
        """
        super().__init__(*args, **kwargs)
        placeholders = {
            'email': 'example@example.com',
            'postcode': 'Postal Code or Eircode',
            'county': 'County, State or Locality',
        }
        self.fields['full_name'].widget.attrs['autofocus'] = True
        for field in self.fields:
            if field in placeholders.keys():
                self.fields[field].widget.attrs['placeholder'] = (
                    placeholders[field]
                    )
            self.fields[field].widget.attrs['class'] = 'order-form-input'

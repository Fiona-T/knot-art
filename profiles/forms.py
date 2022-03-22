"""Order form for checkout app"""
from django import forms
from .models import UserProfile


class UserProfileForm(forms.ModelForm):
    """form for default delivery details on user profile"""
    class Meta:
        """
        Form based on UserProfile model, but exclude user as this
        will not change (it's linked to User model).
        """
        model = UserProfile
        exclude = ('user',)
        labels = {
            'default_street_address1': 'Street address 1',
            'default_street_address2': 'Street address 2',
        }

    def __init__(self, *args, **kwargs):
        """
        Override init method to add placeholders for some fields
        add class for CSS, set autofocus on first field
        """
        super().__init__(*args, **kwargs)
        placeholders = {
            'postcode': 'Postal Code or Eircode',
            'county': 'County, State or Locality',
        }
        self.fields['default_phone_number'].widget.attrs['autofocus'] = True
        for field in self.fields:
            if field in placeholders.keys():
                self.fields[field].widget.attrs['placeholder'] = (
                    placeholders[field]
                    )
            self.fields[field].widget.attrs['class'] = 'order-form-input'

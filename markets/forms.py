"""Forms for 'markets' app"""
from django import forms
from products.widgets import CustomClearableFileInput
from .models import Market, County


class MarketForm(forms.ModelForm):
    """
    Market form for admin user to add/edit market from frontend.
    Image field - uses custom file input widget that overrides Django one
    """
    class Meta:
        """
        Form based on Market model.
        Helptexts and labels specified for some fields.
        """
        model = Market
        fields = (
            'name', 'location', 'county', 'date', 'start_time', 'end_time',
            'image', 'website',
        )
        labels = {
            'name': 'Market Name',
        }
        help_texts = {
            'date': 'Cannot be in the past, only markets with today\'s date '
            'or later are shown to users',
            'start_time': 'Must be before End Time!',
            'end_time': 'Must be after Start Time!',
            'website': 'Use social media link if market does not have website',
            }
        widgets = {
            'date': forms.DateInput(
                format=('%Y-%m-%d'),
                attrs={'type': 'date'}
                ),
            'start_time': forms.TimeInput(
                format=('%H:%M'),
                attrs={'type': 'time'}
                ),
            'end_time': forms.TimeInput(
                format=('%H:%M'),
                attrs={'type': 'time'}
                ),
            }

    image = forms.ImageField(
        label='Image', required=False, widget=CustomClearableFileInput
        )

    def __init__(self, *args, **kwargs):
        """
        Override init method to make changes to fields:
        Create tuple of county ids and friendly names, use this to set the
        choices in the County field dropdown. Add CSS class to all fields.
        """
        super().__init__(*args, **kwargs)
        counties = County.objects.all()
        friendly_names = [(c.id, c.get_friendly_name()) for c in counties]
        self.fields['county'].choices = friendly_names
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'order-form-input'

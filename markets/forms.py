"""Forms for 'markets' app"""
import datetime
from django import forms
from django.core.exceptions import ValidationError
from products.widgets import CustomClearableFileInput
from .models import Market, County, Comment


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
            'date': 'Cannot be in the past. Only markets with today\'s date '
            'or later are shown to users in the Upcoming Markets page',
            'start_time': 'Must be before End time!',
            'end_time': 'Must be after Start time!',
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
        Add time-input class for time fields, to be used by JS validation.
        Amend the helptext on date field if existing date in past.
        """
        super().__init__(*args, **kwargs)
        counties = County.objects.all()
        friendly_names = [(c.id, c.get_friendly_name()) for c in counties]
        self.fields['county'].choices = friendly_names
        self.fields['county'].choices.insert(
            0, ('', 'Choose county, or Dublin postcode')
            )
        for field in self.fields:
            if field == 'start_time' or field == 'end_time':
                self.fields[field].widget.attrs['class'] = (
                    'brand-form-input time-input')
            else:
                self.fields[field].widget.attrs['class'] = 'brand-form-input'

        today = datetime.date.today()
        if self.instance.date:
            if self.instance.date < today:
                date = self.instance.date.strftime('%d/%m/%Y')
                self.fields['date'].help_text = (
                    f'Editing a past market dated {date}. If you are amending '
                    'the date it can only be changed to a future date.')

    def clean(self):
        """
        Override the clean method on form to include checks on date and times.
        Date not earlier than today, unless it is equal to existing date,
        start time must be before end time.
        Raise errors on field + remove helptext (as error msgs are similar).
        """
        cleaned_data = super().clean()
        market_date = cleaned_data.get('date')
        today = datetime.date.today()
        existing_date = self.instance.date
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')

        if start_time and end_time:
            if end_time < start_time:
                self.add_error(
                    'end_time',
                    ValidationError('End time must be after Start time')
                    )
                self.add_error(
                    'start_time',
                    ValidationError('Start time must be before End time')
                    )
                for fieldname in ['end_time', 'start_time']:
                    self.fields[fieldname].help_text = None

        if market_date:
            if market_date < today and market_date != existing_date:
                self.add_error(
                    'date',
                    ValidationError('Market date must not be in the past')
                    )
                self.fields['date'].help_text = None


class CommentForm(forms.ModelForm):
    """
    Comment form to add comments on markets
    """
    class Meta:
        """
        Form based on Comment model.
        Other fields - author, market and created_on are set in view
        """
        model = Comment
        fields = ('comment', )
        labels = {'comment': 'Your comment', }

    def __init__(self, *args, **kwargs):
        """
        Override init method to add number of rows + maxlength for textarea
        field and add CSS class.
        """
        super().__init__(*args, **kwargs)
        self.fields['comment'].widget.attrs = {'rows': 5, 'maxlength': 1000}
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'brand-form-input'

    def clean(self):
        """
        Override the clean method on form to include check on textarea field.
        Raise error on comment field if length is too long. As Django doesn't
        do a check for maxlength on this field type.
        """
        cleaned_data = super().clean()
        comment = cleaned_data.get('comment')
        if comment:
            if len(comment) >= 1005:
                self.add_error(
                        'comment',
                        ValidationError(
                            'Comment is too long. Please shorten and re-submit'
                        )
                    )

"""Tests for forms in markets app"""
import datetime
from django.test import TestCase
from django.contrib.auth.models import User
from .forms import MarketForm, CommentForm
from .models import County, Market


class TestMarketForm(TestCase):
    """Tests for the MarketForm"""
    @classmethod
    def setUpTestData(cls):
        """Set up past market instance for testing editing past market"""
        County.objects.create(
            name='dublin_3',
            friendly_name='Dublin 3'
        )
        today = datetime.date.today()
        Market.objects.create(
            name='The Craft Market',
            location='The Street',
            county=County.objects.get(id=1),
            date=today - datetime.timedelta(days=1),
            start_time='09:00',
            end_time='17:00',
            website='www.crafted.ie',
        )

    def test_explicitly_set_field_labels_exist(self):
        """
        Check labels are present for the fields where a label was explicitly
        set in the form Meta class
        """
        form = MarketForm()
        self.assertTrue(
            form.fields['name'].label is None or
            form.fields['name'].label == 'Market Name'
            )

    def test_helptext_exists_and_correct_where_set_in_meta_class(self):
        """
        Test helptext present and correct on fields that should have it
        """
        form = MarketForm()
        help_texts = {
            'date': 'Cannot be in the past, only markets with today\'s date '
            'or later are shown to users',
            'start_time': 'Must be before End time!',
            'end_time': 'Must be after Start time!',
            'website': 'Use social media link if market does not have website',
            }
        for field in form.fields:
            if field in help_texts.keys():
                self.assertEqual(
                    form.fields[field].help_text, help_texts[field])

    def test_helptext_correct_when_editing_past_market(self):
        """
        Instantiate form for existing market with a date in the past, confirm
        helptext is as expected.
        """
        market = Market.objects.get(id=1)
        form = MarketForm(instance=market)
        date = market.date.strftime('%d/%m/%Y')
        self.assertEqual(
            form.fields['date'].help_text,
            f'Editing a past market dated {date}. If you are amending '
            'the date it can only be changed to a future date.'
            )

    def test_css_class_exists_on_fields(self):
        """Test CSS classes are present and correct on the form fields"""
        form = MarketForm()
        for field in form.fields:
            if field == 'start_time' or field == 'end_time':
                self.assertEqual(
                    form.fields[field].widget.attrs['class'],
                    'order-form-input time-input'
                    )
            else:
                self.assertEqual(
                    form.fields[field].widget.attrs['class'],
                    'order-form-input'
                    )

    def test_required_fields_are_required(self):
        """
        Check form is not valid if required fields are blank.
        Test required fields are in form errors, not required not.
        Check error message exists for each required field.
        """
        form = MarketForm({
            'name': '',
            'location': '',
            'county': '',
            'date': '',
            'start_time': '',
            'end_time': '',
            'image': '',
            'website': '',
        })

        required_fields = [
            'name',
            'location',
            'county',
            'date',
            'start_time',
            'end_time',
            'website',
            ]
        for field in required_fields:
            self.assertIn(field, form.errors.keys())
            self.assertEqual(form.errors[field][0], 'This field is required.')

        not_required_fields = ['image', ]
        for field in not_required_fields:
            self.assertNotIn(field, form.errors.keys())

    def test_custom_widget_exists_on_image_field(self):
        """Check that image field has CustomClearableFileInput widget"""
        form = MarketForm()
        self.assertEqual(
            form.fields['image'].widget.__class__.__name__,
            'CustomClearableFileInput'
            )

    def test_widget_exists_on_date_field(self):
        """Test that date field has DateInput widget attached"""
        form = MarketForm()
        self.assertEqual(
            form.fields['date'].widget.__class__.__name__, 'DateInput'
            )

    def test_widget_exists_on_time_fields(self):
        """Test that time fields have TimeInput widget attached"""
        form = MarketForm()
        self.assertEqual(
            form.fields['start_time'].widget.__class__.__name__, 'TimeInput'
            )
        self.assertEqual(
            form.fields['end_time'].widget.__class__.__name__, 'TimeInput'
            )

    def test_end_time_before_start_time_raises_error_message(self):
        """
        Create form instance with end time earlier than start time, check
        it is not valid. Check that the two fields are in the keys of the form
        errors dict. Check that the error returned is correct.
        """
        form = MarketForm({
            'name': 'my market',
            'county': 1,
            'location': 'the street',
            'date': '2022-10-01',
            'start_time': '17:00',
            'end_time': '11:00',
            'website': 'http://www.website.ie',
        })
        self.assertFalse(form.is_valid())
        self.assertIn('start_time', form.errors.keys())
        self.assertIn('end_time', form.errors.keys())
        self.assertEqual(
            form.errors['start_time'][0],
            'Start time must be before End time'
            )
        self.assertEqual(
            form.errors['end_time'][0],
            'End time must be after Start time'
            )

    def test_date_before_today_raises_error_message(self):
        """
        Create form instance with date earlier than today's date, check
        it is not valid. Check that the field is in the keys of the form
        errors dict. Check that the error returned is correct.
        """
        today = datetime.date.today()
        form = MarketForm({
            'name': 'my market',
            'county': 1,
            'location': 'the street',
            'date': today - datetime.timedelta(days=1),
            'start_time': '11:00',
            'end_time': '17:00',
            'website': 'http://www.website.ie',
        })
        self.assertFalse(form.is_valid())
        self.assertIn('date', form.errors.keys())
        self.assertEqual(
            form.errors['date'][0],
            'Market date must not be in the past'
            )

    def test_editing_past_market_does_not_raise_date_error_message(self):
        """
        Instantiate form for existing market with a date in the past, confirm
        the date error message is not raised.
        """
        market = Market.objects.get(id=1)
        form = MarketForm(instance=market)
        self.assertNotIn('date', form.errors.keys())

    def test_fields_are_explicit_in_form_metaclass(self):
        """
        Check the Meta fields attribute is equal to the list of fields
        defined in the form Meta innerclass
        """
        form = MarketForm()
        self.assertEqual(
            form.Meta.fields, (
                'name', 'location', 'county', 'date', 'start_time', 'end_time',
                'image', 'website',
                )
            )


class TestCommentForm(TestCase):
    """Tests for the CommentForm"""
    @classmethod
    def setUpTestData(cls):
        """Set up user, county and market instance for comments"""
        test_user = User.objects.create_user(
            username='User',
            password='secret12',
        )
        test_user.save()

        County.objects.create(
            name='dublin_3',
            friendly_name='Dublin 3'
        )
        today = datetime.date.today()
        Market.objects.create(
            name='The Craft Market',
            location='The Street',
            county=County.objects.get(id=1),
            date=today,
            start_time='09:00',
            end_time='17:00',
            website='www.crafted.ie',
        )

    def test_explicitly_set_field_labels_exist(self):
        """
        Check labels are present for the fields where a label was explicitly
        set in the form Meta class
        """
        form = CommentForm()
        self.assertTrue(
            form.fields['comment'].label is None or
            form.fields['comment'].label == 'Your comment'
            )

    def test_css_class_exists_on_fields(self):
        """Test CSS classes are present and correct on the form field"""
        form = CommentForm()
        for field in form.fields:
            self.assertEqual(
                form.fields[field].widget.attrs['class'], 'order-form-input')

    def test_widgets_exist_on_comment_field(self):
        """
        Check comment field has Textarea widget and this has the rows and
        maxlength attributes set on it.
        """
        form = CommentForm()
        self.assertEqual(form.fields['comment'].widget.attrs['rows'], 5)
        self.assertEqual(
            form.fields['comment'].widget.attrs['maxlength'], 1000
            )
        self.assertEqual(
            form.fields['comment'].widget.__class__.__name__, 'Textarea'
            )

    def test_required_fields_are_required(self):
        """
        Check form is not valid if comment field is blank. Comment field
        is the only field on the form and is required.
        Check error message exists for this field.
        """
        form = CommentForm({
            'comment': '',
        })

        self.assertIn('comment', form.errors.keys())
        self.assertEqual(form.errors['comment'][0], 'This field is required.')

    def test_too_long_comment_raises_error_message(self):
        """
        Create form instance with comment which is too long, check form is not
        valid. Check that the field is in the keys of the form errors dict.
        Check that the error returned is correct.
        """
        comment = 'and on ' * 1000
        form = CommentForm({
            'author': User.objects.get(id=1),
            'market': Market.objects.get(id=1),
            'comment': comment,
        })
        self.assertFalse(form.is_valid())
        self.assertIn('comment', form.errors.keys())
        self.assertEqual(
            form.errors['comment'][0],
            'Comment is too long. Please shorten and re-submit'
            )

    def test_fields_are_explicit_in_form_metaclass(self):
        """
        Check the Meta fields attribute is equal to the list of fields
        defined in the form Meta innerclass
        """
        form = CommentForm()
        self.assertEqual(form.Meta.fields, ('comment', ))

"""
Override of widget for products app.
Credit: Code Institute
"""
from django.forms.widgets import ClearableFileInput
from django.utils.translation import gettext_lazy as _


class CustomClearableFileInput(ClearableFileInput):
    """
    Overrides to ClearableFileInput for file upload form field:
    Put new values for checkbox label, initial text and input text
    Use our template.
    """
    clear_checkbox_label = _('Remove')
    initial_text = _('Current Image')
    input_text = _('')
    template_name = 'products/custom_widget_templates/custom_clearable_file_input.html'

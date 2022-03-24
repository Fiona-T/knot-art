"""Forms for 'products' app - shop"""
from django import forms
from .models import Product, Category


class ProductForm(forms.ModelForm):
    """Product form for admin user to add/edit product from frontend"""
    class Meta:
        """
        Form based on Product model.
        Helptexts and labels specified for some fields.
        """
        model = Product
        fields = '__all__'
        labels = {
            'is_active': 'Active product?',
            'is_new': 'New product?',
        }
        help_texts = {
            'name': 'Product name must be unique',
            'is_active': 'Only active products are visible in the shop to '
            'users. Leave un-checked if product not ready to be shown in shop',
            'is_new': 'A "New!" badge will be shown on the product if this '
            'is ticked',
            }

    def __init__(self, *args, **kwargs):
        """
        Override init method to make changes to fields:
        Create tuple of category ids and friendly names, use this to set the
        choices in the category field dropdown. Add css class to all fields.
        """
        super().__init__(*args, **kwargs)
        categories = Category.objects.all()
        friendly_names = [(c.id, c.get_friendly_name()) for c in categories]
        self.fields['category'].choices = friendly_names
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'order-form-input'

"""
config for checkout app - added function to override ready
method, to import signals module - used to listen for signals
from OrderLineItem instance to call method to update Order instance
"""
from django.apps import AppConfig


class CheckoutConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'checkout'

    def ready(self):
        """ override ready method - import signals module """
        import checkout.signals

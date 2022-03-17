"""
To listen for signals from OrderLineItem - when instance of this model
is saved or deleted. Then call the update_total method on the Order
instance that the lineitem relates to, so that the totals in the Order
instance get updated.
"""
# signals are sent after (post) a model is saved or deleted
from django.db.models.signals import post_save, post_delete
# to rececive the signals
from django.dispatch import receiver
from .models import OrderLineItem


@receiver(post_save, sender=OrderLineItem)
def update_on_save(sender, instance, created, **kwargs):
    """
    Handles signals from the post_save event
    When lineitem updated/created, update the order total
    """
    instance.order.update_total()


@receiver(post_delete, sender=OrderLineItem)
def update_on_delete(sender, instance, **kwargs):
    """
    Handles signals from the post_delete event
    When lineitem deleted, update the order total
    """
    instance.order.update_total()

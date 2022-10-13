from django.dispatch import receiver
from django.shortcuts import get_object_or_404
from paystack.api.signals import payment_verified

from .models import Rent


@receiver(payment_verified)
def on_payment_verified(sender, ref, amount, order, **kwargs):
    """
    ref: paystack reference sent back.
    amount: amount in Naira.
    order: paystack id tied to the user rent id.
    """
    get_rent = get_object_or_404(Rent, paystack_id=order)
    get_rent.paid = True
    get_rent.is_available = False
    get_rent.save()

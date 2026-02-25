from django import forms
from .models import Payment

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = [
            'shipment_id',
            'payer_id',
            'amount',
            'payment_method',
            'payment_status',
            'transaction_reference'
        ]
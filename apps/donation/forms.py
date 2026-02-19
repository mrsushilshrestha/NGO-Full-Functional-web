from django import forms
from .models import Donation


class DonationForm(forms.Form):
    amount = forms.DecimalField(min_value=1, max_digits=10, decimal_places=2)
    donor_name = forms.CharField(max_length=200, required=False)
    donor_email = forms.EmailField(required=False)
    payment_method = forms.ChoiceField(
        choices=[('esewa', 'eSewa'), ('khalti', 'Khalti'), ('bank', 'Bank Transfer')]
    )

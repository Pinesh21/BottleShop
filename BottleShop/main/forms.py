from .models import ProductReview
from django import forms
# from django.forms import Textarea
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget

class ReviewAdd(forms.ModelForm):
	class Meta:
		model=ProductReview
		fields=('review_text','review_rating')


class CheckoutForm (forms.Form):
    # Following form is to get shipping info for order/customer

    street_address = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': '1234 Main St',
        'id': 'address',
        'class': 'form-control'
    }))
    apartment_address = forms.CharField(required=False,widget=forms.TextInput(attrs={
        'placeholder': 'apartment or suits',
        'id': 'address-2',
        'class': 'form-control'
    }))
    country = CountryField(blank_label=('select country')).formfield(required=True, widget=CountrySelectWidget( attrs={
        'class': 'custom-select d-block w-100',
        'id': 'country'
    }))
    zip = forms.CharField(required=True,widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'zip',
        'placeholder': ''
    }))
    same_billing_address = forms.BooleanField(required=False,widget=forms.CheckboxInput)
    save_info = forms.BooleanField(required=False,widget=forms.CheckboxInput)
    payment_option = forms.ChoiceField(widget=forms.RadioSelect(), choices=[(1, 'Stripe'), (2, 'PayPal')])

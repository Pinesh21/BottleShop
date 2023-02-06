from django.contrib.auth.forms import UserCreationForm
from django import forms
from main.models import UserAddressBook
from django.contrib.auth.models import User


class SignupForm(UserCreationForm):
    mobile  =forms.CharField(widget=forms.TextInput(attrs={'type':'number'}))
    email = forms.EmailField()
    address =forms.CharField(max_length=50, required=True)

    class Meta:
        model=User
        fields = ['first_name','last_name','mobile','email','address','username','password1','password2']

# AddressBook Add Form
class AddressBookForm(forms.ModelForm):
	class Meta:
		model=UserAddressBook
		fields=('address','mobile','status')

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Account
from .filters import AccountFilter
from django.forms import modelformset_factory

class AccountCreationForm(UserCreationForm):
    email = forms.EmailField(widget=forms.TextInput(attrs={'class':'form-control'}))
    password1 = forms.CharField(
        label = 'Password',
        widget =  forms.PasswordInput(attrs={'class':'form-control'})
        )
    password2 = forms.CharField(
        label = 'Confirm password',
        widget =  forms.PasswordInput(attrs={'class':'form-control'})
        )

    class Meta:
        model = Account
        fields = ['email']

class AccountAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email'}))
    password = forms.CharField(
        label = 'Password',
        widget =  forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Password'})
        )

    class Meta:
        model: Account

class AccountAssignmentForm(forms.ModelForm):

    class Meta:
        model = Account
        fields = ['id','email', 'role']

    def __init__(self, *args, **kwargs):
        super(AccountAssignmentForm, self).__init__(*args, **kwargs)
        if self.instance.id:
            self.fields['email'].widget.attrs['hidden'] = True
            self.fields['email'].widget.attrs['readonly'] = True
            self.fields['role'].widget.attrs['class'] = 'form-control'

AccountAssignmentFormSet = modelformset_factory(Account, form=AccountAssignmentForm, extra=0)
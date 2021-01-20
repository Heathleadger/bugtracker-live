import django_filters
from .models import Account
from django import forms

class AccountFilter(django_filters.FilterSet):
    email = django_filters.CharFilter(field_name='email', lookup_expr='contains', widget= forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Search by account email'}))
    class Meta:
        model = Account
        fields = {
            # 'name' : ['contains'],
        }

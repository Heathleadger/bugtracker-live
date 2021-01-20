import django_filters
from .models import Account, Project, Ticket
from django import forms

class StakeholdersFilter(django_filters.FilterSet):
    email = django_filters.CharFilter(lookup_expr='contains')

    class Meta:
        model = Account
        fields = ['email']


class ProjectFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='name', lookup_expr='contains', widget= forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Search by project name', 'width':'100%'}))
    class Meta:
        model = Project
        fields = {
            # 'name' : ['contains'],
        }

class TicketFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(field_name='title', lookup_expr='contains', widget= forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Search by project title'}))
    class Meta:
        model = Ticket
        fields = {
            # 'name' : ['contains'],
        }

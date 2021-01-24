from django import template
from tracker.models import Account
from django.shortcuts import get_object_or_404

register = template.Library()

@register.filter(name='get_custom_status_display')
def get_custom_status_display(value):
    status = {
        None: '--/--',
        1: 'Sent',
        2: 'Assigned',
        3: 'In Progress',
        4: 'Done'
    }
    return status[value]



@register.filter(name='get_user_email')
def get_user_email(value):

    try:
        Account.objects.get(id=value)
        user = Account.objects.get(id=value)
        return user.email
    except Account.DoesNotExist:
        return 'None'


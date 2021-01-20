from django import forms
from .models import Project, TicketComment, Ticket, Account
from django.db.models import Q
# Customer Fields

class DateInput(forms.DateInput):
    input_type = 'datetime-local'

#Forms
class ProjectCreateForm(forms.ModelForm):

    class Meta:
        model = Project
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control','form':'filter_stakeholder','form':'create_project'}),
            'description': forms.Textarea(attrs={'class':'form-control'}),
            'manager': forms.SelectMultiple(attrs={'class':'form-control'}),
            'public': forms.CheckboxInput(attrs={'class':'form-check-input'}),
            'stakeholder': forms.CheckboxSelectMultiple(attrs={'class':'form-control'}),
        }

    def clean_stakeholder(self):
        stakeholders = self.cleaned_data.get('stakeholder')
        managers = self.cleaned_data.get('manager')
        stakeholders = stakeholders | managers
        return stakeholders


class TicketCommentForm(forms.ModelForm):
    
    class Meta:
        model = TicketComment
        fields = ['comment','file']
        widgets = {
            'comment':  forms.Textarea(attrs={'class': 'form-control'})
        }

class TicketCreateForm(forms.ModelForm):


    class Meta:
        model = Ticket
        fields = ['title', 'description','deadline','priority','tag','assigned']
        widgets = {
            'title':  forms.TextInput(attrs={'class': 'form-control'}),
            'description':  forms.Textarea(attrs={'class': 'form-control'}),
            'deadline':  DateInput(attrs={'class':'form-control'}),
            'priority':  forms.Select(attrs={'class': 'form-control'}),
            'tag':  forms.Select(attrs={'class': 'form-control'}),
            'assigned':  forms.Select(attrs={'class': 'form-control'}),

        }

    def __init__(self, *args, **kwargs):
        project_id = kwargs.pop('project_id', None)
        super(TicketCreateForm, self).__init__(*args, **kwargs)
        project = Project.objects.get(id=project_id)
        self.fields['assigned'].queryset = project.stakeholder.filter(Q(role = 2) | Q(role=1))



class TicketEditAssignedForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['assigned']
        widgets = {
            'assigned':  forms.Select(attrs={'class': 'form-control mr-1'}),
        }

class TicketEditStatusForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['status']
        widgets = {
            'status':  forms.Select(attrs={'class': 'form-control mr-1'}),
        }
                
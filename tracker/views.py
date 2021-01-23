from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Project, Ticket, Account 
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import ProjectCreateForm, TicketCommentForm, TicketCreateForm, TicketEditAssignedForm, TicketEditStatusForm
from django.urls import reverse_lazy, reverse
from .filters import StakeholdersFilter, ProjectFilter, TicketFilter
from django.http import JsonResponse, HttpResponseRedirect
from django.forms.models import model_to_dict
from django.core import serializers
from django.db.models import Q
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.core.paginator import Paginator


# General


def homepage(request):
    return render(request, 'homepage.html')


def accounts_json(request):
    search = request.GET.get('search')
    result = Account.objects.filter(email__icontains = search).values('id','email','role')

    result = list(result)
    #acc = serializers.serialize('json',Account.objects.filter(email__icontains = search))

    return JsonResponse(result, safe=False)

def project_create_view(request):
    form = ProjectCreateForm()

    stake_filter = StakeholdersFilter(request.GET, queryset= Account.objects.all())
    stakeholders = stake_filter.qs
    print(stakeholders)

    if request.method == 'POST':
        
        print(request.POST)        
        print('oiee')
        # form.save(commit=false)
    else:
        print('else')

    context = {
        'form': form,
        'stakeholders': stakeholders,
        'stake_filter': stake_filter
    }
    return render(request, 'tracker/project_creating.html', context)


# Ticket Views


def ticket_detail_view(request, pk):
    ticket = Ticket.objects.get(id=pk)
    # Checks if user is PM in order not to update field accidentally
    if request.user.role == 1:
        ticket_assigned_form = TicketEditAssignedForm(request.POST or None, instance=ticket)
        ticket_status_form = TicketEditStatusForm(request.POST or None, instance=ticket)
        project = Project.objects.get(ticket=ticket)
        ticket_assigned_form.fields['assigned'].queryset = project.stakeholder.filter(Q(role = 2) | Q(role=1))
    else:
        ticket_assigned_form = TicketEditAssignedForm(instance=ticket)
        ticket_status_form = TicketEditStatusForm(instance=ticket)


    if request.method == 'POST':
        if 'start' in request.POST:
            ticket = Ticket.objects.get(id=pk)
            ticket.status = 3
            ticket.save()
            ticket_status_form = TicketEditStatusForm(instance=ticket)
            ticket_assigned_form = TicketEditAssignedForm(instance=ticket)

        if 'finish' in request.POST:
            ticket = Ticket.objects.get(id=pk)
            ticket.status = 4
            ticket.save()
            ticket_status_form = TicketEditStatusForm(instance=ticket)
            ticket_assigned_form = TicketEditAssignedForm(instance=ticket)

        comment_form = TicketCommentForm(request.POST, request.FILES)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.ticket = ticket
            new_comment.user = request.user
            new_comment.save()
            comment_form = TicketCommentForm()


        if 'assigned' in ticket_assigned_form.data:
            if ticket_assigned_form.is_valid() and request.user.role == 1 :
                ticket_assigned_form.save()
                ticket.status = 2
                ticket.save()
                ticket_status_form = TicketEditStatusForm(instance=ticket)
                ticket_assigned_form = TicketEditAssignedForm(instance=ticket)

        if 'status' in ticket_status_form.data:
            if ticket_status_form.is_valid() and request.user.role == 1 :
                print('status valid')
                ticket_status_form.save()
                ticket_status_form = TicketEditStatusForm(instance=ticket)
                ticket_assigned_form = TicketEditAssignedForm(instance=ticket)


    else:
        comment_form = TicketCommentForm()

    context = {
        'ticket': ticket,
        'form': comment_form,
        'ticket_assigned_form': ticket_assigned_form,
        'ticket_status_form': ticket_status_form 
    }
    return render(request,'tracker/ticket_detail.html', context)

class TicketCreateView(LoginRequiredMixin, CreateView):
    models = Ticket
    form_class = TicketCreateForm
    template_name = 'tracker/ticket_form.html'
    
 
    def form_valid(self, form, **kwargs):
        ticket = form.save(commit=False)
        project_id = self.kwargs['project_id']
        project = get_object_or_404(Project, id=project_id)
        ticket.project = project
        ticket.requester = self.request.user
        if self.request.user.role == 1 and ticket.assigned != None:
            ticket.status  = 2
        return super(TicketCreateView, self).form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(TicketCreateView, self).get_form_kwargs()
        kwargs['project_id'] = self.kwargs['project_id']
        return kwargs

    def get_success_url(self):
        return reverse('tracker:project-detail', kwargs={'pk': self.kwargs['project_id']})



# Project Views


class ProjectDetailView(LoginRequiredMixin, DetailView):
    login_url = '/accounts/template/registration/login/'
    model = Project

    def get_context_data(self,**kwargs):
        context = super(ProjectDetailView,self).get_context_data(**kwargs)
        tickets = Ticket.objects.filter(project= self.get_object())

        if self.request.GET.get('search'):
            search_field = self.request.GET.get('search')
            tickets = tickets.filter(title__icontains = search_field)

        context['tickets'] = tickets
        return context
    
    



class ProjectListView(LoginRequiredMixin, ListView):
    model = Project
    paginate_by = 5


    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.GET.get('search'):
            search_field = self.request.GET.get('search')
            queryset = Project.objects.filter(name__icontains = search_field)
        
        return queryset
    
    
class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    form_class = ProjectCreateForm

    def get_context_data(self, **kwargs):
        context = super(ProjectCreateView, self).get_context_data(**kwargs)
        stakeholders = StakeholdersFilter(self.request.GET, queryset= Account.objects.all())
        context["filter"] = stakeholders
        return context
    
    def get_form(self, *args, **kwargs):
        form = super(ProjectCreateView, self).get_form(*args, **kwargs)
        form.fields['manager'].queryset = Account.objects.filter(role=1)
        return form


class ProjectUpdateView(LoginRequiredMixin, UpdateView):
    model = Project
    form_class = ProjectCreateForm

    def get_form(self, *args, **kwargs):
        form = super(ProjectUpdateView, self).get_form(*args, **kwargs)
        form.fields['manager'].queryset = Account.objects.filter(role=1)
        return form

class ProjectDeleteView(LoginRequiredMixin, DeleteView):
    model = Project
    success_url = reverse_lazy('tracker:project-list')
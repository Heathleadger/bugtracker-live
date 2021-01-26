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
from rest_framework.views import APIView
from rest_framework.response import Response 
from rest_framework import authentication, permissions
from rest_framework.permissions import IsAuthenticated
# General

def index(request):
    return render(request,'index.html')
def homepage(request):

    if request.user.is_authenticated:


        #Tickets sent
        tickets_sent = Ticket.objects.filter(requester=request.user).order_by('status')
        sent_paginator = Paginator(tickets_sent,5)
        sent_page_number = request.GET.get('sent_page')
        sent_page_obj = sent_paginator.get_page(sent_page_number)

        #Tickets assigned
        tickets_assigned = Ticket.objects.filter(assigned=request.user).order_by('status')
        assigned_paginator = Paginator(tickets_assigned,5)
        assigned_page_number = request.GET.get('assigned_page')
        assigned_page_obj = assigned_paginator.get_page(assigned_page_number)
        




        context = {
            'sent_page_obj': sent_page_obj,
            'assigned_page_obj': assigned_page_obj
        }


        return render(request, 'homepage.html', context)
    else:
        return render(request, 'homepage.html')


class AccountsAPI(APIView):
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = (IsAuthenticated,)
    def get(self, request, format=None):

        search = request.GET.get('search')
        data = Account.objects.filter(email__icontains = search).values('id','email','role')
        data = list(data)
        return Response(data)

#Graphs data


class ProjectManagerTicketsOverview(APIView):
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        projects = Project.objects.filter(manager=request.user)

        labels = []
        sent = {'label':'Sent', 'data':[]}
        assigned = {'label':'Assigned', 'data':[]}
        in_progress = {'label':'In Progress', 'data':[]}
        done = {'label':'Done', 'data':[]}

        for project in projects:
            tickets = Ticket.objects.filter(project=project)

            labels.append(project.name)
            
            sent['data'].append(tickets.filter(status=1).count())
            assigned['data'].append(tickets.filter(status=2).count())
            in_progress['data'].append(tickets.filter(status=3).count())
            done['data'].append(tickets.filter(status=4).count())

        dataset = [sent, assigned, in_progress, done]

        data ={
            'labels': labels,
            'dataset': dataset
        }

        return Response(data)


class UserTickets(APIView):
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = (IsAuthenticated,)
    def get(self, request, format=None):
        user = request.user

        print(user)
        user_tickets = Ticket.objects.filter(requester=user)
        
        sent = user_tickets.filter(status=1).count()
        assgined = user_tickets.filter(status=2).count()
        in_progress = user_tickets.filter(status=3).count()
        done = user_tickets.filter(status=4).count()



        status_label = ['Received','Assigned','In Progress','Done']
        status_data = [sent, assgined, in_progress, done]

        data ={
            'label': status_label,
            'value' : status_data,
        }

        return Response(data)



# Ticket Views


def ticket_detail_view(request, pk):
    #Instance of ticket
    ticket = Ticket.objects.get(id=pk)

    # Get whistory of changes
    history = ticket.history.all()
    total_records = []
    #Loop through each line and check field, olg and new values
    for line in history:
        #Ignore the last line as it does not have a .prev_record
        if line == history.reverse()[0]:
            break
        user = Account.objects.get(id=line.requester_id)
        new_record = line
        old_record = line.prev_record
        delta = new_record.diff_against(old_record)
        # Loop through changes and append to record + append user (requester)
        for change in delta.changes:
            total_records.append({'instance':change, 'user':user})

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
        # Trigger star ticket for developers
        if 'start' in request.POST:
            ticket = Ticket.objects.get(id=pk)
            ticket.status = 3
            ticket.save()
            ticket_status_form = TicketEditStatusForm(instance=ticket)
            ticket_assigned_form = TicketEditAssignedForm(instance=ticket)
        #Trigger finish ticket for developers
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

        # Assign new dev to ticket - autoupdate the status
        if 'assigned' in ticket_assigned_form.data:
            if ticket_assigned_form.is_valid() and request.user.role == 1 :
                ticket_assigned_form.save()
                ticket.status = 2
                ticket.save()
                ticket_status_form = TicketEditStatusForm(instance=ticket)
                ticket_assigned_form = TicketEditAssignedForm(instance=ticket)

        # Update status
        if 'status' in ticket_status_form.data:
            if ticket_status_form.is_valid() and request.user.role == 1 :
                ticket_status_form.save()
                ticket_status_form = TicketEditStatusForm(instance=ticket)
                ticket_assigned_form = TicketEditAssignedForm(instance=ticket)


    else:
        comment_form = TicketCommentForm()

    context = {
        'ticket': ticket,
        'form': comment_form,
        'ticket_assigned_form': ticket_assigned_form,
        'ticket_status_form': ticket_status_form,
        'history': total_records
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
        #Assign project to ticket
        ticket.project = project
        #Assign user to ticket
        ticket.requester = self.request.user
        #Auto update status in case PM has set a dev for a ticket
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
        user = self.request.user
        if self.request.GET.get('search'):
            search_field = self.request.GET.get('search')
            queryset = Project.objects.filter(Q(name__icontains = search_field) & (Q(manager=user)| Q(stakeholder=user))).distinct()
        else:
            queryset = Project.objects.filter(Q(manager=user)| Q(stakeholder=user)).distinct()
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
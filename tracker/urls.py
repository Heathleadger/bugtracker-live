from django.urls import path
from tracker.views import (
    homepage, 
    ProjectDetailView, 
    ProjectListView, 
    ProjectCreateView, 
    ProjectUpdateView, 
    ProjectDeleteView,
    ticket_detail_view,
    TicketCreateView,
    AccountsAPI,
    UserTickets,
    ProjectManagerTicketsOverview,
    index
    )

app_name = 'tracker'
urlpatterns = [

    path('', index, name="index"),
    path('home', homepage, name="homepage"),

    # Ticket Urls

    path('ticket/<int:pk>', ticket_detail_view, name="ticket-detail" ),
    path('ticket/create/<int:project_id>', TicketCreateView.as_view(), name="ticket-create" ),


    # Project URLS
    path('projects/', ProjectListView.as_view(), name='project-list'),   
    path('projects/<int:pk>', ProjectDetailView.as_view(), name='project-detail'),
    path('projects/create/', ProjectCreateView.as_view(), name= 'project-create' ),
    path('projects/<int:pk>/update/', ProjectUpdateView.as_view(), name= 'project-edit' ),
    path('projects/<int:pk>/delete/', ProjectDeleteView.as_view(), name= 'project-delete' ),


    #Json response
    path('api/accounts/', AccountsAPI.as_view(), name="accounts-api"),
    path('api/user_ticket_status', UserTickets.as_view(),name="user-ticket-status"),
    path('api/pm_tickets_overview', ProjectManagerTicketsOverview.as_view(),name="pm-tickets-overview"),


]

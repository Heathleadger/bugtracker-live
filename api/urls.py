from django.urls import path
from rest_framework.authtoken import views
from .views import ProjectGeneralView, ProjectViewSet, TicketViewSet, TicketCommentsViewSet, CustomAuthToken, AccountViewSet, ProjectManagerOverviewChart, TicketsSentChart

app_name = 'api'

urlpatterns = [
    # Tickets
    path('tickets/', TicketViewSet.as_view({'get':'list','post':'create'}), name="ticket-list" ),
    path('ticket-detail/<int:pk>', TicketViewSet.as_view({'get':'retrieve'}), name="ticket-detail" ),


    path('ticket-comments-viewset/', TicketCommentsViewSet.as_view({'post': 'create'}), name="ticket-comments-view-set" ),
    

    # Projects
    
    path('projects/', ProjectGeneralView.as_view(), name="project-list-api" ),

    path('project-viewset/', ProjectViewSet.as_view({'get': 'list', 'post': 'create'}), name="project-view-set" ),
    path('project-viewset/<int:pk>', ProjectViewSet.as_view({'get': 'retrieve', 'post': 'update', 'delete':'destroy'}), name="project-view-set" ),

    #Charts
    path('project-manager-chart/', ProjectManagerOverviewChart.as_view(), name="project-manager-chart" ),
    path('tickets-sent-chart/', TicketsSentChart.as_view(), name="tickets-sent-chart" ),

    #Accounts

    path('accounts/<int:pk>', AccountViewSet.as_view({'put':'update'}), name="accounts-viewset" ),
    path('accounts/', AccountViewSet.as_view({'get':'list'}), name="accounts-viewset" ),
    path('register/', AccountViewSet.as_view({'post': 'create'}), name="register"),

    #Auth

    path('auth/', CustomAuthToken.as_view(), name="token-auth")
]

from django.shortcuts import render
from django.forms.models import model_to_dict
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework import generics, viewsets, mixins, status
from .serializers import ProjectSerializer, AccountsSerializer, TicketsSerializer, TicketCommentsSerializer
from tracker.models import Project, Ticket, TicketComment
from accounts.models import Account
from django.db.models import Q

# Create your views here.

class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email,
            'role': user.role
        })

    def get(self, request, *args, **kwargs):
        token = Token.objects.get(user=request.user)
        return Response({'id': request.user.id,'email':request.user.email,'role': request.user.role, 'token': token.key})


class ProjectGeneralView(generics.ListAPIView):
    lookup_field = 'pk'
    serializer_class = ProjectSerializer
    
    def get_queryset(self):
        return Project.objects.filter(Q(manager = self.request.user) | Q(stakeholder= self.request.user)).distinct()
    


class AccountViewSet(viewsets.ModelViewSet):
    lookup_field = 'pk'
    queryset = Account.objects.all()
    serializer_class = AccountsSerializer

    def update(self, request, *args, **kwargs):
        instance = Account.objects.get(id = request.data.get('id'))
        serializer = self.serializer_class(instance ,data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes = (AllowAny,)

        return super(AccountViewSet, self).get_permissions()

class ProjectViewSet(viewsets.ModelViewSet):
    lookup_field = "pk"
    serializer_class = ProjectSerializer

    def get_queryset(self):
        return Project.objects.filter(manager = self.request.user)


class TicketViewSet(viewsets.ModelViewSet):
    lookup_field = "pk"
    serializer_class = TicketsSerializer

    def get_queryset(self):
        return Ticket.objects.all()

    # def create (self, request, *args, **kwargs):
    #     # print(self.request.user)
    #     # request.data['requester'] = self.request.user
    #     request.data['assigned'] = model_to_dict(Account.objects.get(id = request.data['assigned']))
    #     serializer = TicketsSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     else:
    #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        return serializer.save(requester= self.request.user)  


class TicketCommentsViewSet(viewsets.ModelViewSet):
    serializer_class = TicketCommentsSerializer
    queryset = TicketComment.objects.all()

    def perform_create(self, serializer):
        return serializer.save(user= self.request.user)



class ProjectManagerOverviewChart(APIView):

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


class TicketsSentChart(APIView):
    def get(self, request, format=None):
        user = request.user

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
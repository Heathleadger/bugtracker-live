from django.db import models
from django.contrib.auth.models import User
from accounts.models import Account
from django.urls import reverse
from simple_history.models import HistoricalRecords

# Create your models here.        

class Project(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=500)
    manager = models.ManyToManyField(Account,related_name='projectmanager')
    public = models.BooleanField(default=True)
    stakeholder = models.ManyToManyField(Account, related_name='projectstakeholder', blank=True)
    history = HistoricalRecords()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('tracker:project-list')
    

class Ticket(models.Model):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    PRIORITIES_CHOICES = [
        (LOW, 'Low'),
        (MEDIUM, 'Medium'),
        (HIGH, 'High'),
    ]

    SENT = 1
    ASSIGNED = 2
    IN_PROGRESS = 3
    DONE = 4
    STATUS_CHOICES = [
        (SENT, 'Sent'),
        (ASSIGNED, 'Assigned'),
        (IN_PROGRESS, 'In Progress'),
        (DONE, 'Done'),
    ]

    project = models.ForeignKey(Project, related_name='ticket', on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    requester = models.ForeignKey(Account, related_name='userticket', on_delete=models.CASCADE)
    assigned = models.ForeignKey(Account, related_name='userassigned', on_delete=models.CASCADE, blank=True, null=True)
    description =  models.TextField()
    deadline = models.DateTimeField()
    priority = models.PositiveSmallIntegerField(choices=PRIORITIES_CHOICES, default=1)
    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES, default=1)
    tag = models.ForeignKey("TicketTag", related_name="tickettag", on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

"""     def get_absolute_url(self):
        return reverse('tracker:project-list') """

class TicketTag(models.Model):
    label = models.CharField(max_length=50)

    def __str__(self):
        return self.label

class TicketComment(models.Model):
    ticket = models.ForeignKey(Ticket, related_name="ticketcoment", on_delete=models.CASCADE)
    user = models.ForeignKey(Account, related_name='usercomment', on_delete=models.CASCADE)
    comment = models.TextField()
    file = models.FileField(blank=True, null=True)

    def __str__(self):
        return self.comment

class TicketHistory(models.Model):
    ticket = models.ForeignKey(Ticket, related_name='historyticket', on_delete=models.CASCADE)
    user = models.ForeignKey(Account, related_name='historyuser', on_delete=models.CASCADE)
    camp = models.CharField(max_length=255)
    old_value = models.CharField(max_length=255)
    new_value = models.CharField(max_length=255)
    data_created = models.DateTimeField(auto_now_add=True)

class TicketFiles(models.Model):
    ticket = models.ForeignKey(Ticket, related_name="ticketfiles", on_delete=models.CASCADE)
    file = models.FileField(upload_to=None, max_length=100)

class TicketFilesComment(models.Model):
    ticketfile = models.ForeignKey(TicketFiles, related_name="ticketfilecoment", on_delete=models.CASCADE)
    comment = models.TextField()

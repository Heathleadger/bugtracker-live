from django.contrib import admin
from .models import (
    Project, 
    Ticket, 
    TicketHistory, 
    TicketFiles, 
    TicketComment, 
    TicketFilesComment,
    TicketTag
    )
# Register your models here.

admin.site.register(Project)
admin.site.register(Ticket)
admin.site.register(TicketHistory)
admin.site.register(TicketFiles)
admin.site.register(TicketFilesComment)
admin.site.register(TicketComment)
admin.site.register(TicketTag)

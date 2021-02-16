from rest_framework import serializers
from tracker.models import Project, Ticket, TicketComment
from accounts.models import Account
from tracker.models import TicketTag
from rest_framework.response import Response
from django.core.serializers import serialize


class AccountsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = super().create(validated_data)
        user.set_password(password)
        user.save()
        return user


class TicketCommentsSerializer(serializers.ModelSerializer):
    user = AccountsSerializer(required=False)
    class Meta:
        model = TicketComment
        fields = '__all__'


class ProjectSerializer(serializers.ModelSerializer):
    # manager = AccountsSerializer(many=True, read_only=True)
    # stakeholder = AccountsSerializer(many=True, read_only=True)
    # ticket =  TicketsSerializer(many=True, read_only=True)
    class Meta:
        model = Project
        fields = '__all__'


class TicketsSerializer(serializers.ModelSerializer):
    history = serializers.SerializerMethodField()
    requester = AccountsSerializer(required=False)
    ticketcomment = TicketCommentsSerializer(read_only=True, many=True)
    project = serializers.PrimaryKeyRelatedField(
    many = False,
    queryset = Project.objects.all()
    )
    tag = serializers.PrimaryKeyRelatedField(
    many = False,
    queryset = TicketTag.objects.all()
    )

    # project = ProjectSerializer(read_only=True)
    # ticket_comments = serializers.SerializerMethodField('_get_comments')

    class Meta:
        model = Ticket
        fields = '__all__'
        depth = 1

    def get_history(self, obj):
        history = obj.history.all()
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
                qs = change.__dict__
                qs['user'] = user.email
                total_records.append(qs)
        return total_records


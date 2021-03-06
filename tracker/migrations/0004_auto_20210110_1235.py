# Generated by Django 3.1.5 on 2021-01-10 11:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tracker', '0003_auto_20210110_1225'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='project',
            name='stakeholder',
            field=models.ManyToManyField(blank=True, related_name='projectstakeholder', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='TickerHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('camp', models.CharField(max_length=255)),
                ('data_created', models.DateTimeField(auto_now_add=True)),
                ('ticket', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='historyticket', to='tracker.ticket')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='historyuser', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

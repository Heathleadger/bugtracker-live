# Generated by Django 3.1.5 on 2021-02-03 10:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0016_historicalticket'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticketcomment',
            name='ticket',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ticketcomment', to='tracker.ticket'),
        ),
    ]

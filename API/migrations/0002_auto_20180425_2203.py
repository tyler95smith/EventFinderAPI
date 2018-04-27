# Generated by Django 2.0.2 on 2018-04-25 22:03

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('API', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rsvp',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('status', models.IntegerField(default=0)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='API.Event')),
                ('requester', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='notification',
            name='event',
        ),
        migrations.RemoveField(
            model_name='notification',
            name='time_to_send',
        ),
        migrations.AddField(
            model_name='notification',
            name='date_created',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now),
        ),
        migrations.AddField(
            model_name='notification',
            name='date_sent',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='notification',
            name='reciver',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='reciver', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='notification',
            name='sender',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='sender', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='report',
            name='rep_account',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reported_account', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='report',
            name='rep_event',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='API.Event'),
        ),
    ]
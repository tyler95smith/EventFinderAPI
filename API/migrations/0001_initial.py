# Generated by Django 2.0.2 on 2018-03-01 20:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('eventname', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Conversation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('event_name', models.CharField(max_length=100)),
                ('location', models.CharField(max_length=200)),
                ('event_date', models.DateTimeField()),
                ('description', models.CharField(max_length=512)),
                ('age_min', models.IntegerField(default=0)),
                ('age_max', models.IntegerField(default=0)),
                ('is_hidden', models.BooleanField(default=False)),
                ('attendees', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='atendee_accounts', to='API.Account')),
                ('host', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='event_host_account', to='API.Account')),
            ],
        ),
        migrations.CreateModel(
            name='Interests',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('message', models.CharField(max_length=512)),
                ('conversation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='API.Conversation')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='API.Account')),
            ],
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_to_send', models.DateTimeField()),
                ('message', models.CharField(max_length=512)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='API.Event')),
            ],
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('rep_message', models.CharField(max_length=512)),
                ('rep_account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reported_account', to='API.Account')),
                ('rep_event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='API.Event')),
                ('snitch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reportee_account', to='API.Account')),
            ],
        ),
        migrations.AddField(
            model_name='event',
            name='interests',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='API.Interests'),
        ),
        migrations.AddField(
            model_name='conversation',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='API.Event'),
        ),
        migrations.AddField(
            model_name='conversation',
            name='guest',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='guest_account', to='API.Account'),
        ),
        migrations.AddField(
            model_name='conversation',
            name='host',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='host_account', to='API.Account'),
        ),
    ]

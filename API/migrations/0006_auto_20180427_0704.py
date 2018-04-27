# Generated by Django 2.0.2 on 2018-04-27 07:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('API', '0005_auto_20180426_2315'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventPicture',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.FileField(blank=True, null=True, upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='Interest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=512)),
            ],
        ),
        migrations.CreateModel(
            name='ProfilePicture',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.FileField(blank=True, null=True, upload_to='')),
                ('description', models.CharField(blank=True, max_length=100, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterField(
            model_name='event',
            name='interests',
            field=models.ManyToManyField(to='API.Interest'),
        ),
        migrations.AddField(
            model_name='eventpicture',
            name='event',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='API.Event'),
        ),
        migrations.AddField(
            model_name='person',
            name='interests',
            field=models.ManyToManyField(to='API.Interest'),
        ),
    ]
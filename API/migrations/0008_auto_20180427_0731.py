# Generated by Django 2.0.2 on 2018-04-27 07:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0007_auto_20180427_0730'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='interests',
            field=models.ManyToManyField(blank=True, to='API.Interest'),
        ),
        migrations.AlterField(
            model_name='person',
            name='interests',
            field=models.ManyToManyField(blank=True, to='API.Interest'),
        ),
    ]

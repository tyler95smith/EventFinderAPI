# Generated by Django 2.0.2 on 2018-04-26 21:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0003_auto_20180425_2312'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='isFemale',
            field=models.BooleanField(default=True),
        ),
    ]
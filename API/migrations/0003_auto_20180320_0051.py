# Generated by Django 2.0.2 on 2018-03-20 00:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0002_auto_20180302_0148'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='isBanned',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='person',
            name='date_of_birth',
            field=models.DateField(null=True),
        ),
    ]
# Generated by Django 4.0 on 2022-05-24 12:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client_management', '0002_token'),
    ]

    operations = [
        migrations.AddField(
            model_name='consumer',
            name='avatar',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='producer',
            name='avatar',
            field=models.CharField(max_length=50, null=True),
        ),
    ]

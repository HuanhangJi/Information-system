# Generated by Django 2.1.15 on 2022-05-30 10:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task_management', '0002_project_project_pic'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='item_per_task',
            field=models.IntegerField(null=True),
        ),
    ]

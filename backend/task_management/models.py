from django.db import models
# Create your models here.


class Task(models.Model):
    task_id = models.CharField(max_length=25,primary_key=True)
    project_id = models.CharField(max_length=25)
    PAF_id = models.CharField(max_length=25)
    task_status = models.CharField(max_length=20)
    score = models.IntegerField()


class Project(models.Model):
    project_id = models.CharField(max_length=25,primary_key=True,auto_created=True)
    prepay_id = models.CharField(max_length=25)
    account_id = models.CharField(max_length=25)
    publisher_id = models.CharField(max_length=25)
    project_name = models.CharField(max_length=64)
    project_type = models.CharField(max_length=20)
    description = models.CharField(max_length=1024)
    sample_document = models.FileField(upload_to='sample_document')
    due_time = models.DateTimeField()
    payment_per_task = models.FloatField()
    project_status = models.IntegerField()
    task_num = models.IntegerField()
    completed_task_num = models.IntegerField()


class Prepay(models.Model):
    prepay_id = models.CharField(max_length=25, primary_key=True, auto_created=True)
    project_id = models.CharField(max_length=25)
    prepay_amount = models.FloatField()
    prepay_balance = models.FloatField()


class Task_record(models.Model):
    account_id = models.CharField(max_length=25)
    worker_id = models.CharField(max_length=25)
    task_id = models.CharField(max_length=25)
    reward_id = models.CharField(max_length=25)

    class Meta:
        unique_together = ("account_id", "worker_id", "task_id")


class Reward_record(models.Model):
    reward_id = models.CharField(max_length=25,primary_key=True, auto_created=True)
    reward_amount = models.FloatField()
    reward_time = models.DateTimeField()


class Total_account(models.Model):
    PAF_id = models.CharField(max_length=25,primary_key=True, auto_created=True)
    task_id = models.CharField(max_length=25)
    PAF_type = models.CharField(max_length=4)
    PAF_amount = models.FloatField()
    PAF_balance = models.FloatField()
    PAF_time = models.DateTimeField()
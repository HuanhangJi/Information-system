from django.db import models

# Create your models here.

class Task(models.Model):
    task_id = models.CharField(max_length=25,primary_key=True)
    project_id = models.CharField(max_length=25)
    task_status = models.CharField(max_length=20)
    # original_data = models.FileField(upload_to='data')
    # processed_data = models.FileField(upload_to='data')
    score = models.IntegerField()
    due_time = models.DateTimeField()

    def to_dict(self):
        data = {'project_id':self.project_id,
                'task_id':self.task_id,
                'score':self.score,
                'due_time': self.due_time
                }
        return data


class Project(models.Model):
    project_id = models.CharField(max_length=25,primary_key=True)
    prepay_id = models.CharField(max_length=25)
    account_id = models.CharField(max_length=25)
    project_name = models.CharField(max_length=64)
    project_type = models.CharField(max_length=20)
    description = models.CharField(max_length=1024)
    # sample_document = models.FileField(upload_to='sample_document')
    due_time = models.DateTimeField()
    payment_per_task = models.FloatField()
    project_status = models.IntegerField()
    task_num = models.IntegerField()
    completed_task_num = models.IntegerField()
    project_star = models.IntegerField()



    def to_dict(self):
        data = {'project_id':self.project_id,
                'description':self.description,
                'project_name':self.project_name,
                'project_type':self.project_type,
                'due_time':self.due_time,
                'payment_per_task':self.payment_per_task,
                'task_num':self.task_num,
                # 'sample_document':self.sample_document
                }
        return data


class Prepay(models.Model):#数据库修改
    prepay_id = models.CharField(max_length=25, primary_key=True, auto_created=True)
    project_id = models.CharField(max_length=25)
    prepay_amount = models.FloatField()
    prepay_balance = models.FloatField()
    account_id = models.CharField(max_length=25)



class Reward_record(models.Model):#数据库修改
    ta_id = models.CharField(max_length=25)
    reward_id = models.CharField(max_length=25,primary_key=True, auto_created=True)
    reward_amount = models.FloatField()
    reward_time = models.DateTimeField()


class Web_account(models.Model):
    PAF_id = models.CharField(max_length=25,primary_key=True, auto_created=True)
    task_id = models.CharField(max_length=25)
    PAF_type = models.CharField(max_length=4)
    PAF_amount = models.FloatField()
    PAF_balance = models.FloatField()
    PAF_time = models.DateTimeField()


class Task_association(models.Model):#数据库修改
    account_id = models.CharField(max_length=25)
    task_id = models.CharField(max_length=25)
    project_id = models.CharField(max_length=25)
    ta_id = models.CharField(max_length=25,primary_key=True,auto_created=True)



# 项目id库
class project_id_pool(models.Model):
    project_id = models.CharField(max_length=20,primary_key=True)
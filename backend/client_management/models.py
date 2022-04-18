from django.db import models
# Create your models here.


#用户基类
class UserInfo(models.Model):
    account_id = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    account_type = models.IntegerField()
    tel = models.CharField(max_length=20)
    name = models.CharField(max_length=20)
    avatar = models.ImageField(upload_to='avatar/%Y/%m/%d', default='')#头像
    gender = models.CharField(max_length=2)
    ID_num = models.CharField(max_length=25)#身份证号
    nickname = models.CharField(max_length=20)
    mail_add = models.CharField(max_length=20)

    class Meta:
        abstract = True


#完成者类
class Consumer(UserInfo):
    worker_id = models.CharField(max_length=20, auto_created=True)
    level = models.IntegerField()
    experience = models.IntegerField()

    class Meta:
        unique_together = ("account_id", "worker_id")

    def to_dict(self):
        pass


#发布者类
class Producer(UserInfo):
    publisher_id = models.CharField(max_length=20, auto_created=True)
    payment_password = models.CharField(max_length=6)

    class Meta:
        unique_together = ("account_id", "publisher_id")

    def to_dict(self):
        pass

#钱包类
class wallet(models.Model):
    AB_id = models.CharField(max_length=25, primary_key=True, auto_created=True)
    account_id = models.CharField(max_length=20)
    account_num = models.FloatField()

#银行卡类
class bank_card(models.Model):
    BC_id = models.CharField(max_length=25, primary_key=True, auto_created=True)
    account_id = models.CharField(max_length=20)
    card_num = models.CharField(max_length=20)

#充值体现记录类
class record(models.Model):
    cw_id = models.CharField(max_length=25, primary_key=True, auto_created=True)
    AB_id = models.ForeignKey(wallet, on_delete=models.CASCADE)
    cw_type = models.CharField(max_length=4)
    cw_amount = models.FloatField()
    pay_time = models.DateTimeField()
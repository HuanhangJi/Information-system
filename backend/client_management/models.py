from django.db import models
# Create your models here.


#用户基类
class UserInfo(models.Model):
    account_id = models.CharField(max_length=20,primary_key=True)
    password = models.CharField(max_length=50)
    account_type = models.IntegerField()
    tel = models.CharField(max_length=20)
    name = models.CharField(max_length=20)
    avatar = models.CharField(max_length=50,null=True)
    gender = models.CharField(max_length=2)
    ID_num = models.CharField(max_length=25)#身份证号
    nickname = models.CharField(max_length=20)
    mail_add = models.CharField(max_length=20)
    status = models.IntegerField()

    class Meta:
        abstract = True


#标注者类
class Consumer(UserInfo):
    level = models.IntegerField()
    experience = models.IntegerField()

    def to_dict(self):
        data = {'account_id' : self.account_id,
                'tel':self.tel,
                'nickname':self.nickname,
                'level':self.level,
                # 'avatar':self.avatar,
                'experience':self.experience,
                'avatar' : self.avatar
                }
        return data


#发布者类
class Producer(UserInfo):

    def to_dict(self):
        data = {'account_id' : self.account_id,
                'tel':self.tel,
                'nickname':self.nickname,
                'avatar':self.avatar,
                }
        return data


#钱包类
class Wallet(models.Model):#数据库修改
    # AB_id = models.CharField(max_length=25, primary_key=True, auto_created=True)
    account_id = models.CharField(max_length=20)
    account_num = models.FloatField()
    payment_password = models.CharField(max_length=50)



#银行卡类
class Bank_card(models.Model):
    # BC_id = models.CharField(max_length=25, primary_key=True, auto_created=True)
    account_id = models.CharField(max_length=20)
    card_num = models.CharField(max_length=20)


#充值体现记录类
class Wallet_record(models.Model):
    # cw_id = models.CharField(max_length=25, primary_key=True, auto_created=True)
    AB_id = models.CharField(max_length=25)
    cw_type = models.CharField(max_length=20)
    cw_amount = models.FloatField()
    pay_time = models.DateTimeField()


#用户id库
class User_id_pool(models.Model):
    account_id = models.CharField(max_length=20,primary_key=True)

class Token(models.Model):
    account_id = models.CharField(max_length=50)
import datetime
import math
from django.http import *
from .models import *
import os
import sys
import random
from PIL import Image, ImageDraw
sys.path.append(os.path.abspath('..'))
os.chdir(os.path.abspath(os.getcwd()))
from client_management.models import *
from django.db.models import Q
import shutil
import json
import time
import zipfile
task_num = 0
flag = 0

## request初始化 FINISH
def get_res(request):
    data = request.body.decode('utf-8')
    res = json.loads(data)
    print(res)
    return res['info']


## TODO 补充ID池
def full_project_id(request):
    for ids in range(10000000,10005000):
        id = project_id_pool()
        id.project_id = ids
        id.save()
    return HttpResponse('成功添加')


## TODO 判断分数
def judge_score(star):
    stars = int(star)
    if stars == 1:
        score = 100
    elif stars == 2:
        score = 300
    elif stars == 3:
        score = 500
    elif stars == 4:
        score = 1000
    else:
        score = 2000
    return score

def judge_level(scores):
    if scores <= 1000:
        return 1
    elif scores <=3000:
        return 2
    elif scores <= 10000:
        return 3
    elif scores <= 20000:
        return 4
    else:
        return 5


## TODO 增加任务函数
def project_add(request):
    # try:
        res = get_res(request)
        publisher_id = res['publisher_id']
        project_name = res['project_name']
        project_type = res['project_type']
        global flag
        if project_type == 'image_block':
            flag = 0
            project_type = '图片识别标注'
        elif project_type == 'text_type':
            flag = 1
            project_type = '文本类型标注'
        else:
            flag = 2
            project_type = '图片类型标注'
        description = res['description']
        due_time = res['due_time']
        start_time = res['start_time']
        pay_per_task = res['pay_per_task']
        global task_num
        task_num = res['task_num']
        project_star = res['project_star']
        project_target = res['project_target']
        text_tags = res['text_tags']
        p = Project()
        id = project_id_pool.objects.first()
        project_id = id.project_id
        p.project_id = project_id
        id.delete()
        dic = prepay(request,project_id)
        if dic['code'] == 200:
            if os.path.exists(f'./static/sample_document/{project_id}'):
                shutil.rmtree(f'./static/sample_document/{project_id}')
            os.mkdir(f'./static/sample_document/{project_id}')
            if flag != 0:
                with open(f'./static/sample_document/{project_id}/text_tags_{project_id}.txt','w',encoding='utf-8') as fp:
                    n = len(text_tags)
                    for i in range(n):
                        if text_tags[i] == '，':
                            text_tags=replace_char(text_tags,",",i)
                        if text_tags[i] == '；':
                            text_tags=replace_char(text_tags,";",i)
                    fp.write(text_tags)
            p.account_id = publisher_id
            p.project_type = project_type
            p.task_num = task_num
            p.project_status = 0
            p.payment_per_task = pay_per_task
            t = time.localtime(due_time/1000)
            due_time = time.strftime("%Y-%m-%d %H:%M:%S",t)
            p.due_time = str(due_time)
            t = time.localtime(start_time/1000)
            start_time = time.strftime("%Y-%m-%d %H:%M:%S",t)
            p.start_time = str(start_time)
            p.completed_task_num = 0
            p.description = description
            p.project_name = project_name
            p.project_star = project_star
            p.project_target = project_target
            # p.sample_document = sample_document
            p.save()
            for i in range(1,task_num+1):
                t = Task()
                t.project_id = project_id
                t.task_id = project_id+'_'+str(i)
                t.score = judge_score(project_star)
                # t.original_data = sample_document
                t.due_time = due_time
                t.task_status = 0
                t.save()
            data = {'code':200,'msg':'添加任务成功','project_id':project_id}
        else:
            data = {'code':404,'msg':'预付款余额不足'}
        # except BaseException:
        #     data = {'code':404,'msg':'添加任务失败'}
        return JsonResponse(data)

def replace_char(old_string, char, index):
    '''
    字符串按索引位置替换字符
    '''
    old_string = str(old_string)
    # 新的字符串 = 老字符串[:要替换的索引位置] + 替换成的目标字符 + 老字符串[要替换的索引位置+1:]
    new_string = old_string[:index] + char + old_string[index+1:]
    return new_string



## TODO 删除任务函数
def project_delete(request):
    # try:
        res = get_res(request)
        project_id = res['project_id']
        if Project.objects.filter(project_id=project_id).exist():
            Project.objects.get(project_id=project_id).delete()
            Task.objects.filter(project_id=project_id).delete()
            data = {'code':200,'msg':'删除成功'}
        else:
            data = {'code':402,'msg':'不存在删除对象'}
    # except BaseException:
    #     data = {'code':404,'msg':'删除失败'}
        return JsonResponse(data)


## TODO 编辑任务函数
def project_edit(request):
    # try:
        res = get_res(request)
        project_id = res['project_id']
        project_name = res['project_name']
        description = res['description']
        due_time = res['due_time']
        # pay_per_task = request.GET['pay_per_task']
        if Project.objects.filter(project_id=project_id).exist():
            p = Project.objects.get(project_id=project_id)
            p.project_name = project_name
            p.description = description
            p.due_time = due_time
            # p.payment_per_task = pay_per_task
            p.save()
            data = {'code': 200, 'msg': '修改成功'}
        else:
            data = {'code':404,'msg':'未找到该任务'}
    # except BaseException:
    #     data = {'code':404,'msg':'修改失败'}
        return JsonResponse(data)


## TODO 查询任务函数
def project_query(request):
    # try:
        res = get_res(request)
        keyword = res['keyword']
        t = Project.objects.get(project_id=keyword)
        info = t.to_dict()
        data = {'code': 200, 'msg': '查询成功', 'task_info':info}
    # except BaseException:
    #     data = {'code': 404, 'msg': '查询失败','task_info':''}
        return JsonResponse(data)


# def write_data(request, project_id):
#     project_id = project_id
#     sample_document = request.FILES['file']
#     destination = f'./static/sample_document/{project_id}/{sample_document.name}'
#     if os.path.exists(destination):
#         os.remove(destination)
#     z = zipfile.ZipFile(destination,'w',zipfile.ZIP_DEFLATED)
#     z.close()
#     try:
#         with open(destination,'wb') as f:
#             for chunk in sample_document.chunks():
#                 f.write(chunk)
#         Z = zipfile.ZipFile(destination,'r',zipfile.ZIP_DEFLATED)
#         path = f'./static/sample_document/{project_id}'
#         num = 0
#         for i in Z.namelist():
#             num += 1
#             try:
#                 new_name = i.encode('cp437').decode('gbk')
#             except:
#                 new_name = i.encode('cp437').decode('utf-8')
#             Z.extract(i,path=path)
#             os.rename(path+f'/{i}',path+f'/{new_name}')
#         data = {'code': 200, 'msg': '写入成功'}
#     except Exception:
#         os.remove(destination)
#         data = {'code': 404, 'msg': '写入失败'}
#     return JsonResponse(data)


def write_data(request, project_id):
    global task_num
    global flag
    sample_document = request.FILES['file']
    destination = f'./static/sample_document/{project_id}/{sample_document.name}'
    if os.path.exists(destination):
        os.remove(destination)
    z = zipfile.ZipFile(destination,'w',zipfile.ZIP_DEFLATED)
    z.close()
    with open(destination,'wb') as f:
        for chunk in sample_document.chunks():
            f.write(chunk)
    Z = zipfile.ZipFile(destination,'r',zipfile.ZIP_DEFLATED)
    path = f'./static/sample_document/{project_id}'
    num = 0
    f = open(path+'/map.txt','w',encoding='utf-8')
    for i in Z.namelist():
        try:
            new_name = i.encode('cp437').decode('gbk')
        except:
            new_name = i.encode('cp437').decode('utf-8')
        type = new_name.split('.')[-1]
        if flag != 1:
            if type not in ['jpg','jpeg','png']:
                continue
            num += 1
            Z.extract(i, path=path)
            os.rename(path + f'/{i}', path + f'/{num}.{type}')
            f.write(f'{i} {num}.{type}\n')
        else:
            num += 1
            Z.extract(i,path=path)
            os.rename(path+f'/{i}',path+f'/{num}.{type}')
            f.write(f'{i} {num}.{type}\n')
    Z.close()
    f.close()
    #图片任务
    if flag != 1:
        task_should = math.floor(num/task_num)
        if task_should < 10:
            p = Project.objects.get(project_id=project_id)
            p.project_status = 6
            p.save()
            data = {'code':404, 'msg':'无法分配任务','path':path}
            shutil.rmtree(path)
        else:
            for i in os.listdir(path):
                try:
                    type = i.split('.')[1]
                    if type not in ['jpg','jpeg','png']:
                        continue
                    num = int(i.split('.')[0])
                    id = math.ceil(num/task_should)
                    if id >task_num:
                        id = task_num
                    os.rename(path + f'/{i}', path + f'/{num}_{id}.{type}')
                except:
                    pass
            pic = ''
            for i in os.listdir(path):
                try:
                    type = i.split('.')[1]
                    if type not in ['jpg','jpeg','png']:
                        continue
                    pic = i
                    break
                except:
                    pass
            p = Project.objects.get(project_id=project_id)
            p.project_pic = (path+f'/{pic}')[1:]
            p.item_per_task = task_should
            p.save()
            data = {'code': 200, 'msg': '写入成功'}
        return JsonResponse(data)
    #文本任务
    if flag == 1:
        p = Project.objects.get(project_id=project_id)
        p.project_pic = f'/static/sample_document/txt_pic/txt_defalut_pic.png'
        task_num = p.task_num
        n = 0
        try:
            with open(f'{path}/total.txt','w',encoding='gb18030') as fp:
                for i in range(1,num+1):
                    with open(f'{path}/{i}.txt','r',encoding='gb18030') as f:
                        for line in f:
                            n += 1
                            fp.write(line)
        except:
            with open(f'{path}/total.txt','w',encoding='gb18030') as fp:
                for i in range(1,num+1):
                    with open(f'{path}/{i}.txt','r',encoding='gbk') as f:
                        for line in f:
                            n += 1
                            fp.write(line)
        task_should = math.floor(n/task_num)
        p.item_per_task = task_should
        p.save()
        data = {'code': 200, 'msg': '写入成功'}
        return JsonResponse(data)


## TODO 预付款
def prepay(request,project_id):
    res = get_res(request)
    pay_per_task = float(res['pay_per_task'])
    task_num = int(res['task_num'])
    account_id = res['publisher_id']
    total = pay_per_task * task_num
    w = Wallet.objects.get(account_id=account_id)
    if w.account_num >= total:
        w.account_num -= total
        w.save()
        p = Prepay()
        p.prepay_amount = total
        p.prepay_balance = total
        p.project_id = project_id
        p.account_id = account_id
        p.save()
        data = {'code': 200}
    else:
        data = {'code':404}
    return data


## TODO 标注者取消任务
def give_up_task(request):
    res = get_res(request)
    account_id = res['account_id']
    task_id = res['task_id']
    ta = Task_association.objects.filter(Q(account_id=account_id),Q(task_id=task_id))
    ta.delete()
    t = Task.objects.get(task_id=task_id)
    t.task_status = 0
    t.save()
    return JsonResponse({'code': 200})


## TODO task提交成功后付款与升级
def completed_task(task_id):
    project_id = task_id.split('_')[0]
    t = Task.objects.get(task_id=task_id)
    ta = Task_association.objects.get(task_id=task_id)
    account_id = ta.account_id
    c = Consumer.objects.get(account_id=account_id)
    p = Project.objects.get(project_id=project_id)
    pre = Prepay.objects.get(project_id=project_id)
    w = Wallet.objects.get(account_id=account_id)
    r = Reward_record()
    web = Web_account()
    web.task_id = task_id
    t.save()
    r.reward_amount = p.payment_per_task
    r.task_id = task_id
    r.reward_time = datetime.datetime.now()
    r.save()
    pre.prepay_balance -= p.payment_per_task
    pre.save()
    p.completed_task_num += 1
    w.account_num += float(p.payment_per_task)*0.8
    web.PAF_time = datetime.datetime.now()
    web.PAF_amount = float(p.payment_per_task)*0.2
    web.PAF_type = p.project_type
    if web.PAF_balance is None:
        web.PAF_balance = 0
    web.PAF_balance += web.PAF_amount
    web.save()
    w.save()
    c.experience += t.score
    c.level = judge_level(c.experience)
    c.save()
    if p.task_num == p.completed_task_num:
        p.project_status = 2
    p.save()


def judge_status(status):
    if status == 0:
        return '未开始'
    if status == 1:
        return '已开始'
    if status == 5:
        return '已结束'
    if status == 10:
        return '暂停'

def judge_status_reverse(status):
    if status == '未开始':
        return 0
    if status == '已开始':
        return 1
    if status == '已结束':
        return 5
    if status == '暂停':
        return 10

## TODO 发布者任务管理面板
def project_management(request):
    res = get_res(request)
    account_id = res['account_id']
    where = res['params']
    plist = Project.objects.filter(account_id=account_id).exclude(project_status=6)
    now = datetime.datetime.now()
    for item in plist:
        if now>item.start_time.replace(tzinfo=None):
            item.project_status=1
        if now>item.due_time.replace(tzinfo=None):
            item.project_status=5
            project_id = item.project_id
            account_id = item.project_id
            w = Wallet.objects.get(account_id=account_id)
            p = Prepay.objects.get(project_id=project_id)
            w.account_num += p.prepay_balance
            w.save()
            p.delete()
        item.save()
    if where is not None:
        name = where['name']
        status = where['status']
        end_time = where['end_time']
        level_min = where['level_min']
        level_max= where['level_max']
        price_min = where['price_min']
        price_max = where['price_max']
        if name != '':
            plist = plist.filter(project_name__contains=name)
        if status != '':
            plist = plist.filter(project_status=judge_status_reverse(status))
        if end_time is not None:
            t = time.localtime(end_time / 1000 + 8 * 60 * 60)
            due_time = time.strftime("%Y-%m-%d %H:%M:%S", t)
            plist = plist.filter(due_time__lte=due_time)
        if level_max is not None:
            plist = plist.filter(project_star__lte=level_max)
        if level_min is not None:
            plist = plist.filter(project_star__gte=level_min)
        if price_max is not None:
            plist = plist.filter(payment_per_task__lte=price_max)
        if price_min is not None:
            plist = plist.filter(project_name__gte=price_min)
    missions = []
    for project in plist:
        data = {}
        data['mission_id'] = int(project.project_id)
        data['name'] = project.project_name
        data['state'] = judge_status(project.project_status)
        time_ = str(project.due_time)[:-6]
        time_s = int(time.mktime(time.strptime(time_, "%Y-%m-%d %H:%M:%S")))*1000
        data['end_time'] = time_s
        data['level'] = project.project_star
        data['money'] = project.payment_per_task
        data['edit'] = True
        data['edit_text'] = "修改"
        data['start_time'] = project.start_time
        if project.project_type == '文本类型标注':
            data['project_type'] = 1
        elif project.project_type == '图片识别标注':
            data['project_type'] = 2
        else:
            data['project_type'] = 3
        data['target'] = project.project_target
        missions.append(data)
    return JsonResponse({'code':200,'data':missions})


def task_management(request):
    res = get_res(request)
    account_id = res['account_id']
    where = res['params']
    ta = Task_association.objects.filter(account_id=account_id)
    if list(ta) == []:
        return JsonResponse({'code': 200, 'data': []})
    missions = []
    name = ''
    status = ''
    publisher = ''
    end_time = None
    start_time = None
    level_min = None
    level_max = None
    price_min = None
    price_max = None
    if where is not None:
        name = where['name']
        status = where['status']
        end_time = where['end_time']
        start_time = where['start_time']
        level_min = where['level_min']
        level_max = where['level_max']
        price_min = where['price_min']
        price_max = where['price_max']
        publisher = where['poster_name']
    for task in ta:
        data = {}
        task_id = task.task_id
        t = Task.objects.get(task_id=task_id)
        project_id = task.project_id
        p = Project.objects.get(project_id=project_id)
        if p.project_status >= 5:
            pass
        if name != '':
            s = p.project_name.find(name)
            if s == -1:
                continue
        if status != '':
            if p.project_status != judge_status_reverse(status):
                continue
        if end_time is not None:
            if p.due_time.replace(tzinfo=None) <= datetime.datetime.fromtimestamp(end_time / 1000):
                continue
        if start_time is not None:

            if p.due_time.replace(tzinfo=None) >= datetime.datetime.fromtimestamp(start_time / 1000):
                continue
        if level_max is not None:
            if p.project_star > level_max:
                continue
        if level_min is not None:
            if p.project_star < level_min:
                continue
        if price_max is not None:
            if p.payment_per_task > price_max:
                continue
        if price_min is not None:
            if p.payment_per_task < price_min:
                continue
        if publisher != '':
            d = Producer.objects.get(account_id=p.account_id)
            if d.nickname.find(publisher) == -1:
                continue
        data['mission_id'] = task_id
        data['name'] = p.project_name
        data['poster'] = Producer.objects.get(account_id=p.account_id).nickname
        data['state'] = judge_task(t.task_status)
        time_ = str(p.due_time)[:-6]
        time_s = int(time.mktime(time.strptime(time_, "%Y-%m-%d %H:%M:%S")))*1000
        data['end_time'] = time_s
        data['level'] = p.project_star
        data['money'] = p.payment_per_task
        time_ = str(p.start_time)[:-6]
        time_s = int(time.mktime(time.strptime(time_, "%Y-%m-%d %H:%M:%S")))*1000
        data['start_time'] = time_s
        if p.project_type == '文本类型标注':
            data['task_type'] = 1
        elif p.project_type == '图片识别标注':
            data['task_type'] = 2
        else:
            data['task_type'] = 3
        missions.append(data)
    return JsonResponse({'code': 200, 'data': missions})


#更新项目列表
def project_management_update(request):
    res = get_res(request)
    data = res['data']
    project_id = data['mission_id']
    p = Project.objects.get(project_id=project_id)
    p.project_name = data['name']
    p.project_status = judge_status_reverse(data['state'])
    t = time.localtime(((int(data['end_time']))/ 1000)+8*60*60)
    due_time = time.strftime("%Y-%m-%d %H:%M:%S", t)
    p.due_time = str(due_time)
    p.save()
    return JsonResponse({'code':200})

#任务验收
def acceptance_check(request):
    res = get_res(request)
    task_id = res['task_id']
    sample_num = int(res['sample_num'])
    project_id = task_id.split('_')[0]
    num = int(task_id.split('_')[1])
    p = Project.objects.get(project_id=project_id)
    type = p.project_type
    ta = Task_association.objects.get(task_id=task_id)
    consumer = ta.account_id
    path = f'./static/data/account_{consumer}_task_{task_id}/data.json'
    with open(path,'r') as f:
        data = json.load(f)
    sample = random.sample(data.keys(), sample_num)
    da = []
    for item in sample:
        da.append(data[item])
    if type == '文本类型标注':
        path2 = f'./static/sample_document/{project_id}/total.txt'
        p = Project.objects.get(project_id=project_id)
        start = int(p.item_per_task) * (num - 1)
        txt = []
        for i in sample:
            txt.append(get_text(path2, start + int(i)))
        call = []
        for i in range(sample_num):
            data = {}
            data['content'] = txt[i]
            data['value'] = da[i]
            call.append(data)
    else:
        path2 = f'http://localhost:8000/static/sample_document/{project_id}/'
        p = Project.objects.get(project_id=project_id)
        start = int(p.item_per_task) * (num - 1)
        pic_path = []
        for i in sample:
            pic_name = f'{start + int(i)}_{num}'
            pics = os.listdir(f'./static/sample_document/{project_id}/')
            for pic in pics:
                if pic.split('.')[0] == pic_name:
                    pic_path.append(path2 + pic)
        call = []
        if type == '图片识别标注':
            for i in range(sample_num):
                path3 ='http://localhost:8000/static/acceptance/'
                data = {}
                data['content'] = pic_path[i]
                path_pic = '.'+pic_path[i][21:]
                print(pic_path[i],"651")
                rectangle_pic(path_pic,f'./static/acceptance/{project_id}_{pic_path[i].split("/")[-1]}',da[i])
                data['value'] = path3 + f'{project_id}_{pic_path[i].split("/")[-1]}'
                call.append(data)
        else:
            for i in range(sample_num):
                data = {}
                data['content'] = pic_path[i]
                data['value'] = da[i]
                call.append(data)
    return JsonResponse({'code':200,'data':call,'mission_target':p.project_target,'task_id':task_id})

def get_text(path,index):
    with open(path,'r',encoding='gbk') as fp:
        count = 1
        for line in fp:
            if count == index:
                break
            count += 1
    return line[:-1]


def rectangle_pic(path1,path2,index):
    img_fpath = path1
    img = Image.open(img_fpath)
    width = img.size[0]  # 获取宽度
    height = img.size[1]  # 获取长度
    a = ImageDraw.ImageDraw(img)
    for item in index:
        x1 = item['x'] * width
        y1 = item['y'] * height
        x2 = item['ex'] * width
        y2 = item['ey'] * height
        print(path1,path2)
        a.rectangle(((x1, y1), (x2, y2)), fill=None, outline='red', width=5)
    img.save(path2)

def acceptance_show(request):
    res = get_res(request)
    project_id = res['project_id']
    p = Project.objects.get(project_id=project_id)
    ta = Task_association.objects.filter(project_id=project_id)
    if list(ta) == []:
        return JsonResponse({'code':200,'data':''})
    info = []
    for i in ta:
        task_consumer = i.account_id
        c = Consumer.objects.get(account_id=task_consumer)
        nickname = c.nickname
        level = c.level
        tel = c.tel
        pay = p.payment_per_task
        email = c.mail_add
        data = {}
        data['name'] = nickname
        data['level'] = level
        data['pay'] = pay
        data['phone_num'] = tel
        if email is None:
            email=''
        data['email']=email
        data['task_id'] = i.task_id
        task = Task.objects.get(task_id=i.task_id)
        s = int(task.task_status)
        if s == 2:
            data['task_status'] = 0
        elif s == 3:
            data['task_status'] = 1
        elif s == 4:
            data['task_status'] = 2
        elif s == 10:
            data['task_status'] = 3
        else:
            data['task_status'] = -1
        info.append(data)
    return JsonResponse({'code': 200,'data':info})

def error_append(request):
    res = get_res(request)
    task_id = res['task_id']
    if_accept = res['if_accept']
    wrong_item_list = res['wrong_item_list']
    t = Task.objects.get(task_id=task_id)
    if if_accept == 1:
        t.task_status = 3
        t.save()
        completed_task(task_id)
        return JsonResponse({'code':200})
    else:
        t.task_status=10
        t.save()
        for item in wrong_item_list:
            if item!={}:
                te = task_error()
                te.task_id = task_id
                te.error = item['content']
                te.error_value = item['value']
                te.save()
        return JsonResponse({'code': 200})


#0表示未接收，1表示被接收，2表示提交审核，3表示任务通过，4表示审核未通过
def judge_task(status):
    s = 0
    status = int(status)
    if status == 0:
        s = '未接收'
    if status == 1:
        s = '已领取'
    if status == 2:
        s = '提交审核'
    if status == 3:
        s = '任务通过'
    if status == 4:
        s = '审核未通过'
    if status == 10:
        s = '管理员审核中'
    return s


def get_data(request):
    res = get_res(request)
    task_id = res['task_id']
    project_id = task_id.split('_')[0]
    p = Project.objects.get(project_id=project_id)
    task_num = task_id.split('_')[1]
    path1 = f'./static/sample_document/{project_id}/map.txt'
    ta = Task_association.objects.get(task_id=task_id)
    account = ta.account_id
    path2 = f'./static/data/account_{account}_task_{task_id}/'
    path3 = path2 + 'data.json'
    f = open(path3,'r')
    data = json.load(f)
    start = int(p.item_per_task) * (int(task_num)-1) + 1
    num = 0
    i = 1
    ans = {}
    if p.project_type != '文本类型标注':
        with open(path1,'r',encoding='utf-8') as fp:
            for line in fp:
                num += 1
                if num >= start and num < start + int(p.item_per_task):
                    po = data[str(i)]
                    ans[line.split(' ')[0]] = po
                    i += 1
                if num >= start + int(p.item_per_task):
                    break
        with open('ans.json','w') as f2:
            json.dump(ans,f2)
        with zipfile.ZipFile(path2+'ans.zip', 'w',zipfile.ZIP_DEFLATED) as f:
            f.write('ans.json')
    else:
        with open(f'./static/sample_document/{project_id}/total.txt','r',encoding='gbk') as fp:
            print(start + int(p.item_per_task))
            for line in fp:
                print(line)
                num += 1
                if num >= start and num < start + int(p.item_per_task):
                    po = data[str(i)]
                    ans[line[:-1]] = po
                    i += 1
                if num >= start + int(p.item_per_task):
                    break
        with open('ans.json','w') as f2:
            json.dump(ans,f2)
        with zipfile.ZipFile(path2+'ans.zip', 'w',zipfile.ZIP_DEFLATED) as f:
            f.write('ans.json')
    return JsonResponse({'code':200,'url':f'http://localhost:8000/static/data/account_{account}_task_{task_id}/ans.zip'})

# 管理员审核
# 管理员审核
def admin_management(request):
    res = get_res(request)
    tlist = Task.objects.filter(task_status=10)
    if list(tlist) == []:
        return JsonResponse({'code': 200, 'data': []})
    missions = []
    task_id = res['task_id']
    name = res['project_name']
    poster_name = res['poster_name']
    project_type = res['project_type']
    for task in tlist:
        data = {}
        project_id = task.project_id
        p = Project.objects.get(project_id=project_id)
        pr = Producer.objects.get(account_id=p.account_id)
        if name != '':
            s = p.project_name.find(name)
            if s == -1:
                continue
        if task_id != '':
            if task.task_id != task_id:
                continue
        if poster_name != '':
            if pr.nickname.find(poster_name) == -1:
                continue
        if project_type != '':
            if p.project_type != project_type:
                continue
        data['mission_id'] = p.project_id
        data['name'] = p.project_name
        data['poster_name'] = pr.nickname
        data['state'] = judge_task(task.task_status)
        time_ = str(p.due_time)[:-6]
        time_s = int(time.mktime(time.strptime(time_, "%Y-%m-%d %H:%M:%S"))) * 1000
        data['end_time'] = time_s
        data['level'] = p.project_star
        data['money'] = p.payment_per_task
        time_ = str(p.start_time)[:-6]
        time_s = int(time.mktime(time.strptime(time_, "%Y-%m-%d %H:%M:%S"))) * 1000
        data['start_time'] = time_s
        data['task_id'] = task.task_id
        data['project_type'] = p.project_type
        missions.append(data)
    return JsonResponse({'code': 200, 'data': missions})




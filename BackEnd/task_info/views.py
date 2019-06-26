from django.shortcuts import *
from django.http import *
from django.shortcuts import *
from django.urls import *
import traceback
import json
from .models import *
from django.db.utils import IntegrityError
from django.db.models import F
from .crypto import *
import math
from account_info.models import User
from wallet_info.models import Wallet
from task_info.models import Task
from accept_task_info.models import AcceptTask


# Create your views here.
MAX_PAGE_ITEMS = 6

def dealResponse(status_code, res_text={}):
    traceback.print_exc()
    dic = {
        400 : 'Decode Failed',
        406 : 'Verification Failed',
        200 : 'Standard Successed',
        201 : 'Create Resource Successed',
        409 : 'Confict Field or MultipleAcceptance', 
        500 : 'Unknown Server Error',
        404 : 'Not Exist', 
        416 : 'OutOfRange or CompletedTask', 
        401 : 'Unauthorized', 
        403 : 'TaskBeenFinished'
    }
    traceback.print_exc()
    print('[+] ' + dic[status_code])
    res_text['status_code'] = status_code
    resp = HttpResponse(encrypt(json.dumps(res_text)))
    # resp.status_code = status_code
    return resp

def operate_task(request):
    """
    if not request.method == 'GET' and not request.method == 'POST':
        put = QueryDict(request.body)
        id = put.get('taskID')
        username = put.get('issuer')
        print(put)
        print(id)
        print(username)
        return dealResponse(200) 
    """
    if request.method == 'GET':
        try:
            id = decrypt(request.GET['taskID'])
        except:
            return dealResponse(400)
        try:
            result = Task.objects.get(taskID=id)
        except Task.DoesNotExist:
            return dealResponse(404)
        res_text = {
            'data':{
                'title' : result.title, 
                'content' : result.content, 
                'type' : result.types, 
                'issuer' : result.issuer.username, 
                'reward' : result.reward, 
                'deadline' : result.deadline, 
                'repeatTime' : result.repeatTime, 
                'isCompleted' : result.isCompleted, 
            }
        }
        return dealResponse(200, res_text)  
    elif request.method == 'POST':
        try:
            raw_string = decrypt(str(request.body, 'utf-8'))
            content = json.loads(raw_string)
            ttitle = content['title']
            tcontent = content['content']
            ttype = content['type']
            tissuer = content['issuer']
            treward = content['reward']
            trepeatTime = content['repeatTime']
            tdeadline = content['deadline']
        except:
            return dealResponse(400)
        try:
            user = User.objects.get(username=tissuer)
        except User.DoesNotExist:
            return dealResponse(404)
        task = Task(title=ttitle, content=tcontent, types=ttype,\
            issuer=user, reward=treward, repeatTime=trepeatTime,\
                deadline=tdeadline, )
        task.save()
        return dealResponse(201, {"data":{"taskID":task.taskID}})
    """
    elif request.method == 'DELETE':
        try:
            id = decrypt(request.DELETE['taskID'])
            username = decrypt(request.DELETE['issuer'])
        except:
            return dealResponse(400)
        try:
            result = Task.objects.get(taskID=id)
        except Task.DoesNotExist:
            return dealResponse(404)
        if result.issuer.username != username:
            return dealResponse(401) 
        result.isCompleted = True
        result.save()
        return dealResponse(200) 
    """

def task_finished(request):
    try:
        # id = decrypt(request.POST['taskID'])
        # username = decrypt(request.POST['issuer'])
        raw_string = decrypt(str(request.body, 'utf-8'))
        content = json.loads(raw_string)
        id = content['taskID']
        username = content['issuer']
    except:
        return dealResponse(400)
    try:
        result = Task.objects.get(taskID=id)
    except Task.DoesNotExist:
        return dealResponse(404)
    if result.issuer.username != username:
        return dealResponse(401) 
    result.isCompleted = True
    result.save()
    return dealResponse(200) 

def get_tasks(request):
    try:
        page = int(decrypt(request.GET['page']))
        title = decrypt(request.GET.get('title', default=''))
        types = decrypt(request.GET.get('type', default=''))
        issuer = decrypt(request.GET.get('issuer', default=''))
        content = decrypt(request.GET.get('content', default=''))
        isCompleted = decrypt(request.GET.get('isComplete', default=''))
    except:
        return dealResponse(400)
    dic = {}
    if title != '':
        dic['title'] = title
    if types != '':
        dic['types'] = types
    if issuer != '':
        dic['issuer'] = issuer
    if content != '':
        dic['content'] = content
    if isCompleted != '':
        if isCompleted == 'true':
            dic['isCompleted'] = True
        elif isCompleted == 'false':
            dic['isCompleted'] = False
    result = Task.objects.filter(**dic)
    # for item in result:
    #     print(item.taskID)
    max_pages = math.ceil(float(len(result)) / MAX_PAGE_ITEMS)
    if page > max_pages or page <= 0:
        return dealResponse(416, {"data": {"max_pages": max_pages}})
    page = page - 1
    resp = {"data" : {
            "tasks" : [], 
            "max_pages" : max_pages
        }
    }
    startid = page * MAX_PAGE_ITEMS
    endid = min(len(result), (page+1)*MAX_PAGE_ITEMS)
    for i in range(startid, endid):
        oner =  {
        "taskID": result[i].taskID,
        "title": result[i].title,
        "content": result[i].content,
        "type": result[i].types,
        "issuer": result[i].issuer.username,
        "reward": result[i].reward,
        "deadline": result[i].deadline,
        "repeatTime": result[i].repeatTime, 
        # "isCompleted": result[i].isCompleted,
      }
        resp['data']['tasks'].append(oner)
    return dealResponse(200, resp) 

def operate_created_tasks(request):
    if request.method == 'GET':
        try:
            page = int(decrypt(request.GET['page']))
            tusername = decrypt(request.GET['issuer'])
        except:
            return dealResponse(400)
        try:
            fuser = User.objects.get(username=tusername)
        except User.DoesNotExist:
            return dealResponse(404)
        result = Task.objects.filter(issuer=fuser)
        max_pages = math.ceil(float(len(result)) / MAX_PAGE_ITEMS)
        if page > max_pages or page <= 0:
            return dealResponse(416, {"data": {"max_pages": max_pages}})
        page = page - 1
        resp = {"data" : {
                "tasks" : [], 
                "max_pages" : max_pages
            }
        }
        startid = page * MAX_PAGE_ITEMS
        endid = min(len(result), (page+1)*MAX_PAGE_ITEMS)
        for i in range(startid, endid):
            oner =  {
            "taskID": result[i].taskID,
            "title": result[i].title,
            "content": result[i].content,
            "type": result[i].types,
            "issuer": result[i].issuer.username,
            "reward": result[i].reward,
            "deadline": result[i].deadline,
            "repeatTime": result[i].repeatTime, 
            "isFinished": result[i].isCompleted, 
        }
            resp['data']['tasks'].append(oner)
        return dealResponse(200, resp) 
    elif request.method == 'POST':
        try:
            raw_string = decrypt(str(request.body, 'utf-8'))
            content = json.loads(raw_string)
            ttaskID = content['taskID']
            ttitle = content['title']
            tissuer = content['issuer']
            treward = content['reward']
            tdeadline = content['deadline']
        except:
            return dealResponse(400)
        try:
            task = Task.objects.get(taskID=ttaskID)
            user = User.objects.get(username=tissuer)
        except(Task.DoesNotExist, User.DoesNotExist):
            return dealResponse(404)
        if user != task.issuer:
            return dealResponse(401)
        task.title = ttitle
        task.reward = treward
        task.deadline = tdeadline
        task.save()
        return dealResponse(200)
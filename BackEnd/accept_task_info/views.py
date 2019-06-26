from django.shortcuts import render
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

def operate_accepted_tasks(request):
    if request.method == 'GET':
        try:
            page = int(decrypt(request.GET['page']))
            tusername = decrypt(request.GET['username'])
        except:
            return dealResponse(400)
        try:
            fuser = User.objects.get(username=tusername)
        except User.DoesNotExist:
            return dealResponse(404)
        result = AcceptTask.objects.filter(user=fuser)
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
            thetask = result[i].task
            oner =  {
            "taskID": thetask.taskID,
            "title": thetask.title,
            "content": thetask.content,
            "type": thetask.types,
            "issuer": thetask.issuer.username,
            "reward": thetask.reward,
            "deadline": thetask.deadline,
            "repeatTime": thetask.repeatTime, 
            "isFinished": result[i].isFinished, 
        }
            resp['data']['tasks'].append(oner)
        return dealResponse(200, resp) 
    elif request.method == 'POST':
        try:
            raw_string = decrypt(str(request.body, 'utf-8'))
            content = json.loads(raw_string)
            tusername = content['username']
            ttaskid = content['taskID']
            tanswer = None
            if 'answer' in content:
                tanswer = content['answer']
        except:
            return dealResponse(400)
        try:
            nuser = User.objects.get(username=tusername)
            ntask = Task.objects.get(taskID=ttaskid)
        except(User.DoesNotExist, Task.DoesNotExist):
            return dealResponse(404)
        testask = AcceptTask.objects.filter(user=nuser, task=ntask)
        if len(testask) != 0:
            return dealResponse(409)
        if tanswer is None:
            aptask = AcceptTask(user=nuser, task=ntask, \
                answer=tanswer, isFinished=False)
        else:
            aptask = AcceptTask(user=nuser, task=ntask, \
                answer=tanswer, isFinished=True)
        aptask.save()
        return dealResponse(201)

def operate_acceptance(request):
    if request.method == 'GET':
        try:
            page = int(decrypt(request.GET['page']))
            tusername = decrypt(request.GET['issuer'])
            ttaskID = decrypt(request.GET['taskID'])
        except:
            return dealResponse(400)
        try:
            fuser = User.objects.get(username=tusername)
            ttask = Task.objects.get(taskID=ttaskID)
        except(User.DoesNotExist, Task.DoesNotExist):
            return dealResponse(404)
        if fuser != ttask.issuer:
            return dealResponse(401)
        result = AcceptTask.objects.filter(task=ttask)
        max_pages = math.ceil(float(len(result)) / MAX_PAGE_ITEMS)
        if page > max_pages or page <= 0:
            return dealResponse(416, {"data": {"max_pages": max_pages}})
        page = page - 1
        resp = {"data" : {
                "records" : [], 
                "max_pages" : max_pages
            }
        }
        startid = page * MAX_PAGE_ITEMS
        endid = min(len(result), (page+1)*MAX_PAGE_ITEMS)
        for i in range(startid, endid):
            oner =  {
            "userID": result[i].user.username, 
            "isFinished": result[i].isFinished, 
            "answer":result[i].answer
        }
            resp['data']['records'].append(oner)
        return dealResponse(200, resp) 
    elif request.method == 'POST':
        try:
            raw_string = decrypt(str(request.body, 'utf-8'))
            content = json.loads(raw_string)
            tuserID = content['userID']
            ttaskID = content['taskID']
            tissuer = content['issuer']
        except:
            return dealResponse(400)
        try:
            ntask = Task.objects.get(taskID=ttaskID)
            nuser = User.objects.get(username=tuserID)
            nissuer = User.objects.get(username=tissuer)
        except(Task.DoesNotExist, User.DoesNotExist):
            return dealResponse(404)
        if nissuer != ntask.issuer:
            return dealResponse(401)
        aptask = AcceptTask.objects.get(user=nuser, task=ntask)
        if aptask.isFinished or ntask.isCompleted:
            return dealResponse(416)
        aptask.isFinished = True
        aptask.save()
        # if task finish
        ntask.repeatTime = ntask.repeatTime - 1
        if ntask.repeatTime <= 0:
            ntask.repeatTime = 0
            ntask.isCompleted = True
        ntask.save()
        return dealResponse(200)

def acceptance_removed(request):
    try:
        raw_string = decrypt(str(request.body, 'utf-8'))
        content = json.loads(raw_string)
        tusername = content['username']
        ttaskid = content['taskID']
    except:
        return dealResponse(400)
    try:
        nuser = User.objects.get(username=tusername)
        ntask = Task.objects.get(taskID=ttaskid)
        aptask = AcceptTask.objects.get(user=nuser, task=ntask)
    except(User.DoesNotExist, Task.DoesNotExist\
        , AcceptTask.DoesNotExist):
        return dealResponse(404)
    if aptask.isFinished == True:
        return dealResponse(403)       
    aptask.delete()
    return dealResponse(200)
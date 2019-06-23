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

# Create your views here.
MAX_PAGE_ITEMS = 2

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
        416 : 'OutOfRange', 
        401 : 'Unauthorized', 
    }
    traceback.print_exc()
    print('[+] ' + dic[status_code])
    res_text['status_code'] = status_code
    resp = HttpResponse(encrypt(json.dumps(res_text)))
    # resp.status_code = status_code
    return resp

def index(request):
    return HttpResponse('Welcome to coin arrival backend.')

def verification(request):
    res_text = {}
    try:
        # raw_string = decrypt(request.POST['account'])
        raw_string = decrypt(str(request.body, 'utf-8'))
        content = json.loads(raw_string)
        tusername = content['username']
        tpassword = content['password']
    except:
        return dealResponse(400)
    
    try:
        result = User.objects.get(username=tusername, password=tpassword)
    except User.DoesNotExist:
        return dealResponse(406)
    return dealResponse(200)

def operate_account_info(request):
    if request.method == 'GET':
        try:
            tusername = decrypt(request.GET['username'])
        except:
            return dealResponse(400)
        try:
            result = User.objects.get(username=tusername)
        except User.DoesNotExist:
            return dealResponse(404)
        res_text = {
            'data':{
                'userID': result.userID, 
                'username' : tusername,
                'gender' : result.gender,
                'email' : result.email,
                'phone' : result.phone, 
                'school' : result.school, 
                'major' : result.major, 
                'age' : result.age, 
                'role' : result.role, 
                # 'studentID' : result.studentID, 
                # 'teacherID' : result.teacherID, 
                # 'grade' : result.grade, 
                'avatar' : result.avatar,
            }
        }
        if result.role == "teacher":
            res_text['data']['teacherID'] = result.teacherID
        elif result.role == "student":
            res_text['data']['studentID'] = result.studentID
            res_text['data']['grade'] = result.grade
        return dealResponse(200, res_text)
        
    elif request.method == 'POST':
        try:
            # raw_string = decrypt(request.POST['account'])
            raw_string = decrypt(str(request.body, 'utf-8'))
            content = json.loads(raw_string)


            tusername = content['username']
            tpassword = tgender = temail = tphone = tschool = tmajor = \
                tage = trole = tstudentID = tgrade = \
                    tteacherID = tavatar = None

            if 'password' in content:
                tpassword = content['password']
            if 'gender' in content:
                tgender = content['gender']
            if 'email' in content:
                temail = content['email']
            if 'phone' in content:
                tphone = content['phone']
            if 'school' in content:
                tschool = content['school']
            if 'major' in content:
                tmajor = content['major']
            if 'age' in content:
                tage = content['age']
            if 'role' in content:
                trole  = content['role']
            if 'studentID' in content:
                tstudentID = content['studentID']
            if 'grade' in content:
                tgrade = content['grade']
            if 'teacherID' in content:
                tteacherID = content['teacherID']
            if 'avatar' in content:
                tavatar = content['avatar']
        except:
            return dealResponse(400)
        try:
            result = User.objects.get(username=tusername)
        except User.DoesNotExist:
            return dealResponse(404)
        # if temail == result.email:
        #     return dealResponse(409, {'confict_field' : 'email'})
        # else if tphone == result.phone:
        #     return dealResponse(409, {'confict_field' : 'phone'})
        try:
            if tgender != None:
                result.gender = tgender
            if temail != None:
                result.email = temail
            if tphone != None:
                result.phone = tphone
            if tschool != None:
                result.school = tschool
            if tmajor != None:
                result.major = tmajor
            if tage != None:
                result.age = tage
            if tstudentID != None:
                result.studentID = tstudentID
            if tgrade != None:
                result.grade = tgrade
            if tteacherID != None:
                result.teacherID = tteacherID
            if tavatar != None:
                result.avatar = tavatar
            if tpassword != None:
                result.password = tpassword
            if trole != None:
                result.role = trole
            result.save()
        except IntegrityError:
            try:
                test = User.objects.get(email=temail)
            except User.DoesNotExist:
                test = None
            if test:
                return dealResponse(409, {'data':{'which':'email'}})

            try:
                test = User.objects.get(phone=tphone)
            except User.DoesNotExist:
                test = None
            if test:
                return dealResponse(409, {'data':{'which':'phone'}})
        return dealResponse(201)
    else:
        return dealResponse(400)

def registration(request):
    try:
        # raw_string = decrypt(request.POST['account'])
        raw_string = decrypt(str(request.body, 'utf-8'))
        content = json.loads(raw_string)
        tusername = content['username']
        tpassword = content['password']
        temail = content['email']
        tphone = content['phone']
    except:
        return dealResponse(400)
    try:
        account = User(username=tusername, password=tpassword, \
            email=temail, phone=tphone,)
        account.save()
        user_wallet = Wallet(balance=0, user=account)
        user_wallet.save()
    except IntegrityError:
        try:
            test = User.objects.get(username=tusername)
        except User.DoesNotExist:
            test = None
        if test:
            return dealResponse(409, {'data':{'which':'username'}})

        try:
            test = User.objects.get(email=temail)
        except User.DoesNotExist:
            test = None
        if test:
            return dealResponse(409, {'data':{'which':'email'}})

        try:
            test = User.objects.get(phone=tphone)
        except User.DoesNotExist:
            test = None
        if test:
            return dealResponse(409, {'data':{'which':'phone'}})
    return dealResponse(201)

def get_balance(request):
    try:
        tusername = decrypt(request.GET['username'])
    except:
        return dealResponse(400)
    try:
        result = User.objects.get(username=tusername)
    except User.DoesNotExist:
        return dealResponse(404)
    return dealResponse(200, {'data':{'balance':result.wallet_set.first().balance}})


def operate_task(request):
    # if not request.method == 'GET' and not request.method == 'POST':
    #     put = QueryDict(request.body)
    #     id = put.get('taskID')
    #     username = put.get('issuer')
    #     print(put)
    #     print(id)
    #     print(username)
    #     return dealResponse(200) 
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
        return dealResponse(201)
    # elif request.method == 'DELETE':
    #     try:
    #         id = decrypt(request.DELETE['taskID'])
    #         username = decrypt(request.DELETE['issuer'])
    #     except:
    #         return dealResponse(400)
    #     try:
    #         result = Task.objects.get(taskID=id)
    #     except Task.DoesNotExist:
    #         return dealResponse(404)
    #     if result.issuer.username != username:
    #         return dealResponse(401) 
    #     result.isCompleted = True
    #     result.save()
        # return dealResponse(200) 

def task_finished(request):
    try:
        id = decrypt(request.POST['taskID'])
        username = decrypt(request.POST['issuer'])
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
        isComplete = decrypt(request.GET.get('isComplete', default=''))
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
    if isComplete != '':
        dic['isComplete'] = isComplete
    result = Task.objects.filter(**dic)
    # for item in result:
    #     print(item.taskID)
    max_pages = math.ceil(float(len(result)) / MAX_PAGE_ITEMS)
    if page >= max_pages:
        return dealResponse(416, {"data": {"max_pages": max_pages}})
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
        "isCompleted": result[i].isCompleted, 
      }
        resp['data']['tasks'].append(oner)
    return dealResponse(200, resp) 

def operate_accepted_tasks(request):
    if request.method == 'GET':
        try:
            page = int(decrypt(request.GET['page']))
            tusername = request.GET['username']
        except:
            return dealResponse(400)
        try:
            fuser = User.objects.get(username=tusername)
        except User.DoesNotExist:
            return dealResponse(404)
        result = AcceptTask.objects.filter(user=fuser)
        max_pages = math.ceil(float(len(result)) / MAX_PAGE_ITEMS)
        if page >= max_pages:
            return dealResponse(416, {"data": {"max_pages": max_pages}})
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
            "isCompleted": thetask.isCompleted, 
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
        except User.DoesNotExist or Task.DoesNotExist:
            return dealResponse(404)
        testask = AcceptTask.objects.filter(user=nuser, task=ntask)
        if len(testask) != 0:
            return dealResponse(409)
        aptask = AcceptTask(user=nuser, task=ntask, \
            answer=tanswer, isFinished=False)
        aptask.save()
        return dealResponse(201)
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

# Create your views here.

def dealResponse(status_code, res_text={}):
    traceback.print_exc()
    dic = {
        400 : 'Decode Failed',
        406 : 'Verification Failed',
        200 : 'Standard Successed',
        201 : 'Create Resource Successed',
        409 : 'Confict Field', 
        500 : 'Unknown Server Error',
        404 : 'Not Exist'
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
        account = User(username=tusername, password=tpassword, email=temail, phone=tphone)
        account.save()
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
    except:
        return dealResponse(500)
    return dealResponse(201)
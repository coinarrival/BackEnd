from django.shortcuts import *
from django.http import *
from django.shortcuts import *
from django.urls import *
import traceback
import json
from .models import account_info
from django.db.utils import IntegrityError
from django.db.models import F
from .crypto import *

# Create your views here.

def dealResponse(status_code, res_text={}):
    # traceback.print_exc()
    dic = {
        400 : 'Decode Failed',
        406 : 'Verification Failed',
        200 : 'Successed',
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
        result = account_info.objects.get(username=tusername, password=tpassword)
    except account_info.DoesNotExist:
        return dealResponse(406)
    return dealResponse(200)

def operate_account_info(request):
    if request.method == 'GET':
        try:
            tusername = decrypt(request.GET['username'])
        except:
            return dealResponse(400)
        try:
            result = account_info.objects.get(username=tusername)
        except account_info.DoesNotExist:
            return dealResponse(404)
        res_text = {
            'data':{
                'username' : tusername,
                'password' : result.password, 
                'email' : result.email,
                'phone' : result.phone, 
                'avatar' : result.avatar,
            }
        }
        return dealResponse(200, res_text)
        
    elif request.method == 'POST':
        try:
            # raw_string = decrypt(request.POST['account'])
            raw_string = decrypt(str(request.body, 'utf-8'))
            content = json.loads(raw_string)
            tusername = content['username']
            tpassword = content['password']
            temail = content['email']
            tphone = content['phone']
            tavatar = content['avatar']
        except:
            return dealResponse(400)
        try:
            result = account_info.objects.get(username=tusername)
        except account_info.DoesNotExist:
            return dealResponse(404)
        # if temail == result.email:
        #     return dealResponse(409, {'confict_field' : 'email'})
        # else if tphone == result.phone:
        #     return dealResponse(409, {'confict_field' : 'phone'})
        try:
            result.email = temail
            result.phone = tphone
            result.avatar = tavatar
            result.password = tpassword
            result.save()
        except IntegrityError:
            try:
                test = account_info.objects.get(email=temail)
            except account_info.DoesNotExist:
                test = None
            if test:
                return dealResponse(409, {'data':{'which':'email'}})

            try:
                test = account_info.objects.get(phone=tphone)
            except account_info.DoesNotExist:
                test = None
            if test:
                return dealResponse(409, {'data':{'which':'phone'}})
        return dealResponse(200)
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
        account = account_info(username=tusername, password=tpassword, email=temail, phone=tphone)
        account.save()
    except IntegrityError:
        try:
            test = account_info.objects.get(username=tusername)
        except account_info.DoesNotExist:
            test = None
        if test:
            return dealResponse(409, {'data':{'which':'username'}})

        try:
            test = account_info.objects.get(email=temail)
        except account_info.DoesNotExist:
            test = None
        if test:
            return dealResponse(409, {'data':{'which':'email'}})

        try:
            test = account_info.objects.get(phone=tphone)
        except account_info.DoesNotExist:
            test = None
        if test:
            return dealResponse(409, {'data':{'which':'phone'}})
    return dealResponse(200)